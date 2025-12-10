#!/usr/bin/env python3
"""
Local orchestrator that distributes category crawling to remote workers
"""

import argparse
import json
import logging
import os
import sys
import time
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
import requests

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from utils.db_connector import DatabaseConnection, load_categories, get_target_categories

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LocalOrchestrator:
    """Orchestrates category crawling across remote workers"""
    
    def __init__(self, asin_dir: str, deployment_status_file: str = None, max_product_per_category: Optional[int] = None):
        """
        Initialize orchestrator
        
        Args:
            asin_dir: Directory containing amazon_asin_*.json files
            deployment_status_file: Path to deployment-status.json file
            max_product_per_category: Maximum number of ASINs to process per category (None = all)
        """
        self.asin_dir = os.path.abspath(asin_dir)
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load deployment status
        if deployment_status_file is None:
            deployment_status_file = os.path.join(
                os.path.dirname(__file__), '..', 'config', 'deployment-status.json'
            )
        self.deployment_status_file = deployment_status_file
        self.workers = self._load_workers()
        
        # Store max_product_per_category
        self.max_product_per_category = max_product_per_category
        
        # Worker state: worker_id -> {'request_id': int, 'category': dict, 'status': str}
        self.worker_states = {}
        for i in range(len(self.workers)):
            self.worker_states[i] = {
                'request_id': None,
                'category': None,
                'status': 'idle'
            }
        
        # Categories to process
        self.categories_queue = []
        self.completed_categories = []
        
    def _setup_logging(self):
        pass
        
    def _load_workers(self) -> List[Dict[str, Any]]:
        """Load remote workers from deployment-status.json"""
        if not os.path.exists(self.deployment_status_file):
            raise FileNotFoundError(f"Deployment status file not found: {self.deployment_status_file}")
        
        with open(self.deployment_status_file, 'r') as f:
            data = json.load(f)
        
        workers = []
        for target in data.get('targets', []):
            if target.get('status') == 'running':
                workers.append({
                    'ip': target['ip'],
                    'port': target['port'],
                    'url': f"http://{target['ip']}:{target['port']}"
                })
        
        if not workers:
            raise ValueError("No running workers found in deployment-status.json")
        
        logger.info(f"Loaded {len(workers)} remote workers")
        for i, worker in enumerate(workers, 1):
            logger.info(f"  Worker {i}: {worker['url']}")
        
        return workers
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize category name for filename"""
        safe = name.replace(' ', '_').replace("'", '').replace('"', '')
        safe = ''.join(c for c in safe if c.isalnum() or c in ('_', '-'))
        return safe.lower()
    
    def _get_asin_file_path(self, category_name: str) -> Optional[str]:
        """Get path to ASIN file for a category"""
        safe_name = self._sanitize_filename(category_name)
        filename = f"amazon_asin_{safe_name}.json"
        filepath = os.path.join(self.asin_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        return None
    
    def load_categories_from_db(self, category_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Load categories from database
        
        Args:
            category_names: Optional list of category names to load. If None, loads all categories.
        
        Returns:
            List of category dictionaries
        """
        if category_names:
            logger.info(f"Loading {len(category_names)} specified categories from database...")
        else:
            logger.info("Loading all categories from database...")
        
        try:
            with DatabaseConnection() as cursor:
                if category_names:
                    categories = get_target_categories(cursor, category_names)
                    logger.info(f"Loaded {len(categories)} categories from database")
                else:
                    categories_dict = load_categories(cursor)
                    categories = list(categories_dict.values())
                    logger.info(f"Loaded {len(categories)} categories from database")
                return categories
        except Exception as e:
            logger.error(f"Failed to load categories from database: {e}")
            return []
    
    def prepare_categories_queue(self, categories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare queue of categories that have ASIN files"""
        queue = []
        
        for category in categories:
            category_name = category['name']
            asin_file = self._get_asin_file_path(category_name)
            
            if asin_file:
                # Load ASINs
                try:
                    with open(asin_file, 'r', encoding='utf-8') as f:
                        asins = json.load(f)
                    
                    if isinstance(asins, list) and len(asins) > 0:
                        # Limit ASINs if max_product_per_category is set
                        original_count = len(asins)
                        if self.max_product_per_category is not None and self.max_product_per_category > 0:
                            asins = asins[:self.max_product_per_category]
                            if len(asins) < original_count:
                                logger.info(
                                    f"Limited ASINs for {category_name}: {original_count} -> {len(asins)} "
                                    f"(max_product_per_category={self.max_product_per_category})"
                                )
                        
                        queue.append({
                            'category': category,
                            'asin_file': asin_file,
                            'asins': asins
                        })
                        logger.debug(f"Found ASIN file for {category_name}: {len(asins)} ASINs")
                    else:
                        logger.warning(f"ASIN file for {category_name} is empty or invalid")
                except Exception as e:
                    logger.warning(f"Error reading ASIN file for {category_name}: {e}")
            else:
                logger.debug(f"No ASIN file found for {category_name}")
        
        logger.info(f"Prepared {len(queue)} categories with ASIN files for processing")
        return queue
    
    def start_scraping(self, worker_id: int, category_data: Dict[str, Any]) -> Optional[int]:
        """
        Start scraping on a remote worker
        
        Args:
            worker_id: Index of worker in self.workers
            category_data: Category data with 'category', 'asins'
            
        Returns:
            request_id if successful, None otherwise
        """
        worker = self.workers[worker_id]
        category = category_data['category']
        asins = category_data['asins']
        
        url = urljoin(worker['url'], '/v1/scrapes/start')
        
        payload = {
            'category_id': category['id'],
            'site': 'amazon',
            'asins': asins,
            'category_name': category['name']
        }
        
        try:
            logger.info(f"[Worker {worker_id+1}] Starting scraping for category: {category['name']} ({len(asins)} ASINs)")
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            request_id = data.get('request_id')
            
            if request_id:
                self.worker_states[worker_id]['request_id'] = request_id
                self.worker_states[worker_id]['category'] = category_data
                self.worker_states[worker_id]['status'] = 'in_progress'
                logger.info(f"[Worker {worker_id+1}] Started request_id={request_id} for {category['name']}")
                return request_id
            else:
                logger.error(f"[Worker {worker_id+1}] No request_id in response: {data}")
                return None
                
        except Exception as e:
            logger.error(f"[Worker {worker_id+1}] Error starting scraping: {e}")
            return None
    
    def get_status(self, worker_id: int) -> Optional[Dict[str, Any]]:
        """Get status of current request on a worker"""
        worker = self.workers[worker_id]
        request_id = self.worker_states[worker_id]['request_id']
        
        if not request_id:
            return None
        
        url = urljoin(worker['url'], f'/v1/scrapes/{request_id}/status')
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"[Worker {worker_id+1}] Error getting status: {e}")
            return None
    
    def download_result(self, worker_id: int, request_id: int) -> bool:
        """Download result file from worker"""
        worker = self.workers[worker_id]
        url = urljoin(worker['url'], f'/v1/scrapes/{request_id}/download')
        
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save zip file
            zip_path = os.path.join(self.output_dir, f"scrape_{request_id}.zip")
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.output_dir)
            
            # Remove zip file
            os.remove(zip_path)
            
            logger.info(f"[Worker {worker_id+1}] Downloaded and extracted result for request_id={request_id}")
            return True
            
        except Exception as e:
            logger.error(f"[Worker {worker_id+1}] Error downloading result: {e}")
            return False
    
    def download_logs(self, worker_id: int, request_id: int) -> bool:
        """Download logs from worker"""
        worker = self.workers[worker_id]
        url = urljoin(worker['url'], f'/v1/scrapes/{request_id}/logs')
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save log file
            log_path = os.path.join(self.output_dir, f"{request_id}.log")
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            logger.info(f"[Worker {worker_id+1}] Downloaded logs for request_id={request_id}")
            return True
            
        except Exception as e:
            logger.error(f"[Worker {worker_id+1}] Error downloading logs: {e}")
            return False
    
    def monitor_worker(self, worker_id: int):
        """Monitor a worker's current request"""
        state = self.worker_states[worker_id]
        
        if state['status'] != 'in_progress':
            return
        
        status_data = self.get_status(worker_id)
        if not status_data:
            return
        
        status = status_data.get('status')
        request_id = state['request_id']
        category_name = state['category']['category']['name']
        
        if status in ['completed', 'stopped', 'failed']:
            # Log final status
            processed = status_data.get('processed_count', 0)
            total = status_data.get('total_count', 0)
            success = status_data.get('success_count', 0)
            failed = status_data.get('failed_count', 0)
            
            logger.info(
                f"[Worker {worker_id+1}] Request {request_id} ({category_name}): "
                f"{status.upper()} - {processed}/{total} processed ({success} success, {failed} failed)"
            )
            
            if status == 'failed':
                message = status_data.get('message', 'Unknown error')
                logger.error(f"[Worker {worker_id+1}] Failure message: {message}")
                # Download logs
                self.download_logs(worker_id, request_id)
            
            # Download result if completed or stopped
            if status in ['completed', 'stopped']:
                self.download_result(worker_id, request_id)
            
            # Mark category as completed
            self.completed_categories.append(state['category'])
            
            # Reset worker state
            state['request_id'] = None
            state['category'] = None
            state['status'] = 'idle'
            
        else:
            # Log progress
            processed = status_data.get('processed_count', 0)
            total = status_data.get('total_count', 0)
            success = status_data.get('success_count', 0)
            failed = status_data.get('failed_count', 0)
            progress_pct = (processed / total * 100) if total > 0 else 0
            
            logger.info(
                f"[Worker {worker_id+1}] Request {request_id} ({category_name}): "
                f"{status} - {processed}/{total} ({progress_pct:.1f}%) - "
                f"{success} success, {failed} failed"
            )
    
    def assign_next_category(self, worker_id: int) -> bool:
        """Assign next category from queue to a worker"""
        if not self.categories_queue:
            return False
        
        category_data = self.categories_queue.pop(0)
        request_id = self.start_scraping(worker_id, category_data)
        
        return request_id is not None
    
    def run(self, category_names: Optional[List[str]] = None):
        """
        Run the orchestrator
        
        Args:
            category_names: Optional list of category names to process. If None, processes all categories.
        """
        logger.info("=" * 80)
        logger.info("LOCAL ORCHESTRATOR - DISTRIBUTING TO REMOTE WORKERS")
        logger.info("=" * 80)
        
        if category_names:
            logger.info(f"Processing specified categories: {', '.join(category_names)}")
        else:
            logger.info("Processing all categories")
        
        if self.max_product_per_category:
            logger.info(f"Max products per category: {self.max_product_per_category}")
        else:
            logger.info("Max products per category: unlimited (all ASINs)")
        
        # Load categories from database
        categories = self.load_categories_from_db(category_names)
        if not categories:
            logger.error("No categories loaded from database")
            return
        
        # Prepare categories queue
        self.categories_queue = self.prepare_categories_queue(categories)
        if not self.categories_queue:
            logger.error("No categories with ASIN files found")
            return
        
        total_categories = len(self.categories_queue)
        logger.info(f"Total categories to process: {total_categories}")
        
        # Start initial assignments
        for worker_id in range(len(self.workers)):
            if self.categories_queue:
                self.assign_next_category(worker_id)
        
        # Main monitoring loop
        logger.info("\nStarting monitoring loop...")
        start_time = datetime.now()
        
        while True:
            # Check all workers
            all_idle = True
            for worker_id in range(len(self.workers)):
                state = self.worker_states[worker_id]
                
                if state['status'] == 'in_progress':
                    all_idle = False
                    self.monitor_worker(worker_id)
                elif state['status'] == 'idle' and self.categories_queue:
                    # Assign next category
                    if self.assign_next_category(worker_id):
                        all_idle = False
            
            # Check if we're done
            if all_idle and not self.categories_queue:
                break
            
            # Wait before next check
            time.sleep(5)
        
        # Final summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("\n" + "=" * 80)
        logger.info("ORCHESTRATION COMPLETED")
        logger.info("=" * 80)
        logger.info(f"Duration: {duration}")
        logger.info(f"Total categories processed: {len(self.completed_categories)}/{total_categories}")
        logger.info(f"Results saved to: {self.output_dir}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Local orchestrator for remote scraping workers')
    parser.add_argument(
        '--asin-dir',
        type=str,
        required=True,
        help='Directory containing amazon_asin_*.json files'
    )
    parser.add_argument(
        '--deployment-status',
        type=str,
        default=None,
        help='Path to deployment-status.json file (default: ../config/deployment-status.json)'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        default=None,
        help='List of category names to process (e.g., "Laptop" "Smartphone"). If not specified, processes all categories.'
    )
    parser.add_argument(
        '--max-product-per-category',
        type=int,
        default=None,
        help='Maximum number of ASINs to process per category. If not specified, processes all available ASINs.'
    )
    
    args = parser.parse_args()
    
    orchestrator = LocalOrchestrator(
        asin_dir=args.asin_dir,
        deployment_status_file=args.deployment_status,
        max_product_per_category=args.max_product_per_category
    )
    
    orchestrator.run(category_names=args.categories)


if __name__ == '__main__':
    main()

