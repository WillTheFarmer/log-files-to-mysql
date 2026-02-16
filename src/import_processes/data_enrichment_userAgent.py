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
# module: dataEnrichment_userAgent.py
# function: process()
# synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
# author: Will Raymond <farmfreshsoftware@gmail.com>

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.message_app import add_message

# process-level properties and references shared across process app functions (def) 
from apis.properties_process import DataEnrichmentUserAgent as mod

# Color Class used app-wide for Message Readability in console
from apis.color_class import color

# user-agents worker 
from user_agents import parse

import MySQLdb

def process(parms):

    mod.set_defaults( parms.get("id") , __name__ )

    display_log = parms.get("print")
    app.cursor = app.dbConnection.cursor()

    selectCursor = app.dbConnection.cursor()
    updateCursor = app.dbConnection.cursor()

    try:
        selectCursor.execute("SELECT id, name FROM access_log_useragent WHERE ua_browser IS NULL")

    except Exception as e:
        mod.error_count += 1
        add_message( 0, e , __name__ , type(e).__name__ ,  e)

    for x in range(selectCursor.rowcount):

        mod.records_processed += 1

        userAgent = selectCursor.fetchone()

        recID = str(userAgent[0])
        ua = parse(userAgent[1])

        if display_log >= 2:
            print(f"{color.fg.CYAN}{color.style.DIM}Parsing User Agent | {ua}{color.END}")
            strua = str(ua)
            strua = strua.replace('"', ' in.') # must replace " in string for error occurs
            br = str(ua.browser)  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
            br = br.replace('"', ' in.') # must replace " in string for error occurs
            br_family = str(ua.browser.family)  # returns 'Mobile Safari'
            br_family = br_family.replace('"', ' in.') # must replace " in string for error occurs

            #ua.browser.version  # returns (5, 1)
            br_version = ua.browser.version_string   # returns '5.1'
            br_version = br_version.replace('"', ' in.') # must replace " in string for error occurs

            # Accessing user agent's operating system properties
            os_str = str(ua.os)  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
            os_str = os_str.replace('"', ' in.') # must replace " in string for error occurs
            os_family = str(ua.os.family)  # returns 'iOS'
            os_family = os_family.replace('"', ' in.') # must replace " in string for error occurs

            #ua.os.version  # returns (5, 1)
            os_version = ua.os.version_string  # returns '5.1'
            os_version = os_version.replace('"', ' in.') # must replace " in string for error occurs
            # Accessing user agent's device properties

            dv = str(ua.device)  # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
            dv = dv.replace('"', ' in.') # must replace " in string for error occurs

            dv_family = str(ua.device.family)  # returns 'iPhone'
            dv_family = dv_family.replace('"', ' in.') # must replace " in string for error occurs

            dv_brand = str(ua.device.brand) # returns 'Apple'
            dv_brand = dv_brand.replace('"', ' in.') # must replace " in string for error occurs

            dv_model = str(ua.device.model) # returns 'iPhone'
            dv_model = dv_model.replace('"', ' in.') # must replace " in string for error occurs

            updateSql = f"UPDATE access_log_useragent SET ua='{strua}', " \
                        f"ua_browser='{br}', " \
                        f"ua_browser_family='{br_family}', " \
                        f"ua_browser_version='{br_version}', " \
                        f"ua_os='{os_str}', " \
                        f"ua_os_family'{os_family}', " \
                        f"ua_os_version='{os_version}', " \
                        f"ua_device='{dv}', " \
                        f"ua_device_family='{dv_family}', " \
                        f"ua_device_brand='{dv_brand}', " \
                        f"ua_device_model='{dv_model}' " \
                        f" WHERE id={recID}"

            try:
                updateCursor.execute(updateSql)

            except Exception as e:
                mod.error_count += 1
                add_message( 0, e , __name__ , type(e).__name__ ,  e)

    app.dbConnection.commit()

    selectCursor.close()

    updateCursor.close()

    # UPDATE import_process table processing metrics
    mod.update_import_process()

    return mod.process_report()
