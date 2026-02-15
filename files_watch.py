# Copyright 2024-2026 Will Raymond <farmfreshsoftware@gmail.com>
#
# Licensed under the http License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.http.org/licenses/LICENSE-2.0
#
# version 4.0.2 - 02/13/2026 - INT to BIGINT, PyMSQL to MySQLdb, mysql procedures for each server & format - see changelog
#
# CHANGELOG.md in repository - https://github.com/WillTheFarmer/http-logs-to-mysql
"""
:script: files_watch.py
:synopsis: Polls paths in config.json collection for logFiles2MySQL application. Event passes process_list & file to process_files() 
:author: Will Raymond <farmfreshsoftware@gmail.com>
"""
# To access a custom property of a watchdog event handler from your main While True loop, 
# you need to use a thread-safe method of inter-thread communication, such as a queue.Queue or a threading.Event. 
# The watchdog observer runs in its own background thread, so direct access to a modified property from the main 
# thread can lead to race conditions. 
# Solution using queue.Queue
# This approach allows the event handler to put events into a queue, which the main While True loop then safely processes.
# 
# Key Concepts
# queue.Queue: This is the recommended way to share information between threads in Python. 
# The put() and get() methods handle necessary locking to ensure data integrity.
# Observer as a separate thread: The observer.start() method launches the monitoring process in a new thread. 
# The main program continues to run in the primary thread, executing the while True loop.
# Custom Handler: The MyHandler class is instantiated with a reference to the shared queue, allowing it to 
# signal the main thread whenever a filesystem event occurs.
# time.sleep(): This prevents the while True loop from consuming excessive CPU resources (busy-waiting) by pausing periodically. 

from queue import Queue
from watchdog.observers import Observer
# subclassing this Class
from watchdog.events import FileSystemEventHandler
# config.json drives application loading import processes and watchDog observers 
from config.config_app import load_file
# Color Class used app-wide for Message Readability in console
from apis.color_class import color
# Used to display dictionary lists
from tabulate import tabulate
# time.sleep(1) in LOOP for rest to avoid busy-waiting
import time
# the application - process_files passed - processid list [] and src_path to execute. 
from src.main import process_files
# used to verify path exists
from pathlib import Path

class ProcessFile(FileSystemEventHandler):
    processFiles = 0
    def __init__(self, queue, process_list):
        super().__init__()
        self.queue = queue # Store the queue instance
        self.process_list = process_list #  List [] of processIDs - import processes to execute in series based on file type

    def on_created(self, event):
        if not event.is_directory:
            # Put the event information into the queue
            self.processFiles = 3
            self.process_list.append(event.src_path)
            self.queue.put(self.process_list)

    def on_modified(self, event):
        if not event.is_directory:
            # Put the event information into the queue
            self.processFiles = 2

    def on_any_event(self, event):
        if event.event_type == 'created' and event.is_directory == False:
            self.processFiles = 1
        #print(f"Event: {color.fg.REDI}{event.event_type}{color.END} File: {color.fg.REDI}{event.src_path}{color.END} Processes: {color.fg.REDI}{self.process_list}{color.END}")

if __name__ == "__main__":
    # Create a thread-safe queue
    event_queue = Queue()
    config = load_file()
    if config:
        watchdogObserver = Observer()
        observers_list = []
        attrValues = {}
        for observer in config['observers']:

            # print(f"Process List : {observer.get("process_list")}")
            observerInfo = {"Status": observer.get("status"),
                                "id": observer.get("id"),
                                "name": observer.get("name"),
                                "path": observer.get("path"),
                                "recursive": observer.get("recursive"),
                                "interval":  observer.get("interval"),
                                "process_list": observer.get("process_list")}

            file_path = Path(observer.get("path"))

            if file_path.exists():

                watch_log =  observer.get("print")
                watch_path = observer.get("path")
                watch_recursive = observer.get("recursive")
                watch_interval = observer.get("interval")
                watch_processes = observer.get("process_list")

                # print(f"watch_processes list: {watch_processes}")
                event_handler = ProcessFile(event_queue, watch_processes)
                watchdogObserver.schedule(event_handler, watch_path, recursive=watch_recursive)

                # display what is running
                observerInfo.update({"Watch": f"{color.fg.GREEN}Running{color.END}"})
            else:
                observerInfo.update({"Watch": f"{color.fg.RED}Error{color.END}"})
                print(f"The path '{file_path}' does not exist.")

            observers_list.append(observerInfo)

        watchdogObserver.start()
        print(f"{color.fg.GREEN}Observer List{color.fg.YELLOW} - Each record is a watchDog Observer Schedule. Each Observer executes associated import processes - {color.fg.RED}(process_list){color.END}")
        print(tabulate(observers_list, headers='keys', tablefmt='github'))

    try:
        # Main loop can safely access the queue
        while True:
            # Check queue for new events without blocking indefinitely
            if not event_queue.empty():
                event_data = event_queue.get()
                # print(f"Main loop processing event:{color.fg.REDI}{event_data}{color.END}")
                # Perform main business logic here
                process_files(event_data)
            time.sleep(1) # Sleep briefly to avoid busy-waiting
    except KeyboardInterrupt:
        # Gracefully stop the observer on KeyboardInterrupt
        watchdogObserver.stop()
    watchdogObserver.join() # Wait for the observer thread to finish
