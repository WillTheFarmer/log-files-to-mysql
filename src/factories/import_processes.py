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
# module: import_processes.py
# function: get_import_process()
# synopsis: handles off the proper process to import load execution for logFiles2MySQL application.
# author: Will Raymond <farmfreshsoftware@gmail.com>

# application-level error handle
from apis.message_app import add_message

from src.import_processes.data_file_loader import process as data_file_loader_process
from src.import_processes.database_module import process as database_module_process
from src.import_processes.data_enrichment_geoIP import process as data_enrichment_geoIP_process
from src.import_processes.data_enrichment_userAgent import process as data_enrichment_userAgent_process

# The registry maps process types to loader functions
LOADER_REGISTRY = {
    'data_file_loader': data_file_loader_process,
    'database_module': database_module_process,
    'data_enrichment_geoIP': data_enrichment_geoIP_process,
    'data_enrichment_userAgent': data_enrichment_userAgent_process
}

def get_import_process(import_server_process):
# Factory method to retrieve the correct data loader based on process type name.
    loader = LOADER_REGISTRY.get(import_server_process)
    if not loader:
        add_message( 0, f"Unknown Import Process: {import_server_process}", {__name__})

    return loader
