#!/usr/bin/env python3
"""
Deployment script for GCP instances using Python
Deploys scraping server code and runs it on one or multiple instances
"""

import os
import sys
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


# Configuration
REMOTE_DIR = "~/waterlily-scraper"
LOCAL_DIR = Path(__file__).parent.absolute()
DEPLOYMENT_CONFIG = LOCAL_DIR / "config" / "deployment.json"


@dataclass
class DeploymentTarget:
    """Represents a single deployment target"""
    gcp_zone: str
    gcp_project: str
    gcp_instance: str
    remote_dir: str = REMOTE_DIR
    
    def __str__(self):
        return f"{self.gcp_instance} ({self.gcp_zone}, {self.gcp_project})"


def run_command(cmd: List[str], check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=check,
        capture_output=capture_output,
        text=True
    )
    
    if result.stdout and capture_output:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    
    return result


def gcloud_ssh(target: DeploymentTarget, command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run command on GCP instance via SSH"""
    cmd = [
        "gcloud", "compute", "ssh",
        "--zone", target.gcp_zone,
        target.gcp_instance,
        "--project", target.gcp_project,
        "--command", command
    ]
    return run_command(cmd, check=check)


def gcloud_scp(target: DeploymentTarget, source: str, dest: str) -> subprocess.CompletedProcess:
    """Copy file to GCP instance"""
    cmd = [
        "gcloud", "compute", "scp",
        "--zone", target.gcp_zone,
        "--project", target.gcp_project,
        source,
        f"{target.gcp_instance}:{dest}"
    ]
    return run_command(cmd)


def create_deployment_archive() -> str:
    """Create tar archive excluding output folders"""
    print("\nCreating deployment archive...")
    
    exclude_patterns = [
        'output*',
        '__pycache__',
        '*.pyc',
        '.git',
        '*.log',
        '.DS_Store',
        '*.swp',
        '*.swo',
        'server.pid',
        '*.tar.gz',
        'venv',
        '.venv'
    ]
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz')
    temp_file.close()
    
    with tarfile.open(temp_file.name, 'w:gz') as tar:
        for root, dirs, files in os.walk(LOCAL_DIR):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not any(
                d.startswith(pattern.rstrip('*')) or pattern in d 
                for pattern in exclude_patterns
            )]
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(LOCAL_DIR)
                
                # Skip excluded files
                if any(
                    str(rel_path).startswith(pattern.rstrip('*')) or 
                    pattern in str(rel_path) or
                    file_path.match(pattern)
                    for pattern in exclude_patterns
                ):
                    continue
                
                tar.add(file_path, arcname=rel_path)
    
    print(f"Archive created: {temp_file.name}")
    return temp_file.name


def deploy_code(target: DeploymentTarget) -> None:
    """Deploy code to GCP instance"""
    print(f"\n{'='*60}")
    print(f"Deploying code to {target}")
    print(f"{'='*60}")
    
    # Create archive
    archive_path = create_deployment_archive()
    
    try:
        # Create remote directory
        gcloud_ssh(target, f"mkdir -p {target.remote_dir}")
        
        # Copy archive
        remote_archive = "/tmp/waterlily-deploy.tar.gz"
        gcloud_scp(target, archive_path, remote_archive)
        
        # Extract archive
        gcloud_ssh(target, f"""
            cd {target.remote_dir}
            tar -xzf {remote_archive}
            rm {remote_archive}
            echo 'Code extracted successfully'
        """)
        
        print(f"✓ Code deployed to {target.gcp_instance}")
    finally:
        # Cleanup local archive
        os.unlink(archive_path)


def install_dependencies(target: DeploymentTarget) -> None:
    """Install pip3, venv, unzip and Python dependencies"""
    print(f"\nInstalling dependencies on {target.gcp_instance}...")
    
    # Check and install pip3, python3-venv, and unzip
    gcloud_ssh(target, """
        if command -v apt-get &> /dev/null; then
            echo 'Installing system packages (Debian/Ubuntu)...'
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv unzip || {
                echo 'Warning: Some packages may have failed to install'
            }
        elif command -v yum &> /dev/null; then
            echo 'Installing system packages (RHEL/CentOS)...'
            sudo yum install -y python3-pip python3-devel unzip || {
                echo 'Warning: Some packages may have failed to install'
            }
        else
            echo 'Error: Could not determine package manager'
            exit 1
        fi
        
        # Verify installations
        if command -v pip3 &> /dev/null; then
            echo 'pip3 installed:'
            pip3 --version
        fi
        
        if command -v python3 &> /dev/null; then
            echo 'python3 version:'
            python3 --version
        fi
    """)
    
    # Create and activate virtual environment, then install Python requirements
    gcloud_ssh(target, f"""
        cd {target.remote_dir}
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            echo 'Creating virtual environment...'
            python3 -m venv venv
        else
            echo 'Virtual environment already exists'
        fi
        
        # Activate virtual environment and install requirements
        echo 'Activating virtual environment and installing requirements...'
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt || {{
            echo 'Warning: Some packages may have failed to install'
        }}
        echo 'Requirements installation completed'
        deactivate
    """)


def install_chrome(target: DeploymentTarget) -> None:
    """Install Chrome (ChromeDriver managed by webdriver-manager)"""
    print(f"\nInstalling Chrome on {target.gcp_instance}...")
    
    gcloud_ssh(target, """
        # Install Chrome
        if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
            echo 'Installing Google Chrome...'
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y wget gnupg
                wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
                sudo apt-get update
                sudo apt-get install -y google-chrome-stable
            elif command -v yum &> /dev/null; then
                sudo yum install -y wget
                wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
                sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
                rm -f google-chrome-stable_current_x86_64.rpm
            fi
        else
            echo 'Chrome already installed'
        fi
        
        # Note: ChromeDriver will be automatically managed by webdriver-manager package
        echo 'ChromeDriver will be automatically managed by webdriver-manager'
    """)


def kill_existing_server(target: DeploymentTarget) -> None:
    """Kill existing server process if running"""
    print(f"\nChecking for existing server process on {target.gcp_instance}...")
    
    gcloud_ssh(target, f"""
        cd {target.remote_dir}
        
        # Stop existing server if running
        echo 'Checking for existing server process...'
        
        # Kill process from server.pid if it exists
        if [ -f server.pid ]; then
            OLD_PID=$(cat server.pid)
            if ps -p $OLD_PID > /dev/null 2>&1; then
                echo 'Stopping existing server (PID: $OLD_PID)...'
                kill $OLD_PID || true
                sleep 2
                # Force kill if still running
                if ps -p $OLD_PID > /dev/null 2>&1; then
                    echo 'Force killing server process...'
                    kill -9 $OLD_PID || true
                    sleep 1
                fi
            fi
            rm -f server.pid
        fi
        
        # Also check for any process using port 5001 and kill it
        PORT_PID=""
        if command -v lsof &> /dev/null; then
            PORT_PID=$(lsof -ti:5001 2>/dev/null || true)
        elif command -v ss &> /dev/null; then
            PORT_PID=$(ss -tlnp | grep ':5001' | grep -oP 'pid=\\K[0-9]+' | head -1 || true)
        elif command -v fuser &> /dev/null; then
            PORT_PID=$(fuser 5001/tcp 2>/dev/null | awk '{{print $1}}' || true)
        fi
        
        if [ ! -z "$PORT_PID" ] && [ "$PORT_PID" != "-" ]; then
            echo "Found process using port 5001 (PID: $PORT_PID), killing it..."
            kill $PORT_PID 2>/dev/null || true
            sleep 2
            if ps -p $PORT_PID > /dev/null 2>&1; then
                echo 'Force killing process on port 5001...'
                kill -9 $PORT_PID 2>/dev/null || true
                sleep 1
            fi
        fi
    """)


def start_server(target: DeploymentTarget, server_config: Optional[Dict[str, Any]] = None) -> None:
    """
    Start the scraping server
    
    Args:
        target: Deployment target
        server_config: Optional server configuration (for future use)
                      e.g., {"headless": True, "port": 5001, "config_file": "..."}
    """
    print(f"\nStarting server on {target.gcp_instance}...")
    
    # Future: use server_config for port, headless mode, etc.
    port = server_config.get("port", 5001) if server_config else 5001
    
    gcloud_ssh(target, f"""
        cd {target.remote_dir}
        
        # Activate virtual environment and start server
        echo 'Activating virtual environment and starting server...'
        source venv/bin/activate
        nohup python scrapers/server.py > server.log 2>&1 &
        echo $! > server.pid
        deactivate
        
        sleep 2
        
        # Check if server started
        if [ -f server.pid ]; then
            PID=$(cat server.pid)
            if ps -p $PID > /dev/null 2>&1; then
                echo "Server started successfully (PID: $PID)"
                echo "Server logs: tail -f {target.remote_dir}/server.log"
            else
                echo 'Server failed to start. Check server.log for errors:'
                tail -20 server.log
                exit 1
            fi
        else
            echo 'Failed to create PID file'
            exit 1
        fi
    """)


def deploy_to_target(
    target: DeploymentTarget,
    server_config: Optional[Dict[str, Any]] = None,
    skip_chrome: bool = False
) -> None:
    """
    Deploy to a single target
    
    Args:
        target: Deployment target
        server_config: Optional server configuration
        skip_chrome: Skip Chrome installation if True
    """
    print(f"\n{'='*60}")
    print(f"Deploying to {target}")
    print(f"{'='*60}")
    
    try:
        # Deploy code
        deploy_code(target)
        
        # Install dependencies
        install_dependencies(target)
        
        # Install Chrome (unless skipped)
        if not skip_chrome:
            install_chrome(target)
        else:
            print(f"\nSkipping Chrome installation on {target.gcp_instance}")
        
        # Kill existing server
        kill_existing_server(target)
        
        # Start server
        start_server(target, server_config)
        
        print(f"\n{'='*60}")
        print(f"✓ Deployment completed for {target.gcp_instance}")
        print(f"{'='*60}")
        print(f"Server is running on: http://{target.gcp_instance}:5001")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error deploying to {target.gcp_instance}: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error deploying to {target.gcp_instance}: {e}", file=sys.stderr)
        raise


def load_deployment_config(config_path: Path = DEPLOYMENT_CONFIG) -> List[Dict[str, Any]]:
    """Load deployment configuration from JSON file"""
    if not config_path.exists():
        raise FileNotFoundError(f"Deployment config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config.get('targets', [])


def deploy_batch(
    config_path: Path = DEPLOYMENT_CONFIG,
    server_config: Optional[Dict[str, Any]] = None,
    skip_chrome: bool = False
) -> None:
    """
    Deploy to multiple targets from deployment config
    
    Args:
        config_path: Path to deployment.json config file
        server_config: Optional server configuration for all targets
        skip_chrome: Skip Chrome installation if True
    """
    print(f"\n{'='*60}")
    print("Batch Deployment")
    print(f"{'='*60}")
    print(f"Loading config from: {config_path}")
    
    targets_config = load_deployment_config(config_path)
    
    if not targets_config:
        print("No targets found in deployment config")
        return
    
    # Create deployment targets
    all_targets = []
    for target_config in targets_config:
        zone = target_config.get('gcp_zone')
        project = target_config.get('gcp_project')
        instances = target_config.get('gcp_instances', [])
        
        if not zone or not project or not instances:
            print(f"Warning: Skipping invalid target config: {target_config}")
            continue
        
        for instance in instances:
            all_targets.append(DeploymentTarget(
                gcp_zone=zone,
                gcp_project=project,
                gcp_instance=instance
            ))
    
    if not all_targets:
        print("No valid targets found")
        return
    
    print(f"\nFound {len(all_targets)} target(s) to deploy:")
    for target in all_targets:
        print(f"  - {target}")
    print()
    
    # Deploy to each target
    results = []
    for i, target in enumerate(all_targets, 1):
        print(f"\n[{i}/{len(all_targets)}] Processing {target.gcp_instance}...")
        try:
            deploy_to_target(target, server_config=server_config, skip_chrome=skip_chrome)
            results.append((target, True, None))
        except Exception as e:
            print(f"✗ Failed to deploy to {target.gcp_instance}: {e}", file=sys.stderr)
            results.append((target, False, str(e)))
    
    # Print summary
    print(f"\n{'='*60}")
    print("Deployment Summary")
    print(f"{'='*60}")
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total targets: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print("Successfully deployed to:")
        for target, success, _ in results:
            if success:
                print(f"  ✓ {target.gcp_instance} - http://{target.gcp_instance}:5001")
    
    if failed > 0:
        print("\nFailed deployments:")
        for target, success, error in results:
            if not success:
                print(f"  ✗ {target.gcp_instance}: {error}")
    
    if failed > 0:
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy scraping server to GCP instances')
    parser.add_argument(
        '--target',
        action='store_true',
        help='Deploy to a single target (requires --zone, --instance, --project)'
    )
    parser.add_argument(
        '--zone',
        type=str,
        help='GCP zone (required for single target)'
    )
    parser.add_argument(
        '--instance',
        type=str,
        help='GCP instance name (required for single target)'
    )
    parser.add_argument(
        '--project',
        type=str,
        help='GCP project ID (required for single target)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Deploy to multiple targets from deployment.json config'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(DEPLOYMENT_CONFIG),
        help=f'Path to deployment config file (default: {DEPLOYMENT_CONFIG})'
    )
    parser.add_argument(
        '--skip-chrome',
        action='store_true',
        help='Skip Chrome installation'
    )
    # Future: add more server config options
    # parser.add_argument('--port', type=int, default=5001, help='Server port')
    # parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    # Future: build server_config from args
    server_config = {}
    # if args.port:
    #     server_config['port'] = args.port
    # if args.headless:
    #     server_config['headless'] = True
    
    if args.target:
        # Single target deployment
        if not args.zone or not args.instance or not args.project:
            parser.error("--target requires --zone, --instance, and --project")
        
        target = DeploymentTarget(
            gcp_zone=args.zone,
            gcp_project=args.project,
            gcp_instance=args.instance
        )
        
        deploy_to_target(target, server_config=server_config, skip_chrome=args.skip_chrome)
        
    elif args.batch:
        # Batch deployment
        config_path = Path(args.config)
        deploy_batch(
            config_path=config_path,
            server_config=server_config,
            skip_chrome=args.skip_chrome
        )
    else:
        # Default: batch deployment
        deploy_batch(
            server_config=server_config,
            skip_chrome=args.skip_chrome
        )


if __name__ == "__main__":
    main()

