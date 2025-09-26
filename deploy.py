#!/usr/bin/env python3

import subprocess
import sys
import os
import re

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    print(f"Running: {description or cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    # Change to project directory
    project_dir = "/Users/barrysolomon/Projects/solar_monitor"
    os.chdir(project_dir)
    
    # Get current build number
    with open('src/version.py', 'r') as f:
        content = f.read()
    
    build_match = re.search(r"'build':\s*(\d+)", content)
    if not build_match:
        print("❌ Could not find build number in src/version.py")
        return False
    
    current_build = int(build_match.group(1))
    new_build = current_build + 1
    
    print(f"Current build: {current_build}")
    print(f"New build: {new_build}")
    
    # Update build number
    new_content = re.sub(r"'build':\s*\d+", f"'build': {new_build}", content)
    with open('src/version.py', 'w') as f:
        f.write(new_content)
    
    # Get new version string
    sys.path.insert(0, 'src')
    from version import get_version_string
    new_version = get_version_string()
    print(f"New version: {new_version}")
    
    # Pre-deployment syntax checks
    print("🔍 Running pre-deployment checks...")
    
    files_to_check = [
        'web_dashboard_cached_simple.py',
        'src/version.py', 
        'src/mobile_api.py'
    ]
    
    for file in files_to_check:
        if not run_command(f"python3 -m py_compile {file}", f"Checking syntax of {file}"):
            print("❌ Syntax check failed!")
            return False
    
    print("✅ All syntax checks passed")
    
    # Deploy files
    print(f"Deploying {new_version}...")
    
    deploy_commands = [
        ("scp web_dashboard_cached_simple.py barry@192.168.1.126:/opt/solar_monitor/", "Copying main dashboard"),
        ("scp src/version.py barry@192.168.1.126:/opt/solar_monitor/src/", "Copying version system"),
        ("scp src/mobile_api.py barry@192.168.1.126:/opt/solar_monitor/src/", "Copying mobile API"),
        ("scp -r static/ barry@192.168.1.126:/opt/solar_monitor/", "Copying static files"),
    ]
    
    for cmd, desc in deploy_commands:
        if not run_command(cmd, desc):
            print("❌ Deployment failed!")
            return False
    
    # Post-deployment verification
    print("🔍 Verifying deployment on server...")
    if not run_command('ssh barry@192.168.1.126 "cd /opt/solar_monitor && python3 -m py_compile web_dashboard_cached_simple.py"', "Server-side syntax check"):
        print("❌ Server-side verification failed!")
        return False
    
    print("✅ Server-side syntax verification passed")
    
    # Restart service
    if not run_command('ssh barry@192.168.1.126 "sudo systemctl restart solar-monitor.service"', "Restarting service"):
        print("❌ Service restart failed!")
        return False
    
    print(f"✅ Deployment complete: {new_version}")
    print("🌐 Access at: http://192.168.1.126:5000")
    print("📱 Mobile API: http://192.168.1.126:5000/api/mobile/version")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
