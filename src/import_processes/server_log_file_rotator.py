import os
import signal
import subprocess
import time
from datetime import datetime

def rotate_log_files(log_dir="/var/log/nginx", old_dir="/var/log/nginx_rotation"):
    """
    Implements 'In-Place' rotation:
    1. Rename active logs to a processing name.
    2. Signal NGINX to re-open fresh log files.
    3. Finalize name for Watchdog/MySQL ingestion.
    """
    # 1. Create rotation directory if it doesn't exist
    if not os.path.exists(old_dir):
        os.makedirs(old_dir)

    # 2. Identify logs to rotate (e.g., access.log, error.log)
    active_logs = [f for f in os.listdir(log_dir) if f.endswith('.log')]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    processing_files = []

    for log_file in active_logs:
        src = os.path.join(log_dir, log_file)
        # Temporary name while NGINX still has the file handle open
        dst_tmp = os.path.join(old_dir, f"{log_file}.{timestamp}.tmp")
        
        try:
            os.rename(src, dst_tmp)
            # process in separate process
            # processing_files.append((dst_tmp, log_file))
        except OSError as e:
            print(f"Error moving {log_file}: {e}")

    # 3. Signal NGINX to reopen log files (The USR1 Signal)
    # This is safer than 'nginx -s reload' as it doesn't drop connections
    try:
        # Standard way to find PID and send USR1
        # Equivalent to: kill -USR1 $(cat /run/nginx.pid)
        subprocess.run(["nginx", "-s", "reopen"], check=True)
        # Small sleep to ensure NGINX has released old file handles
        time.sleep(1) 
    except subprocess.CalledProcessError:
        print("Failed to signal NGINX. Ensure script has sudo/root permissions.")

    # 4. Finalize names to trigger Watchdog events in old_dir
    for tmp_path, original_name in processing_files:
        final_path = tmp_path.replace(".tmp", "")
        os.rename(tmp_path, final_path)
        print(f"Rotated: {original_name} -> {os.path.basename(final_path)}")

if __name__ == "__main__":
    rotate_log_files()
