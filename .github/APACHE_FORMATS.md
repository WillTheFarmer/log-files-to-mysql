## Four Apache Access Log Formats
Apache uses Standard Access LogFormats (***common***, ***combined***, ***vhost_combined***) on all 3 platforms. Each LogFormat adds 2 Format Strings to the prior. 
Format String descriptions are listed below each LogFormat. Information from: https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#logformat 
```
LogFormat "%h %l %u %t \"%r\" %>s %O" common
```
|Format String|Description|
|-------------|-----------|
|%h|Remote hostname. Will log IP address if HostnameLookups is set to Off, which is default. If it logs hostname for only a few hosts, you probably have access control directives mentioning them by name.|
|%l|Remote logname. Returns dash unless "mod_ident" is present and IdentityCheck is set On. This can cause serious latency problems accessing server since every request requires a lookup be performed.| 
|%u|Remote user if the request was authenticated. May be bogus if return status (%s) is 401 (unauthorized).|
|%t|Time the request was received, in the format [18/Sep/2011:19:18:28 -0400]. The last number indicates the timezone offset from GMT|
|%r|First line of request. Contains 4 format strings (%m - The request method, %U - The URL path requested not including any query string, %q - The query string, %H - The request protocol)|
|%s|Status. For requests that have been internally redirected, this is the status of the original request. Use %>s for the final status.|
|%O|Bytes sent, including headers. May be zero in rare cases such as when a request is aborted before a response is sent. You need to enable mod_logio to use this.|
```
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
```
|Format String|Description - additional format strings|
|-------------|-----------|
|"%{Referer}i|The "Referer" (sic) HTTP request header. This gives the site that the client reports having been referred from.|
|%{User-Agent}i|The User-Agent HTTP request header. This is the identifying information that the client browser reports about itself.|
```
LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
```
|Format String|Description - additional format strings|
|-------------|-----------|
|%v|The canonical ServerName of the server serving the request.|
|%p|The canonical port of the server serving the request.|

Application is designed to use the ***csv2mysql*** LogFormat. LogFormat has comma-separated values and adds 8 Format Strings. A complete list of Format Strings
with descriptions indicating added Format Strings below.
```
LogFormat "%v,%p,%h,%l,%u,%t,%I,%O,%S,%B,%{ms}T,%D,%^FB,%>s,\"%H\",\"%m\",\"%U\",\"%q\",\"%{Referer}i\",\"%{User-Agent}i\",\"%{VARNAME}C\",%L" csv2mysql
```
|Format String|Description|
|-------------|-----------|
|%v|The canonical ServerName of the server serving the request.|
|%p|The canonical port of the server serving the request.|
|%h|Remote hostname. Will log the IP address if HostnameLookups is set to Off, which is the default.|
|%l|Remote logname. Returns dash unless "mod_ident" is present and IdentityCheck is set On. This can cause serious latency problems accessing server since every request requires a lookup be performed.| 
|%u|Remote user if the request was authenticated. May be bogus if return status (%s) is 401 (unauthorized).|
|%t|Time the request was received, in the format [18/Sep/2011:19:18:28 -0400]. The last number indicates the timezone offset from GMT|
|%I|ADDED - Bytes received, including request and headers. Enable "mod_logio" to use this.|
|%O|Bytes sent, including headers. The %O format provided by mod_logio will log the actual number of bytes sent over the network. Enable "mod_logio" to use this.|
|%S|ADDED - Bytes transferred (received and sent), including request and headers, cannot be zero. This is the combination of %I and %O. Enable "mod_logio" to use this.|
|%B|ADDED - Size of response in bytes, excluding HTTP headers. Does not represent number of bytes sent to client, but size in bytes of HTTP response (will differ, if connection is aborted, or if SSL is used).|
|%{ms}T|ADDED - The time taken to serve the request, in milliseconds. Combining %T with a unit is available in 2.4.13 and later.|
|%D|ADDED - The time taken to serve the request, in microseconds.|
|%^FB|ADDED - Delay in microseconds between when the request arrived and the first byte of the response headers are written. Only available if LogIOTrackTTFB is set to ON. Available in Apache 2.4.13 and later.|
|%s|Status. For requests that have been internally redirected, this is the status of the original request.|
|%H|The request protocol. Included in %r - First line of request.|
|%m|The request method. Included in %r - First line of request.|
|%U|The URL path requested, not including any query string. Included in %r - First line of request.|
|%q|The query string (prepended with a ? if a query string exists, otherwise an empty string). Included in %r - First line of request.|
|%{Referer}i|The "Referer" (sic) HTTP request header. This gives the site that the client reports having been referred from.|
|%{User-Agent}i|The User-Agent HTTP request header. This is the identifying information that the client browser reports about itself.|
|%{VARNAME}C|ADDED - The contents of cookie VARNAME in request sent to server. Only version 0 cookies are fully supported. Format String is optional.|
|%L|ADDED - The request log ID from the error log (or '-' if nothing has been logged to the error log for this request). Look for the matching error log line to see what request| caused what error.
## Two Apache Error Log Formats - next release includes NGINX Formats
Application processes Error Logs with ***default format*** for threaded MPMs (Multi-Processing Modules). If running Apache 2.4 on any platform 
and ErrorLogFormat is not defined in config files this is the Error Log format.
Information from: https://httpd.apache.org/docs/2.4/mod/core.html#errorlogformat
```
ErrorLogFormat "[%{u}t] [%-m:%l] [pid %P:tid %T] %7F: %E: [client\ %a] %M% ,\ referer\ %{Referer}i"
```
|Format String|Description|
|-------------|-----------|
|%{u}t|The current time including micro-seconds|
|%m|Name of the module logging the message|
|%l|Loglevel of the message|
|%P|Process ID of current process|
|%T|Thread ID of current thread|
|%F|Source file name and line number of the log call. %7F - the 7 means only display when LogLevel=debug|
|%E|APR/OS error status code and string|
|%a|Client IP address and port of the request|
|%M|The actual log message|
|%{Referer}i|The "Referer" (sic) HTTP request header. This gives the site that the client reports having been referred from.| 

Application also processes Error Logs with ***additional format*** which adds:
 1) `%v - The canonical ServerName` - This is easiest way to identify error logs for each domain is add `%v` to ErrorLogFormat. 
 2) `%L - Log ID of the request` - This is easiest way to associate Access record that created an Error record. 
 Apache mod_unique_id.generate_log_id() only called when error occurs and will not cause performance degradation under error-free operations. 

***Important:*** `Space` required on left-side of `Commas` as defined below:
```
ErrorLogFormat "[%{u}t] [%-m:%l] [pid %P:tid %T] %7F: %E: [client\ %a] %M% ,\ referer\ %{Referer}i ,%v ,%L"
```
To use this format place `ErrorLogFormat` before `ErrorLog` in `apache2.conf` to set error log format for ***Server*** and ***VitualHosts*** on Server.
|Format String|Description - `Space` required on left-side of `Commas` to parse data properly|
|-------------|-----------|
|%v|The canonical ServerName of the server serving the request.|
|%L|Log ID of the request. A %L format string is also available in `mod_log_config` to allow to correlate access log entries with error log lines. If [mod_unique_id](https://httpd.apache.org/docs/current/mod/mod_unique_id.html) is loaded, its unique id will be used as log ID for requests.|

### Three options to associate ServerName & server_port to Access & Error logs
Apache LogFormats - ***common***, ***combined*** and Apache ErrorLogFormat - ***default*** do not contain `%v - canonical ServerName` and `%p - canonical server_port`.

In order to consolidate logs from multiple domains `%v - canonical ServerName` is required and `%p - canonical server_port` is optional.

Options to associate ServerName and server_port to Access and Error logs are:

1) Image shows three configurations. Top (A) is default and Bottom (C) will SET  `server_name` and `server_port` COLUMNS of `load_error_default` and `load_access_combined` TABLES during Python `LOAD DATA LOCAL INFILE` execution.

![load_settings_variables.png](./images/load_settings_variables.png)

2) Manually ***UPDATE*** `server_name` and `server_port` COLUMNS of `load_error_default` and `load_access_combined` TABLES after STORED PROCEDURES `process_access_parse` 
and `process_error_parse` and before `process_access_import` and `process_error_import`. 
If `%v` or `%p` Format Strings exist parsing into `server_name` and `server_port` COLUMNS is performed in parse processes. 
Data Normalization is performed in import processes. 

3) Populate `server_name` and `server_port` COLUMNS in `import_file` TABLE before import processes. This will populate all records associated with file.
This option only updates records with NULL values in ***load_tables*** `server_name` and `server_port` COLUMNS while executing 
STORED PROCEDURES `process_access_import` and `process_error_import`. 

UPDATE commands to populate both Access and Error Logs if ***"Log File Names"*** are related to VirtualHost similar to:
```
 ErrorLog ${APACHE_LOG_DIR}/farmfreshsoftware.error.log
 CustomLog ${APACHE_LOG_DIR}/farmfreshsoftware.access.log csv2mysql
```
Log file naming conventions enable the use of UPDATE statements:
```
UPDATE import_file SET server_name='farmfreshsoftware.com', server_port=443 WHERE server_name IS NULL AND name LIKE '%farmfreshsoftware%';
UPDATE import_file SET server_name='farmwork.app', server_port=443 WHERE server_name IS NULL AND name LIKE '%farmwork%';
UPDATE import_file SET server_name='ip255-255-255-255.us-east.com', server_port=443 WHERE server_name IS NULL AND name LIKE '%error%';
```
