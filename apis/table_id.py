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

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.message_app import add_message

import pymysql

def get_table_id(table):
    """
    # Import Process requires 4 Primary IDs from MySQL to start main:process_files
    # app will gracefully end with database premission issue error console message.
    #    
    Args:
        table (str): The name of the table to query.
        Must be one of "client", "device", "load" or "process"

        table - part of corresponding MySQL table name - "import_" + table

       Returns: returns new Primary ID for record INSERTed into TABLE

    """

   # centralized controlled function for App Primary IDs
    sql_queries = {
        "client": f"SELECT importClientID( '{app.ipaddress}', '{app.login}', '{app.expandUser}', '{app.platformRelease}', '{app.platformVersion}', '{app.importDeviceID}' );",
        "device": f"SELECT importDeviceID( '{app.deviceid}', '{app.platformNode}', '{app.platformSystem}', '{app.platformMachine}', '{app.platformProcessor}' );",
        "load": f"SELECT importLoadID( '{app.importClientID}' );",
        "process": f"SELECT importLoadProcessID( '{app.importLoadID}' );"
    }

    # Validate the input parameter
    if table not in sql_queries:
        raise ValueError(f"Invalid table parameter: '{table}'. Expected one of 'client', 'device', 'load', or 'process'.")

    # Get the specific SQL string for the valid table name
    sql_string = sql_queries[table]

    table_id = None
    try:
        app.cursor.execute( sql_string )

        result = app.cursor.fetchone()
            
        if result:
            # fetchone() returns a tuple, e.g., (123,)
            table_id = result[0]

        # print(f"SQL for '{table}': {sql_string}")

    except pymysql.Error as e:
        app.error_count += 1
        add_message( 0, e , __name__ , type(e).__name__ ,  e)

    except Exception as e:
        app.error_count += 1
        add_message( 0, e , __name__ , type(e).__name__ ,  e)
        
    #print(f"table {table} id = {table_id}")

    return table_id
