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
# module: dataEnrichment_geoIP.py
# function: process()
# synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
# author: Will Raymond <farmfreshsoftware@gmail.com>

# application-level properties and references shared across app modules (files) 
from apis.properties_app import app

# application-level error handle
from apis.message_app import add_message

# process-level properties and references shared across process app functions (def) 
from apis.properties_process import DataEnrichmentGeoIP as mod

# Color Class used app-wide for Message Readability in console
from apis.color_class import color

# GeoIP worker
import geoip2.database

# used for to check if geodatabases exist
from os import path

# used to remove \\ from paths
from os import sep

import MySQLdb

def process(parms):

    mod.set_defaults( parms.get("id") , __name__ )

    display_log = parms.get("print")
    geoip_city = parms.get("city")
    geoip_asn = parms.get("asn")
    
    # mod.cursor is a property used to share cursor between def()s
    # mod.cursor = app.dbConnection.cursor()
      
    geoip_city_file_exists = True
    geoip_asn_file_exists = True

    if '\\' in geoip_city:
      geoip_city_file = geoip_city.replace(sep, sep+sep)
    else:
      geoip_city_file = geoip_city

    if '\\' in geoip_asn:
      geoip_asn_file = geoip_asn.replace(sep, sep+sep)
    else:
      geoip_asn_file = geoip_asn

    if not path.exists(geoip_city_file):
        geoip_city_file_exists = False
        mod.warning_count += 1
        add_message( 6, f"GeoIP City database {geoip_city_file} not found", __name__ )

    if not path.exists(geoip_asn_file):
        geoip_asn_file_exists = False
        mod.warning_count += 1
        add_message( 7, f"GeoIP ASN database {geoip_city_file} not found", __name__ )

    if geoip_city_file_exists and geoip_asn_file_exists:

        selectCursor = app.dbConnection.cursor()
        updateCursor = app.dbConnection.cursor()

        try:
            selectCursor.execute("SELECT id, name FROM log_client WHERE country_code IS NULL")

        except Exception as e:
            mod.warning_count += 1
            add_message( 2, e , __name__ , type(e).__name__ ,  e)

        try:
            cityReader = geoip2.database.Reader(geoip_city_file)

        except Exception as e:
            mod.warning_count += 1
            add_message( 3, e , __name__ , type(e).__name__ ,  e)

        try:
            asnReader = geoip2.database.Reader(geoip_asn_file)

        except Exception as e:
            mod.warning_count += 1
            add_message( 4, e , __name__ , type(e).__name__ ,  e)

        for x in range(selectCursor.rowcount):
            mod.records_processed += 1
            geoipRec = selectCursor.fetchone()
            recID = str(geoipRec[0])
            ipAddress = geoipRec[1]
            country_code = ''
            country = ''
            subdivision = ''
            city = ''
            latitude = 0.0
            longitude = 0.0
            organization = ''
            network = ''

            if display_log >= 2:
                print(f"{color.fg.CYAN}{color.style.DIM}Retrieving data for IP Address | {ipAddress}{color.END}")

            try:

                cityData = cityReader.city(ipAddress)

                if cityData.country.iso_code is not None:
                    country_code = cityData.country.iso_code
                    country_code = country_code.replace('"', ' ')
                    country_code = country_code.replace("'", ' ')

                if cityData.country.name is not None:
                    country = cityData.country.name
                    country = country.replace('"', ' ')
                    country = country.replace("'", ' ')

                if cityData.city.name is not None:
                    city = cityData.city.name
                    city = city.replace('"', ' ')
                    city = city.replace("'", ' ')

                if cityData.subdivisions.most_specific.name is not None:
                    subdivision = cityData.subdivisions.most_specific.name
                    subdivision = subdivision.replace('"', ' ')
                    subdivision = subdivision.replace("'", ' ')

                if cityData.location.latitude is not None:
                    latitude = cityData.location.latitude

                if cityData.location.longitude is not None:
                    longitude = cityData.location.longitude

            except Exception as e:
                mod.warning_count += 1
                add_message( 9, e , __name__ , type(e).__name__ ,  e)

            try:
                asnData = asnReader.asn(ipAddress)

                if asnData.autonomous_system_organization is not None:
                    organization = asnData.autonomous_system_organization
                    organization = organization.replace('"', ' ')
                    organization = organization.replace("'", ' ')

                asnData_network = asnData.network

                if asnData_network is not None:
                    network = str(asnData_network)

            except Exception as e:
                asnData = None
                network = str(e.network)
                mod.warning_count += 1
                add_message( 8, f"asnReader IP : {ipAddress}", __name__ , type(e).__name__ , e )

            updateSql = f"UPDATE log_client SET country_code = '{country_code}', " \
                        f"country = '{country}' , " \
                        f"subdivision = '{subdivision}' , " \
                        f"city = '{city}' , " \
                        f"latitude = {latitude} , " \
                        f"longitude = {longitude} , " \
                        f"organization = '{organization}' , " \
                        f"network = '{network}' " \
                        f" WHERE id = {recID};"

            try:
                updateCursor.execute(updateSql)

            except MySQLdb.Error as e:
                mod.error_count += 1
                add_message( 0, e , __name__ , type(e).__name__ ,  e)

            except Exception as e:
                mod.warning_count += 1
                sql_message = f"sql : {updateSql} - {e}"
                add_message( 0, sql_message, __name__ , type(e).__name__ ,  e)

        app.dbConnection.commit()
        selectCursor.close()
        updateCursor.close()

        # UPDATE import_process table processing metrics
        mod.update_import_process()

    return mod.process_report()
