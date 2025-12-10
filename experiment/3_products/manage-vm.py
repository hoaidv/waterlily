#!/usr/bin/env python3
"""
VM Management script for GCP instances
Start/stop all VMs from deployment.json or specific VMs
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


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Manage GCP VM instances (start/stop)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start all VMs from deployment.json
  %(prog)s start --all

  # Stop all VMs from deployment.json
  %(prog)s stop --all

  # Start specific VMs
  %(prog)s start --zone us-central1-c --project my-project --instances instance-1 instance-2

  # Stop specific VMs
  %(prog)s stop --zone us-central1-c --project my-project --instances instance-1 instance-2
        """
    )
    
    parser.add_argument(
        'operation',
        choices=['start', 'stop'],
        help='Operation to perform: start or stop'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Start/stop all VMs from deployment.json config'
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
    
    if args.all:
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

