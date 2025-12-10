#!/usr/bin/env python3
"""
Scraping server API
Receives scraping requests and manages scraping jobs
"""

import json
import os
import sys
import threading
import time
import re
import zipfile
import io
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Flask, request, jsonify, send_file
import logging

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from scrapers.selenium_scraper import SeleniumAmazonScraper


app = Flask(__name__)

# Global state
jobs = {}  # request_id -> job_info
jobs_lock = threading.Lock()
request_id_counter = 0
request_id_lock = threading.Lock()

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_next_request_id() -> int:
    """Generate next request ID"""
    global request_id_counter
    with request_id_lock:
        request_id_counter += 1
        return request_id_counter


def load_config() -> Dict[str, Any]:
    """Load scraping configuration"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'scraping_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        'websites': ['amazon'],
        'rate_limiting': {
            'delay_range': [2.0, 4.0],
            'max_retries': 3,
            'timeout': 15
        },
        'output': {
            'directory': '../output'
        }
    }


def run_scraping_job(request_id: int, category_id: int, site: str, asins: List[str], category_name: str = None):
    """
    Run scraping job in background thread
    
    Args:
        request_id: Request ID
        category_id: Category ID
        site: Site name (e.g., 'amazon')
        asins: List of ASINs to scrape
        category_name: Optional category name
    """
    global jobs
    
    result_file = os.path.join(OUTPUT_DIR, f"{request_id}.json")
    log_file = os.path.join(OUTPUT_DIR, f"{request_id}.log")
    
    # Setup file logging for this job
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    job_logger = logging.getLogger(f'job_{request_id}')
    job_logger.addHandler(file_handler)
    job_logger.setLevel(logging.INFO)
    
    try:
        # Update job status
        with jobs_lock:
            jobs[request_id]['status'] = 'in_progress'
            jobs[request_id]['started_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            jobs[request_id]['log_file'] = log_file
        
        job_logger.info(f"Starting scraping job {request_id}")
        job_logger.info(f"Category ID: {category_id}, Site: {site}, ASINs: {len(asins)}")
        
        # Load config
        config = load_config()
        
        # Initialize scraper with headless mode enabled for server
        scraper = SeleniumAmazonScraper(config, output_dir=OUTPUT_DIR, headless=True)
        
        # Create category dict
        category = {
            'id': category_id,
            'name': category_name or f"Category {category_id}"
        }
        
        # Scrape products
        products = []
        success_count = 0
        failed_count = 0
        
        for idx, asin in enumerate(asins, 1):
            # Check if job was stopped
            with jobs_lock:
                if jobs[request_id]['status'] == 'stopped':
                    job_logger.info(f"Job stopped by user at ASIN {idx}/{len(asins)}")
                    break
            
            job_logger.info(f"Scraping product {idx}/{len(asins)}: ASIN {asin}")
            
            try:
                product_url = f"https://www.amazon.com/dp/{asin}"
                product_data = scraper.scrape_product_details(product_url, category)
                product_data['asin'] = asin
                
                if 'error' not in product_data:
                    success_count += 1
                    products.append(product_data)
                else:
                    failed_count += 1
                    job_logger.warning(f"Failed to scrape ASIN {asin}: {product_data.get('error')}")
                
                # Update progress
                with jobs_lock:
                    jobs[request_id]['success_count'] = success_count
                    jobs[request_id]['failed_count'] = failed_count
                    jobs[request_id]['processed_count'] = idx
                    jobs[request_id]['total_count'] = len(asins)
                
            except Exception as e:
                failed_count += 1
                job_logger.error(f"Error scraping ASIN {asin}: {e}")
                with jobs_lock:
                    jobs[request_id]['failed_count'] = failed_count
                    jobs[request_id]['processed_count'] = idx
        
        # Close scraper
        try:
            scraper.close()
        except:
            pass
        
        # Determine final status
        with jobs_lock:
            if jobs[request_id]['status'] == 'stopped':
                final_status = 'stopped'
                jobs[request_id]['stopped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                final_status = 'completed'
                jobs[request_id]['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            jobs[request_id]['status'] = final_status
            jobs[request_id]['success_count'] = success_count
            jobs[request_id]['failed_count'] = failed_count
            jobs[request_id]['processed_count'] = len(asins)
            jobs[request_id]['total_count'] = len(asins)
        
        # Save result file
        result_data = {
            'request_id': request_id,
            'started_at': jobs[request_id]['started_at'],
            'completed_at': jobs[request_id].get('completed_at'),
            'stopped_at': jobs[request_id].get('stopped_at'),
            'status': final_status,
            'success_count': success_count,
            'failed_count': failed_count,
            'processed_count': len(asins),
            'total_count': len(asins),
            'category_id': category_id,
            'category': category_name or f"Category {category_id}",
            'products': products
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        job_logger.info(f"Job {request_id} completed. Success: {success_count}, Failed: {failed_count}")
        
    except Exception as e:
        job_logger.error(f"Error in scraping job {request_id}: {e}")
        with jobs_lock:
            jobs[request_id]['status'] = 'failed'
            jobs[request_id]['error'] = str(e)
    finally:
        # Remove file handler
        job_logger.removeHandler(file_handler)
        file_handler.close()


@app.route('/v1/scrapes/start', methods=['POST'])
def start_scraping():
    '''
    Start scraping for provided category and ASINs. 
    Server does not know about our local database, it works with category_id and asins.
    Once the job is done, we download the result file. 

    One worker only. We can use selenium_scraper.py directly.

    - Save result to `./output/{request_id}.json`
    - Save log to `./output/{request_id}.log`

    POST /v1/scrapes/start 

    Request: 

    {
      "category_id": 1234,
      "site": "amazon",
      "asins": ["B000000000", "B000000001", "B000000002"]
    }

    Response: 

    {
      "message": "Scraping started",
      "status": "accepted",
      "request_id": 98234324
    }
    '''

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        category_id = data.get('category_id')
        site = data.get('site', 'amazon')
        asins = data.get('asins', [])
        category_name = data.get('category_name')
        
        if not category_id:
            return jsonify({'error': 'category_id is required'}), 400
        
        if not asins or not isinstance(asins, list):
            return jsonify({'error': 'asins must be a non-empty list'}), 400
        
        # Generate request ID
        request_id = get_next_request_id()
        
        # Initialize job
        with jobs_lock:
            jobs[request_id] = {
                'request_id': request_id,
                'category_id': category_id,
                'site': site,
                'asins': asins,
                'status': 'accepted',
                'success_count': 0,
                'failed_count': 0,
                'processed_count': 0,
                'total_count': len(asins),
                'started_at': None,
                'completed_at': None,
                'stopped_at': None
            }
        
        # Start scraping in background thread
        thread = threading.Thread(
            target=run_scraping_job,
            args=(request_id, category_id, site, asins, category_name),
            daemon=True
        )
        thread.start()
        
        logger.info(f"Started scraping job {request_id} for category {category_id} with {len(asins)} ASINs")
        
        return jsonify({
            'message': 'Scraping started',
            'status': 'accepted',
            'request_id': request_id
        }), 202
        
    except Exception as e:
        logger.error(f"Error starting scraping: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/v1/scrapes/<int:request_id>/status', methods=['GET'])
def get_status(request_id: int):
    '''
    Get the status of the scraping process by request id.

    GET /v1/scrapes/{request_id}/status

    Response: 

    - Inprogress (60%)

    {
      "message": "Scraping in progress",
      "status": "in_progress",
      "request_id": 98234324,
      "success_count": 50,
      "failed_count": 10,
      "processed_count": 60,
      "total_count": 100
    }

    - Completed:

    {
      "message": "Scraping completed",
      "status": "completed",
      "request_id": 98234324,
      "success_count": 80,
      "failed_count": 20,
      "processed_count": 100,
      "total_count": 100
    }
    '''
    with jobs_lock:
        if request_id not in jobs:
            return jsonify({'error': 'Request ID not found'}), 404
        
        job = jobs[request_id]
        
        if job['status'] == 'completed':
            message = 'Scraping completed'
        elif job['status'] == 'stopped':
            message = 'Scraping stopped'
        elif job['status'] == 'failed':
            message = f"Scraping failed: {job.get('error', 'Unknown error')}"
        else:
            message = 'Scraping in progress'
        
        response = {
            'message': message,
            'status': job['status'],
            'request_id': request_id,
            'success_count': job['success_count'],
            'failed_count': job['failed_count'],
            'processed_count': job['processed_count'],
            'total_count': job['total_count']
        }
        
        return jsonify(response), 200


@app.route('/v1/scrapes/<int:request_id>/stop', methods=['POST'])
def stop_scraping(request_id: int):
    '''
    Stop the scraping process by request id.

    POST /v1/scrapes/{request_id}/stop

    Request:

    {
      "reason": "User requested"
    }

    Response:

    {
      "message": "Scraping stopped",
      "code": "stopped",
      "request_id": 98234324,
      "success_count": 50,
      "failed_count": 10,
      "processed_count": 60,
      "total_count": 100
    }
    '''
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'User requested')
        
        with jobs_lock:
            if request_id not in jobs:
                return jsonify({'error': 'Request ID not found'}), 404
            
            job = jobs[request_id]
            
            if job['status'] in ['completed', 'stopped', 'failed']:
                return jsonify({
                    'error': f"Job already {job['status']}"
                }), 400
            
            job['status'] = 'stopped'
            job['stopped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            job['stop_reason'] = reason
        
        logger.info(f"Stopped scraping job {request_id}: {reason}")
        
        return jsonify({
            'message': 'Scraping stopped',
            'code': 'stopped',
            'request_id': request_id,
            'success_count': job['success_count'],
            'failed_count': job['failed_count'],
            'processed_count': job['processed_count'],
            'total_count': job['total_count']
        }), 200
        
    except Exception as e:
        logger.error(f"Error stopping scraping: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/v1/scrapes/<int:request_id>/download', methods=['GET'])
def download_result(request_id: int):
    '''
    File `./output/{request_id}.json` is zipped and downloaded, only when 
    status=completed|stopped

    GET /v1/scrapes/{request_id}/download

    Response:

    <Binary file>
    '''
    result_file = os.path.join(OUTPUT_DIR, f"{request_id}.json")
    
    with jobs_lock:
        if request_id not in jobs:
            return jsonify({'error': 'Request ID not found'}), 404
        
        job = jobs[request_id]
        
        if job['status'] not in ['completed', 'stopped']:
            return jsonify({
                'error': f"Job status is {job['status']}, cannot download. Status must be 'completed' or 'stopped'"
            }), 400
    
    if not os.path.exists(result_file):
        return jsonify({'error': 'Result file not found'}), 404
    
    # Create zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(result_file, os.path.basename(result_file))
    
    zip_buffer.seek(0)
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"scrape_{request_id}.zip"
    )


@app.route('/v1/scrapes/<int:request_id>/logs', methods=['GET'])
def get_logs(request_id: int):
    '''
    Use 1 of 3 ways to extract the log file by request id.
    - By line number range. If to is not provided, return all lines after from.
    - Tail the log file.
    - Grep the log file (line by line). 
      Also return line count for each grep result

    GET /v1/scrapes/{request_id}/logs?tail=1000&grep=<regex>&from=1000&to=2000

    Response:

    <Log file content>
    '''
    log_file = os.path.join(OUTPUT_DIR, f"{request_id}.log")
    
    with jobs_lock:
        if request_id not in jobs:
            return jsonify({'error': 'Request ID not found'}), 404
    
    if not os.path.exists(log_file):
        return jsonify({'error': 'Log file not found'}), 404
    
    # Get query parameters
    tail = request.args.get('tail', type=int)
    grep_pattern = request.args.get('grep')
    from_line = request.args.get('from', type=int)
    to_line = request.args.get('to', type=int)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Apply filters
        if grep_pattern:
            # Grep mode: return matching lines with line numbers
            matching_lines = []
            for line_num, line in enumerate(lines, 1):
                if re.search(grep_pattern, line):
                    matching_lines.append(f"{line_num}:{line}")
            return '\n'.join(matching_lines), 200, {'Content-Type': 'text/plain'}
        
        elif from_line is not None:
            # Line range mode
            start_idx = max(0, from_line - 1)
            if to_line is not None:
                end_idx = min(len(lines), to_line)
            else:
                end_idx = len(lines)
            selected_lines = lines[start_idx:end_idx]
            return ''.join(selected_lines), 200, {'Content-Type': 'text/plain'}
        
        elif tail is not None:
            # Tail mode
            selected_lines = lines[-tail:] if tail > 0 else lines
            return ''.join(selected_lines), 200, {'Content-Type': 'text/plain'}
        
        else:
            # Return all lines
            return ''.join(lines), 200, {'Content-Type': 'text/plain'}
    
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    logger.info("Starting scraping server...")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    app.run(host='0.0.0.0', port=5001, debug=False)



'''
Result file format (depends on the status)

{
  "request_id": 98234324,
  "started_at": "2025-01-01 12:00:00",
  "completed_at": "2025-01-02 12:00:00",
  "stopped_at": null,
  "status": "completed",
  "success_count": 80,
  "failed_count": 20,
  "processed_count": 100,
  "total_count": 100,
  "category_id": 177800,
  "category": "4K TVs",
  "products": [
    {
      "url": "...",
      "title": "...",
      "price": "...",
      "attributes": {
        ...
      }
    }
  ]
}
'''
