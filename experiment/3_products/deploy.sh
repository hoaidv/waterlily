#!/bin/bash
# Deployment script for GCP instance
# Deploys scraping server code and runs it

set -e  # Exit on error

# Configuration
GCP_ZONE="us-central1-c"
GCP_INSTANCE="instance-20251210-131952"
GCP_PROJECT="todaycreative-395514"
REMOTE_USER="${USER:-$(whoami)}"
REMOTE_DIR="~/waterlily-scraper"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"h

echo "=========================================="
echo "Deploying to GCP Instance"
echo "=========================================="
echo "Instance: ${GCP_INSTANCE}"
echo "Zone: ${GCP_ZONE}"
echo "Project: ${GCP_PROJECT}"
echo "Remote directory: ${REMOTE_DIR}"
echo ""

# Step 1: Connect and create remote directory
echo "Step 1: Setting up remote directory..."
gcloud compute ssh --zone "${GCP_ZONE}" "${GCP_INSTANCE}" --project "${GCP_PROJECT}" --command "
    mkdir -p ${REMOTE_DIR}
    echo 'Remote directory created'
"

# Step 2: Deploy code (excluding output* folders)
echo ""
echo "Step 2: Deploying code using gcloud compute scp..."
echo "Creating tar ball of source code..."
cd "${LOCAL_DIR}"
tar --exclude='output*' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='*.log' \
    -czf /tmp/waterlily-deploy.tar.gz .

echo "Copying tar ball to GCP instance..."
gcloud compute scp --zone "${GCP_ZONE}" --project "${GCP_PROJECT}" \
    /tmp/waterlily-deploy.tar.gz \
    "${GCP_INSTANCE}:/tmp/waterlily-deploy.tar.gz"

echo "Extracting tar ball on GCP instance..."
gcloud compute ssh --zone "${GCP_ZONE}" "${GCP_INSTANCE}" --project "${GCP_PROJECT}" --command "
    cd ${REMOTE_DIR}
    tar -xzf /tmp/waterlily-deploy.tar.gz
    rm /tmp/waterlily-deploy.tar.gz
    echo 'Code extracted'
"

rm /tmp/waterlily-deploy.tar.gz

# Step 3: Install system dependencies
echo ""
echo "Step 3: Installing system dependencies (pip3, python3-venv, unzip)..."
gcloud compute ssh --zone "${GCP_ZONE}" "${GCP_INSTANCE}" --project "${GCP_PROJECT}" --command "
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
"

# Step 4: Create virtual environment and install requirements
echo ""
echo "Step 4: Setting up virtual environment and installing Python requirements..."
gcloud compute ssh --zone "${GCP_ZONE}" "${GCP_INSTANCE}" --project "${GCP_PROJECT}" --command "
    cd ${REMOTE_DIR}
    
    # Create virtual environment if it doesn't exist
    if [ ! -d \"venv\" ]; then
        echo 'Creating virtual environment...'
        python3 -m venv venv
    else
        echo 'Virtual environment already exists'
    fi
    
    # Activate virtual environment and install requirements
    echo 'Activating virtual environment and installing requirements...'
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt || {
        echo 'Warning: Some packages may have failed to install'
    }
    echo 'Requirements installation completed'
    deactivate
"

# Step 5: Install Chrome and ChromeDriver for Selenium (if needed)
echo ""
echo "Step 5: Chrome and ChromeDriver will be automatically managed by webdriver-manager package. Skipping."

# Step 6: Run server
echo ""
echo "Step 6: Starting server..."
echo "Server will run on port 5001"
echo "To access: http://${GCP_INSTANCE}:5001"
echo ""

gcloud compute ssh --zone "${GCP_ZONE}" "${GCP_INSTANCE}" --project "${GCP_PROJECT}" --command "
    cd ${REMOTE_DIR}
    
    # Stop existing server if running
    echo 'Checking for existing server process...'
    
    # Kill process from server.pid if it exists
    if [ -f server.pid ]; then
        OLD_PID=\$(cat server.pid)
        if ps -p \$OLD_PID > /dev/null 2>&1; then
            echo 'Stopping existing server (PID: \$OLD_PID)...'
            kill \$OLD_PID || true
            sleep 2
            # Force kill if still running
            if ps -p \$OLD_PID > /dev/null 2>&1; then
                echo 'Force killing server process...'
                kill -9 \$OLD_PID || true
                sleep 1
            fi
        fi
        rm -f server.pid
    fi
    
    # Also check for any process using port 5001 and kill it
    # Try using lsof first, fallback to ss/fuser if lsof not available
    PORT_PID=\"\"
    if command -v lsof &> /dev/null; then
        PORT_PID=\$(lsof -ti:5001 2>/dev/null || true)
    elif command -v ss &> /dev/null; then
        PORT_PID=\$(ss -tlnp | grep ':5001' | grep -oP 'pid=\\K[0-9]+' | head -1 || true)
    elif command -v fuser &> /dev/null; then
        PORT_PID=\$(fuser 5001/tcp 2>/dev/null | awk '{print \$1}' || true)
    fi
    
    if [ ! -z \"\$PORT_PID\" ] && [ \"\$PORT_PID\" != \"-\" ]; then
        echo \"Found process using port 5001 (PID: \$PORT_PID), killing it...\"
        kill \$PORT_PID 2>/dev/null || true
        sleep 2
        if ps -p \$PORT_PID > /dev/null 2>&1; then
            echo 'Force killing process on port 5001...'
            kill -9 \$PORT_PID 2>/dev/null || true
            sleep 1
        fi
    fi
    
    # Activate virtual environment and start server
    echo 'Activating virtual environment and starting server...'
    source venv/bin/activate
    nohup python scrapers/server.py > server.log 2>&1 &
    echo \$! > server.pid
    deactivate
    
    sleep 2
    
    # Check if server started
    if [ -f server.pid ]; then
        PID=\$(cat server.pid)
        if ps -p \$PID > /dev/null 2>&1; then
            echo \"Server started successfully (PID: \$PID)\"
            echo \"Server logs: tail -f ${REMOTE_DIR}/server.log\"
        else
            echo 'Server failed to start. Check server.log for errors:'
            tail -20 server.log
            exit 1
        fi
    else
        echo 'Failed to create PID file'
        exit 1
    fi
"

echo ""
echo "=========================================="
echo "Deployment completed!"
echo "=========================================="
echo "Server is running on: http://${GCP_INSTANCE}:5001"
echo ""
echo "Useful commands:"
echo "  Check server status: gcloud compute ssh ${GCP_INSTANCE} --zone ${GCP_ZONE} --project ${GCP_PROJECT} --command 'ps -p \$(cat ${REMOTE_DIR}/server.pid)'"
echo "  View server logs: gcloud compute ssh ${GCP_INSTANCE} --zone ${GCP_ZONE} --project ${GCP_PROJECT} --command 'tail -f ${REMOTE_DIR}/server.log'"
echo "  Stop server: gcloud compute ssh ${GCP_INSTANCE} --zone ${GCP_ZONE} --project ${GCP_PROJECT} --command 'kill \$(cat ${REMOTE_DIR}/server.pid)'"
echo "  Restart server: gcloud compute ssh ${GCP_INSTANCE} --zone ${GCP_ZONE} --project ${GCP_PROJECT} --command 'cd ${REMOTE_DIR} && if [ -f server.pid ]; then kill \$(cat server.pid) 2>/dev/null || true; rm -f server.pid; fi; lsof -ti:5001 | xargs kill 2>/dev/null || true; source venv/bin/activate && nohup python scrapers/server.py > server.log 2>&1 & echo \$! > server.pid && deactivate'"
echo ""

