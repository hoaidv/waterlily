#!/usr/bin/env python3
"""
VM Management script for GCP instances
Start/stop/refresh all VMs from deployment.json or specific VMs
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


# Configuration
LOCAL_DIR = Path(__file__).parent.absolute()
DEPLOYMENT_CONFIG = LOCAL_DIR / "config" / "deployment.json"
DEPLOYMENT_STATUS_CONFIG = LOCAL_DIR / "config" / "deployment-status.json"


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=check,
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    
    return result


def gcloud_instance_operation(
    operation: str,
    zone: str,
    project: str,
    instance: str
) -> subprocess.CompletedProcess:
    """
    Perform start/stop operation on a GCP instance
    
    Args:
        operation: 'start' or 'stop'
        zone: GCP zone
        project: GCP project ID
        instance: Instance name
    """
    if operation not in ['start', 'stop']:
        raise ValueError(f"Invalid operation: {operation}. Must be 'start' or 'stop'")
    
    cmd = [
        "gcloud", "compute", "instances", operation,
        instance,
        "--zone", zone,
        "--project", project
    ]
    
    return run_command(cmd)


def get_instance_status(zone: str, project: str, instance: str, quiet: bool = True) -> Optional[str]:
    """
    Get the status of a GCP instance (RUNNING, STOPPED, TERMINATED, etc.)
    
    Args:
        zone: GCP zone
        project: GCP project ID
        instance: Instance name
        quiet: If True, suppress command output
    
    Returns:
        Status string (e.g., 'RUNNING', 'STOPPED') or None if not found
    """
    cmd = [
        "gcloud", "compute", "instances", "describe",
        instance,
        "--zone", zone,
        "--project", project,
        "--format", "value(status)"
    ]
    
    try:
        if quiet:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        else:
            result = run_command(cmd, check=True)
        
        status = result.stdout.strip()
        return status if status else None
    except subprocess.CalledProcessError:
        return None


def get_instance_ip(zone: str, project: str, instance: str, quiet: bool = True) -> Optional[str]:
    """
    Get the external IP address of a GCP instance
    
    Args:
        zone: GCP zone
        project: GCP project ID
        instance: Instance name
        quiet: If True, suppress command output
    
    Returns:
        IP address string or None if not found
    """
    cmd = [
        "gcloud", "compute", "instances", "describe",
        instance,
        "--zone", zone,
        "--project", project,
        "--format", "value(networkInterfaces[0].accessConfigs[0].natIP)"
    ]
    
    try:
        if quiet:
            # Run quietly without printing command
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        else:
            result = run_command(cmd, check=True)
        
        ip = result.stdout.strip()
        # Filter out empty strings and "None" values
        if ip and ip.lower() != 'none':
            return ip
        return None
    except subprocess.CalledProcessError:
        return None


def load_deployment_status(config_path: Path = DEPLOYMENT_STATUS_CONFIG) -> Dict[str, Any]:
    """Load deployment status configuration from JSON file"""
    if not config_path.exists():
        # Create empty status file if it doesn't exist
        return {"targets": []}
    
    with open(config_path, 'r') as f:
        return json.load(f)


def save_deployment_status(status_data: Dict[str, Any], config_path: Path = DEPLOYMENT_STATUS_CONFIG) -> None:
    """Save deployment status configuration to JSON file"""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(status_data, f, indent=2)


def update_status_file(
    operation: str,
    zone: str,
    project: str,
    instance: str,
    status_path: Path = DEPLOYMENT_STATUS_CONFIG
) -> None:
    """
    Update deployment status file after start/stop operation
    
    Args:
        operation: 'start' or 'stop'
        zone: GCP zone
        project: GCP project ID
        instance: Instance name
        status_path: Path to deployment-status.json
    """
    status_data = load_deployment_status(status_path)
    targets = status_data.get('targets', [])
    
    # Find existing entry or create new one
    target_entry = None
    for target in targets:
        if (target.get('gcp_zone') == zone and
            target.get('gcp_project') == project and
            target.get('gcp_instance') == instance):
            target_entry = target
            break
    
    if target_entry is None:
        # Create new entry
        target_entry = {
            'gcp_zone': zone,
            'gcp_project': project,
            'gcp_instance': instance,
            'status': 'stopped',
            'port': 5001
        }
        targets.append(target_entry)
    
    if operation == 'stop':
        # Update status to stopped and remove IP
        target_entry['status'] = 'stopped'
        target_entry.pop('ip', None)
        print(f"  Updated status: {instance} -> stopped (IP removed)")
    elif operation == 'start':
        # Update status to running and fetch IP
        target_entry['status'] = 'running'
        print(f"  Fetching IP address for {instance}...")
        ip = get_instance_ip(zone, project, instance)
        if ip:
            target_entry['ip'] = ip
            print(f"  Updated status: {instance} -> running (IP: {ip})")
        else:
            print(f"  Warning: Could not fetch IP address for {instance}")
            target_entry.pop('ip', None)
    
    # Ensure port is set (default 5001)
    if 'port' not in target_entry:
        target_entry['port'] = 5001
    
    # Save updated status
    status_data['targets'] = targets
    save_deployment_status(status_data, status_path)


def refresh_status_file(
    zone: str,
    project: str,
    instance: str,
    status_path: Path = DEPLOYMENT_STATUS_CONFIG
) -> None:
    """
    Refresh deployment status file by checking actual VM status and IP
    
    Args:
        zone: GCP zone
        project: GCP project ID
        instance: Instance name
        status_path: Path to deployment-status.json
    """
    status_data = load_deployment_status(status_path)
    targets = status_data.get('targets', [])
    
    # Find existing entry or create new one
    target_entry = None
    for target in targets:
        if (target.get('gcp_zone') == zone and
            target.get('gcp_project') == project and
            target.get('gcp_instance') == instance):
            target_entry = target
            break
    
    if target_entry is None:
        # Create new entry
        target_entry = {
            'gcp_zone': zone,
            'gcp_project': project,
            'gcp_instance': instance,
            'status': 'stopped',
            'port': 5001
        }
        targets.append(target_entry)
    
    # Check actual VM status
    print(f"  Checking status of {instance}...")
    actual_status = get_instance_status(zone, project, instance)
    
    if actual_status is None:
        print(f"  Warning: Could not determine status for {instance}")
        return
    
    # Normalize status (RUNNING -> running, STOPPED -> stopped, etc.)
    normalized_status = actual_status.lower()
    if normalized_status == 'running':
        target_entry['status'] = 'running'
        # Fetch IP if running
        print(f"  Fetching IP address for {instance}...")
        ip = get_instance_ip(zone, project, instance)
        if ip:
            target_entry['ip'] = ip
            print(f"  Updated: {instance} -> running (IP: {ip})")
        else:
            print(f"  Updated: {instance} -> running (no IP found)")
            target_entry.pop('ip', None)
    else:
        # For stopped, terminated, etc.
        target_entry['status'] = normalized_status
        target_entry.pop('ip', None)
        print(f"  Updated: {instance} -> {normalized_status} (IP removed)")
    
    # Ensure port is set (default 5001)
    if 'port' not in target_entry:
        target_entry['port'] = 5001
    
    # Save updated status
    status_data['targets'] = targets
    save_deployment_status(status_data, status_path)


def load_deployment_config(config_path: Path = DEPLOYMENT_CONFIG) -> List[Dict[str, Any]]:
    """Load deployment configuration from JSON file"""
    if not config_path.exists():
        raise FileNotFoundError(f"Deployment config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config.get('targets', [])


def manage_all_vms(operation: str, config_path: Path = DEPLOYMENT_CONFIG) -> None:
    """
    Start/stop all VMs from deployment.json
    
    Args:
        operation: 'start' or 'stop'
        config_path: Path to deployment.json config file
    """
    print(f"\n{'='*60}")
    print(f"{operation.capitalize()}ing All VMs from Deployment Config")
    print(f"{'='*60}")
    print(f"Loading config from: {config_path}")
    
    targets_config = load_deployment_config(config_path)
    
    if not targets_config:
        print("No targets found in deployment config")
        return
    
    # Collect all instances
    all_instances = []
    for target_config in targets_config:
        zone = target_config.get('gcp_zone')
        project = target_config.get('gcp_project')
        instances = target_config.get('gcp_instances', [])
        
        if not zone or not project or not instances:
            print(f"Warning: Skipping invalid target config: {target_config}")
            continue
        
        for instance in instances:
            all_instances.append({
                'zone': zone,
                'project': project,
                'instance': instance
            })
    
    if not all_instances:
        print("No valid instances found")
        return
    
    print(f"\nFound {len(all_instances)} instance(s) to {operation}:")
    for inst in all_instances:
        print(f"  - {inst['instance']} ({inst['zone']}, {inst['project']})")
    print()
    
    # Perform operation on each instance
    results = []
    for i, inst in enumerate(all_instances, 1):
        print(f"\n[{i}/{len(all_instances)}] {operation.capitalize()}ing {inst['instance']}...")
        try:
            gcloud_instance_operation(
                operation=operation,
                zone=inst['zone'],
                project=inst['project'],
                instance=inst['instance']
            )
            # Update status file after successful operation
            try:
                update_status_file(
                    operation=operation,
                    zone=inst['zone'],
                    project=inst['project'],
                    instance=inst['instance']
                )
            except Exception as e:
                print(f"  Warning: Failed to update status file: {e}", file=sys.stderr)
            
            results.append((inst, True, None))
            print(f"✓ Successfully {operation}ed {inst['instance']}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to {operation} {inst['instance']}: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((inst, False, error_msg))
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((inst, False, error_msg))
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"{operation.capitalize()} Summary")
    print(f"{'='*60}")
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total instances: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print(f"Successfully {operation}ed:")
        for inst, success, _ in results:
            if success:
                print(f"  ✓ {inst['instance']} ({inst['zone']}, {inst['project']})")
    
    if failed > 0:
        print(f"\nFailed to {operation}:")
        for inst, success, error in results:
            if not success:
                print(f"  ✗ {inst['instance']}: {error}")
    
    if failed > 0:
        sys.exit(1)


def manage_specific_vms(
    operation: str,
    zone: str,
    project: str,
    instances: List[str]
) -> None:
    """
    Start/stop specific VMs (1 zone, 1 project, multiple instance ids)
    
    Args:
        operation: 'start' or 'stop'
        zone: GCP zone
        project: GCP project ID
        instances: List of instance names
    """
    print(f"\n{'='*60}")
    print(f"{operation.capitalize()}ing Specific VMs")
    print(f"{'='*60}")
    print(f"Zone: {zone}")
    print(f"Project: {project}")
    print(f"Instances: {', '.join(instances)}")
    print()
    
    if not instances:
        print("No instances specified")
        return
    
    # Perform operation on each instance
    results = []
    for i, instance in enumerate(instances, 1):
        print(f"\n[{i}/{len(instances)}] {operation.capitalize()}ing {instance}...")
        try:
            gcloud_instance_operation(
                operation=operation,
                zone=zone,
                project=project,
                instance=instance
            )
            # Update status file after successful operation
            try:
                update_status_file(
                    operation=operation,
                    zone=zone,
                    project=project,
                    instance=instance
                )
            except Exception as e:
                print(f"  Warning: Failed to update status file: {e}", file=sys.stderr)
            
            results.append((instance, True, None))
            print(f"✓ Successfully {operation}ed {instance}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to {operation} {instance}: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((instance, False, error_msg))
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((instance, False, error_msg))
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"{operation.capitalize()} Summary")
    print(f"{'='*60}")
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total instances: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print(f"Successfully {operation}ed:")
        for instance, success, _ in results:
            if success:
                print(f"  ✓ {instance}")
    
    if failed > 0:
        print(f"\nFailed to {operation}:")
        for instance, success, error in results:
            if not success:
                print(f"  ✗ {instance}: {error}")
    
    if failed > 0:
        sys.exit(1)


def refresh_all_vms(config_path: Path = DEPLOYMENT_CONFIG) -> None:
    """
    Refresh status and IP of all VMs from deployment.json
    
    Args:
        config_path: Path to deployment.json config file
    """
    print(f"\n{'='*60}")
    print("Refreshing All VMs from Deployment Config")
    print(f"{'='*60}")
    print(f"Loading config from: {config_path}")
    
    targets_config = load_deployment_config(config_path)
    
    if not targets_config:
        print("No targets found in deployment config")
        return
    
    # Collect all instances
    all_instances = []
    for target_config in targets_config:
        zone = target_config.get('gcp_zone')
        project = target_config.get('gcp_project')
        instances = target_config.get('gcp_instances', [])
        
        if not zone or not project or not instances:
            print(f"Warning: Skipping invalid target config: {target_config}")
            continue
        
        for instance in instances:
            all_instances.append({
                'zone': zone,
                'project': project,
                'instance': instance
            })
    
    if not all_instances:
        print("No valid instances found")
        return
    
    print(f"\nFound {len(all_instances)} instance(s) to refresh:")
    for inst in all_instances:
        print(f"  - {inst['instance']} ({inst['zone']}, {inst['project']})")
    print()
    
    # Refresh each instance
    results = []
    for i, inst in enumerate(all_instances, 1):
        print(f"\n[{i}/{len(all_instances)}] Refreshing {inst['instance']}...")
        try:
            refresh_status_file(
                zone=inst['zone'],
                project=inst['project'],
                instance=inst['instance']
            )
            results.append((inst, True, None))
            print(f"✓ Successfully refreshed {inst['instance']}")
        except Exception as e:
            error_msg = f"Failed to refresh {inst['instance']}: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((inst, False, error_msg))
    
    # Print summary
    print(f"\n{'='*60}")
    print("Refresh Summary")
    print(f"{'='*60}")
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total instances: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print("Successfully refreshed:")
        for inst, success, _ in results:
            if success:
                print(f"  ✓ {inst['instance']} ({inst['zone']}, {inst['project']})")
    
    if failed > 0:
        print("\nFailed to refresh:")
        for inst, success, error in results:
            if not success:
                print(f"  ✗ {inst['instance']}: {error}")
    
    if failed > 0:
        sys.exit(1)


def refresh_specific_vms(
    zone: str,
    project: str,
    instances: List[str]
) -> None:
    """
    Refresh status and IP of specific VMs (1 zone, 1 project, multiple instance ids)
    
    Args:
        zone: GCP zone
        project: GCP project ID
        instances: List of instance names
    """
    print(f"\n{'='*60}")
    print("Refreshing Specific VMs")
    print(f"{'='*60}")
    print(f"Zone: {zone}")
    print(f"Project: {project}")
    print(f"Instances: {', '.join(instances)}")
    print()
    
    if not instances:
        print("No instances specified")
        return
    
    # Refresh each instance
    results = []
    for i, instance in enumerate(instances, 1):
        print(f"\n[{i}/{len(instances)}] Refreshing {instance}...")
        try:
            refresh_status_file(
                zone=zone,
                project=project,
                instance=instance
            )
            results.append((instance, True, None))
            print(f"✓ Successfully refreshed {instance}")
        except Exception as e:
            error_msg = f"Failed to refresh {instance}: {e}"
            print(f"✗ {error_msg}", file=sys.stderr)
            results.append((instance, False, error_msg))
    
    # Print summary
    print(f"\n{'='*60}")
    print("Refresh Summary")
    print(f"{'='*60}")
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total instances: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print("Successfully refreshed:")
        for instance, success, _ in results:
            if success:
                print(f"  ✓ {instance}")
    
    if failed > 0:
        print("\nFailed to refresh:")
        for instance, success, error in results:
            if not success:
                print(f"  ✗ {instance}: {error}")
    
    if failed > 0:
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Manage GCP VM instances (start/stop/refresh)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start all VMs from deployment.json
  %(prog)s start --all

  # Stop all VMs from deployment.json
  %(prog)s stop --all

  # Refresh status and IP of all VMs from deployment.json
  %(prog)s refresh --all

  # Start specific VMs
  %(prog)s start --zone us-central1-c --project my-project --instances instance-1 instance-2

  # Stop specific VMs
  %(prog)s stop --zone us-central1-c --project my-project --instances instance-1 instance-2

  # Refresh specific VMs
  %(prog)s refresh --zone us-central1-c --project my-project --instances instance-1 instance-2
        """
    )
    
    parser.add_argument(
        'operation',
        choices=['start', 'stop', 'refresh'],
        help='Operation to perform: start, stop, or refresh'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Start/stop/refresh all VMs from deployment.json config'
    )
    
    parser.add_argument(
        '--zone',
        type=str,
        help='GCP zone (required for specific VMs)'
    )
    
    parser.add_argument(
        '--project',
        type=str,
        help='GCP project ID (required for specific VMs)'
    )
    
    parser.add_argument(
        '--instances',
        nargs='+',
        help='Instance names (required for specific VMs, can specify multiple)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=str(DEPLOYMENT_CONFIG),
        help=f'Path to deployment config file (default: {DEPLOYMENT_CONFIG})'
    )
    
    args = parser.parse_args()
    
    if args.operation == 'refresh':
        # Refresh operation
        if args.all:
            config_path = Path(args.config)
            refresh_all_vms(config_path)
        else:
            if not args.zone or not args.project or not args.instances:
                parser.error("--zone, --project, and --instances are required when not using --all")
            
            refresh_specific_vms(
                zone=args.zone,
                project=args.project,
                instances=args.instances
            )
    elif args.all:
        # Manage all VMs from config
        config_path = Path(args.config)
        manage_all_vms(args.operation, config_path)
    else:
        # Manage specific VMs
        if not args.zone or not args.project or not args.instances:
            parser.error("--zone, --project, and --instances are required when not using --all")
        
        manage_specific_vms(
            operation=args.operation,
            zone=args.zone,
            project=args.project,
            instances=args.instances
        )


if __name__ == "__main__":
    main()

