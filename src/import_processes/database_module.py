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
#
# module: databaseModule.py
# function: process()
# synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
# author: Will Raymond <farmfreshsoftware@gmail.com>

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.message_app import add_message

# process-level properties and references shared across process app functions (def) 
from apis.properties_process import DatabaseModule as mod

# Color Class used app-wide for Message Readability in console
# from apis.color_class import color

import pymysql
# Define specific MySQL error codes for conditional handling
# Example error codes: 1045 (Access denied), 1062 (Duplicate entry), 1146 (No such table)
# You might need to adjust these based on your specific error handling needs.
ERROR_ACCESS_DENIED = 1045
ERROR_NO_SUCH_TABLE = 1146

def process(parms):

    mod.set_defaults()

    display_log = parms.get("print")
    module_name = parms.get("module_name")
    module_parm1 = parms.get("module_parm1")
    
    mod.cursor = app.dbConnection.cursor()

    try:
        mod.cursor.callproc(module_name,
                            [module_parm1,
                            str(app.importProcessID)])

    except pymysql.Error as e:
        mod.error_count += 1
        add_message( 0, e , __name__ , type(e).__name__ ,  e)

        error_code = e.args[0]
        error_message = e.args[1]
        print(f"Error : Stored Procedure : {module_name} Parms : {module_parm1} - Code {error_code} - {error_message}")


        # Conditional handling based on the specific error
        if error_code == ERROR_NO_SUCH_TABLE:
            #print(f"Error: Table does not exist. Breaking loop.")
            # Rollback any pending transaction before breaking
            # app.dbConnection.rollback() 
            return False # break # Stop all processing immediately

        elif error_code == ERROR_ACCESS_DENIED:
            #print(f"Error: Access denied. Continuing to the next file.")
            # Rollback current transaction and continue
            # app.dbConnection.rollback()
            return True #continue # Skip the current file and move to the next iteration

        else:
            #print(f"An unexpected error occurred. Continuing to the next file.")
             # app.dbConnection.rollback()
             return True #continue # Skip the current file and move to the next iteration

    except Exception as e:
        error_count += 1
        add_message( 0, f"Stored Procedure : {module_name} with Parms : {module_parm1} failed", __name__ , type(e).__name__ , e)

    app.dbConnection.commit()

    return mod.process_report()
