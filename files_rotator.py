class RotatorFactory:
    @staticmethod
    def get_rotator(server_type):
        if server_type == "nginx":
            return NginxRotator()
        elif server_type == "apache":
            return ApacheRotator()
        raise ValueError(f"Unknown server type: {server_type}")

# In your main execution loop:
for dataset in config['collections']:
    if dataset['status'] == "active" and dataset['rotator_enabled']:
        # This part runs on your schedule (15m, 60m, etc.)
        rotator = RotatorFactory.get_rotator(dataset['server_type'])
        
        # Rotator returns the list of finalized files
        rotated_files = rotator.execute(
            src=dataset['log_dir'], 
            dst=dataset['rotation_dir']
        )
        
        # Immediately pass the newly rotated files to your existing logic
        for file_path in rotated_files:
            process_files(file_path, dataset)


import time
import threading
from datetime import datetime
from src.main import process_files  # Your existing logic

def rotator_orchestrator(dataset_collection):
    """
    The background loop that manages timing for all domains.
    """
    while True:
        now = datetime.now()
        
        for dataset in dataset_collection:
            # Check if it's time to rotate (e.g., every 15 minutes)
            # Logic: If current minute is a multiple of interval_minutes
            if now.minute % dataset['interval_minutes'] == 0 and now.second < 10:
                print(f"[{now}] Triggering rotation for: {dataset['id']}")
                
                # 1. Execute Rotator Logic (Rename + USR1 Signal)
                # 2. Get list of new files
                rotated_files = perform_self_rotation(dataset) 
                
                # 3. Hand off to your main process
                for file_path in rotated_files:
                    process_files(file_path, dataset)
        
        # Sleep for a bit to avoid CPU spiking, 
        # then check again for the next interval
        time.sleep(30) 

# To run it without blocking your main application:
rotator_thread = threading.Thread(target=rotator_orchestrator, args=(my_datasets,), daemon=True)
rotator_thread.start()
