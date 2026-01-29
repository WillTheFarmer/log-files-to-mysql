# Copyright 2024-2026 Will Raymond <farmfreshsoftware@gmail.com>
#
# Licensed under the http License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.http.org/licenses/LICENSE-2.0
#
# version 4.0.1 - 01/24/2026 - Proper Python code, NGINX format support and Python/SQL repository separation - see changelog
#
# CHANGELOG.md in repository - https://github.com/WillTheFarmer/http-logs-to-mysql
#
# Processes Apache & NGINX logs into normalized MySQL schema for httpLogs2MySQL application.
# module: main.py
# function: process_files()
# module: import_processes.py
# function: get_import_process()
# module: datFileLoader.py
# function: process()
# module: databaseModule.py
# function: process()
# module: dataEnrichment_geoIP.py
# function: process()
# module: dataEnrichment_userAgent.py
# function: process()
# synopsis: main:process_files (import_load table) executes child processes (import_process table) & watchdog observers defined in config.json.
# author: Will Raymond <farmfreshsoftware@gmail.com>
# Refinement updates will be frequent.  

# used for app.expandUser
from os import path

# used to ID computer process is running on.
from os import getlogin
from platform import processor
from platform import uname
from socket import gethostbyname
from socket import gethostname
from apis.device_id import get_device_id

# this handles the 4 modules - fileLoader, dbModuleExecutor, UserAgent module & GeoIP module.
from src.factories.import_processes import get_import_process

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.error_app import add_error

# Color Class used app-wide for Message Readability in console
from apis.color_class import color

# used process execution time calculations and displays
# from time import ctime
from time import perf_counter
from datetime import datetime

# Used to display dictionary lists.
from tabulate import tabulate

# config.json drives application loading import processes and watchDog observers. 
from config.config_app import load_file

# most import function for Import Primary IDs
from apis.table_id import get_table_id

# used EXIT if missing required IDs : app.importDeviceID, app.importClientID and app.importLoadID    
import sys

# all starts here - json process file must exist - nothing works without it
config = load_file()
if config:
    app.ipaddress = gethostbyname(gethostname())
    app.deviceid = get_device_id()
    app.login = getlogin( )
    app.expandUser = path.expanduser('~')
    
    tuple_uname = uname()
    platformSystem = tuple_uname[0]
    platformNode = tuple_uname[1]
    
    app.platformRelease = tuple_uname[2]
    app.platformVersion = tuple_uname[3]
    app.platformMachine = tuple_uname[4]
    app.platformProcessor = processor()

    # settings for shared functions
    app.backup_days = config["backup"].get("days")
    app.backup_path = config["backup"].get("path")

    app.host_name = config["mysql"].get("host")
    app.host_port = config["mysql"].get("port")

    app.mysql = config.get("mysql")

    # Two options for shared database connection to help install issues
    # and separate connction data from JSON app process settings.  
    # Option 1 - pymysql_env.py uses .env file for connection settings 
    #from src.database.pymysql_env import get_connection
    # Option 2 - pymysql_json.py uses config.json file for connection settings
    from src.database.pymysql_json import get_connection

def update_importProcess(data):

    # update import_process record ID = app.importProcessID
    if data.get("ProcessErrors") == 0: 
       """ update import_process.completed = now() """

    #print(f"UPDATE import_process with {data} where id = {app.importProcessID}")

def execute_process(process):
    # process info to feed to processes
    moduleName  = process.get("moduleName")
    processParms = process["attributes"]

    processInfo = {}

    # used for calcuations and log messaging to main:process_files
    app.executeStart = perf_counter()

    if processParms.get("print") >= 1:
        print(f"{color.fg.GREEN}{color.style.NORMAL}Start{color.END} | " \
              f"{process.get("name")} | {datetime.now():%Y-%m-%d %H:%M:%S} | " \
              f"{color.fg.GREEN}{color.style.NORMAL}App execution: {app.executeStart - app.processStart:.4f} seconds.{color.END}")

    try:
        # gererate new primary ID for import_process table
        # each Import Load Child process gets ID. Stored Procudures UPDATE record totals with ID.
        app.importProcessID = get_table_id("process")

        # Use the factory to get the appropriate loader
        importProcess = get_import_process(moduleName)
        #gererate new primary ID for import_process table

        try:
            # import process does work are all modules return the same data list []
            data = importProcess(processParms)

            if data:
                app.executeSeconds = perf_counter() - app.executeStart

                # print(data)
        
                update_importProcess(data)

                # print(data)
                # add import process information for summary report
                processInfo = {"importProcessID": app.importProcessID, "executeSeconds": app.executeSeconds}
                processInfo.update(data)
            else:
                print(f"There is a problem - data: {data}")

        except Exception as e:
            add_error({__name__},{type(e).__name__}, {e}, e)
            #print(f"Error processing {process.get("name")}: {e}")
            return None

        if processParms.get("print") >= 1:
          print(f"{color.fg.GREENI}{color.style.NORMAL}End{color.END} | " \
                f"{process.get('name')} | {color.fg.GREENI}{color.style.NORMAL}Process ID: {processInfo.get('importProcessID'):.4f} | " \
                f"{processInfo.get('Files Loaded')} files loaded | time: {processInfo.get('executeSeconds'):.4f} seconds{color.END}")

        # return dictionary {} to main:process_files for process_list to append for Import Load summary log message
        return processInfo

    except ValueError as e:
        add_error({__name__},{type(e).__name__}, {e}, e)

    except FileNotFoundError:
        add_error({__name__},{type(e).__name__}, {e}, e)

def process_files(process_list=[]):
    # display console message log header
    print (f"{color.fg.YELLOW}{color.style.BRIGHT}ProcessLogs start: {datetime.now():%Y-%m-%d %H:%M:%S} | Host: {app.host_name} | Port: {app.host_port}{color.END}") 

    # reset application-level calcualtion properties
    app.errorCount = 0
    app.processStart = perf_counter()
    app.processSeconds = 0 

    # shared connection for all app modules
    app.dbConnection = get_connection()
    # shared cursor for app-level functions
    app.cursor = app.dbConnection.cursor()

    # if any of the 3 MySQL function calls fail process is aborted 
    app.importDeviceID = get_table_id("device")
    app.importClientID = get_table_id("client")
    app.importLoadID = get_table_id("load")

    if app.errorCount > 0:
        print("Error has already occurred and nothing was done yet!")
        sys.exit(1) # Exit with error code 1

    app.dbConnection.commit()     
    # list for process execution information summary report
    log_processes = []

    # starting collection to filter.A Parameter can be passed - process_list - List[] of processids for flexibility.
    allProcesses = config['processes']

    # the default filter - if process_list is EMPTY - only processes with status = "Active"
    # filtering options are endless. watchDog Observers pass List[] of processid to execute in the order to execute.
    log_file = ""

    if not process_list:
        filteredProcesses = [logformat for logformat in allProcesses if logformat['status'] == 'Active']
    else:
        listItems = len(process_list)
        # print(f"Process List: {process_list} with count of {len(process_list)}")
        # get the file and path to process. 
        log_file = process_list[listItems-1]
        # this removes the file to be processed. 
        process_list.pop(-1)
        # print(f"Process Filter: {process_list} with count of {len(process_list)} - file: {log_file}")
        filteredProcesses = [process for process in allProcesses if process["id"] in process_list]

    for process in filteredProcesses:
        if log_file:
            process["attributes"]["log_file"] = log_file

        processInfo = {"id": process.get("id"), "Module": process.get("moduleName")}
   
        try:
            data = execute_process(process)
            # print(data)
            # add process information for summary report
            if data:
                processInfo.update(data)
                log_processes.append(processInfo)
    
        except Exception as e:
            add_error({__name__},{type(e).__name__}, {e}, e)
            # print(f"Error processing {processInfo}: {e}")
            # break  # Exit the loop entirely on error
            continue  # Or skip this process and move to next

    loadUpdateSQL = f"UPDATE import_load SET errorCount={app.errorCount}, completed=now(), processSeconds={app.processSeconds} WHERE id={app.importLoadID}"

    try:
        app.cursor.execute(loadUpdateSQL)

    except Exception as e:
        app.errorCount += 1
        add_error({__name__},{type(e).__name__}, {e}, e)

    # commit and close 
    app.dbConnection.commit()
    app.cursor.close()

    # clear reference for shared connection
    app.dbConnection.close()
    app.dbConnection = None
 
    # Calculate the elapsed time
    app.processSeconds = perf_counter() - app.processStart            

    # Summary Report - import load process list display
    # List of all processes that executed with totals. 
    # import_load & import_load_process tables have parent and child data records.
    # Print report header
    print(f"{color.fg.GREEN}{color.style.NORMAL}Import Load Summary | Log File & Record Counts and Process Metrics | " \
          f"ImportLoadID: {app.importLoadID} | " \
          f"ClientID: {app.importClientID} | " \
          f"DeviceID:{app.importDeviceID} | " \
          f"Errors Found:{app.errorCount} | " \
          f"Host: {app.host_name} | Port: {app.host_port}{color.END}")

    # The 'keys' header option automatically uses dictionary keys as column headers
    print(tabulate(log_processes, headers='keys', tablefmt='github'))

    # Print summary bottom
    print(f"{color.fg.GREEN}{color.style.NORMAL}" \
          f"ImportLoadID: {app.importLoadID} | " \
          f"{app.errorCount} Errors Found | Import Load Summary Values added to import_load TABLE{color.END}")
   
    # Print report footer
    print(f"{color.fg.YELLOW}{color.style.BRIGHT}ProcessLogs complete: {datetime.now():%Y-%m-%d %H:%M:%S} | " \
          f"Execution time: {app.processSeconds:.4f} seconds{color.END}")
    # Print application footer
    print(f"{color.fg.GREEN}{color.style.NORMAL}httpLogs2MySQL application{color.END} | " \
          f"Import all Files in Folders: {color.fg.GREEN}{color.style.NORMAL}files_import.py{color.END} | " \
          f"Watch for new Files in Folders: {color.fg.GREEN}{color.style.NORMAL}files_watch.py{color.END} | " \
          f"Process & Observer Property Lists: {color.fg.GREEN}{color.style.NORMAL}config_lists.py{color.END}")
