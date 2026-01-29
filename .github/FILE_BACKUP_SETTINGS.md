On servers, run application in conjunction with [logrotate](https://github.com/logrotate/logrotate) using [configuration file directives](https://man7.org/linux/man-pages/man8/logrotate.8.html) - `dateext`, `rotate`, `olddir`, `nocompress`, `notifempty`, `maxage`.
Set `WATCH_PATH` to same folder as `olddir` and configure logrotate to delete files.

On centralized computers, environment variables - `BACKUP_DAYS` and `BACKUP_PATH` can be configured to remove files from `WATCH_PATH` to reduce `importFileExists` execution in `process_logs` when tens of thousands of files exist in `WATCH_PATH` subfolder structure.

If `BACKUP_DAYS` is set to 0 files are never moved or deleted from `WATCH_PATH` subfolder structure. Setting `BACKUP_DAYS` to a positive number will copy files to `BACKUP_PATH` creating an identical subfolder structure as `WATCH_PATH` as files are copied. `BACKUP_DAYS` is number of days since file was initially added to `import_file` TABLE before file is moved to `BACKUP_PATH`. Once file is copied the file will be deleted from `WATCH_PATH`. Setting `BACKUP_DAYS` = -1 files are not copied to `BACKUP_PATH` before deleting files from `WATCH_PATH`. When `BACKUP_DAYS` is set to -1 files are deleted from `WATCH_PATH` next time `processLogs` is executed.

print-level variables can be set to display Process Messages in console or inserted into [PM2](https://github.com/Unitech/pm2) logs for every process step.

Any import errors that occur in Python `process_logs` and Stored Procedures are inserted into `import_error` TABLE.
This is the only schema table that uses ENGINE=MYISAM to avoid TRANSACTION ROLLBACKS.

Logging functionality, database design and table relationship constraints produce both physical and logical integrity. 
This enables a complete audit trail providing ability to determine who, what, when and where each log record originated from.

Client `http-logs-to-mysql` module can run in [PM2](https://github.com/Unitech/pm2) daemon process manager or `logs2mysql` module run in [logrotate's](https://github.com/logrotate/logrotate) apache `postrotate` configuration for 24/7 online processing on multiple web servers feeding a single Server module simultaneous.
