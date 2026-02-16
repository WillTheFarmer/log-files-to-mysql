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
# CHANGELOG.md in repository - https://github.com/WillTheFarmer/files-to-mysql
#
# module: datFileLoader.py
# function: process_file()
# synopsis: each file is processed here. This is where LOAD DATA is done.
# function: process()
# synopsis: loops through files in parameterized directory and calls process_file().
# author: Will Raymond <farmfreshsoftware@gmail.com>

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.message_app import add_message

# process-level properties and references shared across process app functions (def) 
from apis.properties_process import DataFileLoader as mod

# Color Class used app-wide for Message Readability in console
from apis.color_class import color

# used process execution time calculations and displays
from time import ctime
from time import perf_counter
from datetime import datetime

# used for getctime, getmtime, get sise for extracting file properties to store in import_file
from os import path

# used to remove \\ from paths
from os import sep

from glob import glob

import MySQLdb

from src.apis.utilities import copy_backup_file

# this new design uses 'format properties' as LOAD DATA string components to assemble to foster code re-use for all log formats.
# module needs to be refined and tested yet. It was a rushed release due to other stuff but I wanted to get the re-design out.
# The LOAD DATA string building happens here. this was lots of duplicate code between the 5 formats. 
# It has been refined down to normalization of assembling the LOAD DATA string based on the variables:
# mod.load_table - MYSQL staging table
# mod.log_format - the FIELD substring of the LOAD DATA string
# mod.log_server - this enables attaching domains and ports to log files of logFormats that do not contain host data.
# mod.log_server_port - same as above but for the port
#
# days_since_imported - calculated in the importFileID() function. The days since the file was INSERTed into the import_file TABLE
# 
# Define specific MySQL error codes for conditional handling - this is work is progress
# Example error codes: 1045 (Access denied), 1062 (Duplicate entry), 1146 (No such table)
ERROR_ACCESS_DENIED = 1045
ERROR_NO_SUCH_TABLE = 1146

def process_file(rawFile):

    if '\\' in rawFile:
        loadFile = rawFile.replace(sep, sep+sep)
    else:
        loadFile = rawFile

    # MySQL function importFilesExists returns number of days since file was INSERTED into TABLE import_file. 
    # value used in combination with config.json backup_days and backup_path settings to trigger:
    #  1) COPY to backup directory and DELETE file from current directory. 2)just DELETE file or 3) do NOTHING
    days_since_importedSQL = f"SELECT importFileExists('{loadFile}', '{app.importDeviceID}');"

    try:
        mod.cursor.execute( days_since_importedSQL )
        days_since_importedTuple = mod.cursor.fetchall()
        days_since_imported = days_since_importedTuple[0][0]

    except Exception as e:
        mod.error_count += 1
        add_message( 0, e , __name__ , type(e).__name__ ,  e)

    if days_since_imported is None:

        if app.error_details:
            print(f"load_table : {color.fg.GREEN}{mod.load_table}{color.END} " \
                  f"log_format : {color.fg.GREEN}{mod.log_format}{color.END} " \
                  f"server_name : {color.fg.GREEN}{mod.log_server}{color.END} " \
                  f"server_port : {color.fg.GREEN}{mod.log_server_port}{color.END} " \
                  f"loadFile : {color.fg.GREEN}{loadFile}{color.END}" \
                  f"days_since_imported : {color.fg.GREEN}{days_since_imported}{color.END}")

        mod.files_processed += 1

        if mod.display_log >= 2:
            print(f"Loading file | {rawFile}")

        fileInsertCreated = ctime(path.getctime(rawFile))
        fileInsertModified = ctime(path.getmtime(rawFile))
        fileInsertSize = str(path.getsize(rawFile))

        fileInsertSQL = f"SELECT importFileID('{loadFile}', '{fileInsertSize}', '{fileInsertCreated}', '{fileInsertModified}', '{app.importDeviceID}', '{app.importLoadID}', '5' );"
        try:
            mod.cursor.execute( fileInsertSQL )
            fileInsertTupleID = mod.cursor.fetchall()
            fileInsertFileID = fileInsertTupleID[0][0]

        except Exception as e:
            print(f"load_table : {mod.load_table} log_format : {mod.log_format} server_name : {mod.log_server} server_port : {mod.log_server_port} loadFile : {loadFile}")
            mod.error_count += 1
            add_message( 0, e , __name__ , type(e).__name__ ,  e)

        # LOAD DATA SQL String
        fileLoadSQL = ""
        
        #  SQL String Component variables - in order
        fileLoadSQL_tables = ""
        fileLoadSQL_format = ""
        fileLoadSQL_importFileID = ""
        fileLoadSQL_serverInfo = ""

        # build LOAD DATA string - it all depends on log format being setup below - app settings (config.json)
        if app.error_details:
            print(f"load_table : {mod.load_table} log_format : {mod.log_format} server_name : {mod.log_server} server_port : {mod.log_server_port} loadFile : {loadFile}")

        if mod.log_format=="apache_error":
          fileLoadSQL_format = " FIELDS TERMINATED BY ']' ESCAPED BY '\r'"

        elif mod.log_format=="nginx_error":
          fileLoadSQL_format = " FIELDS TERMINATED BY ']' ESCAPED BY '\r'"

        elif mod.log_format=="apache_common" or mod.log_format=="apache_combined" or mod.log_format=="apache_vhost":
            fileLoadSQL_format = " FIELDS TERMINATED BY ' ' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\r'"

        elif mod.log_format=="apache_csv2mysql":
            fileLoadSQL_format = " FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\r'"

        elif mod.log_format=="nginx_default":
            fileLoadSQL_format = " FIELDS TERMINATED BY ' ' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\r'"

        elif mod.log_format=="nginx_csv2mysql":
            fileLoadSQL_format = " FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\r'"

        else:
            mod.error_count += 1
            add_message( 0, f"Process Log Format={mod.log_format} not found", __name__ )

        if fileLoadSQL_format:
            # format is excepted - based on other app settings (config.json) figure out if server info components required for LOAD DATA string build
            fileLoadSQL_tables = f"LOAD DATA LOCAL INFILE '{loadFile}' INTO TABLE {mod.load_table}"

            # import_file TABLE Primary ID - this relates TEXT FILES to RELATIONAL TABLE DATA 
            fileLoadSQL_importFileID = f" SET importfileid={fileInsertFileID}"

            # if the string is set check is server and server port are populated. If YES add the string
            if mod.log_server and mod.log_server_port:
                 fileLoadSQL_serverInfo = f", server_name='{mod.log_server}', server_port={mod.log_server_port}"

            elif mod.log_server:
                 fileLoadSQL_serverInfo = f", server_name='{mod.log_server}'"

            # build LOAD DATA string
            fileLoadSQL = f"{fileLoadSQL_tables}{fileLoadSQL_format}{fileLoadSQL_importFileID}{fileLoadSQL_serverInfo}"

            if app.error_details:
                print(f"fileLoadSQL : {fileLoadSQL}")

            try:
                mod.cursor.execute( fileLoadSQL )
                mod.cursor.execute( "SELECT ROW_COUNT()" )
                fileRecordsLoadedTuple = mod.cursor.fetchall()
                fileRecordsLoaded = fileRecordsLoadedTuple[0][0]
                mod.records_processed = mod.records_processed + fileRecordsLoaded

            except MySQLdb.Error as e:
                mod.error_count += 1
                add_message( 0, e , __name__ , type(e).__name__ ,  e)

    elif mod.backup_days != 0:
        copy_backup_file(rawFile, days_since_imported)

    return

def process(parms):

    mod.set_defaults( parms.get("id") , __name__ )

    # shared application-level connection for any database message logging done during file copy process.
    mod.cursor = app.dbConnection.cursor()

    mod.backup_days = parms.get("backup_days")
    
    mod.log_format = parms.get("log_format")
    mod.load_table = parms.get("load_table")
    mod.log_path = parms.get("path")
    mod.log_recursive = parms.get("recursive")
    mod.display_log = parms.get("print")
    mod.log_server = parms.get("server")
    mod.log_server_port = parms.get("server_port")
    
    # watchDog observers pass each file as a parameter. 
    # if log_file is passed - call process_file directly.
    log_file = parms.get("log_file")
    if app.error_details and log_file:
        print(f"File passed : {log_file}")

    if log_file:
        mod.files_found += 1
        process_file(log_file)
    else:        
        for rawFile in glob(mod.log_path, recursive=mod.log_recursive):

            filename = path.basename(rawFile)

            if app.error_details:
                print(f"Processing file: {filename}")

            mod.files_found += 1

            try:
              fileStatus = process_file(rawFile)
              if app.error_details:
                  if fileStatus:
                      print(f"Status for {filename}: {fileStatus}")
                  else:
                      print(f"No record found for {filename}")

            except MySQLdb.Error as e:
                add_message( 0, __name__ , type(e).__name__ , e )
                mod.error_count += 1

        # Commit changes if the loop completes without a breaking error
        else:
            app.dbConnection.commit()
            if mod.display_log >= 2:
                print("All files processed successfully (or continued past errors). Changes committed.")

    # UPDATE import_process table processing metrics
    mod.update_import_process()

    return mod.process_report()
