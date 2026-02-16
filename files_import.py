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
"""
:script: files_import.py
:synopsis: Executes all active (status='Active') processes in config.json collection for logFiles2MySQL application.
:author: Will Raymond <farmfreshsoftware@gmail.com>
"""
from src import main
# parameters can be passed to process_files() for filtering child processes executed during parent Import Load. 
main.process_files()