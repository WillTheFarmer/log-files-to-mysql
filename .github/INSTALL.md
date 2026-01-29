## Installation Instructions
The steps are important to make installation painless.

### 1. Python Packages
Install all modules (`requirements.txt` in repository):
```
pip install -r requirements.txt
```
### 2. Database
Before running `apache_logs_schema.sql` if `root`@`localhost` does not exist open file and do a ***Find and Replace*** of User Account with a User Account with DBA Role on installation server. Copy below:
```
`root`@`localhost`
```
Rename above <sup>user</sup> to a <sup>user</sup> on your server. For example - `root`@`localhost` to `dbadmin`@`localhost`

The easiest way to install is MySQL Command Line Client. Login as User with DBA Role and execute the following:
```
source yourpath/apache_logs_schema.sql
```
Only MySQL server must be configured in `my.ini`, `mysqld.cnf` or `my.cnf` depending on platform with following: 
```
[mysqld]
local-infile=1
```
### 3. Create Database USER and GRANTS
To minimize data exposure and breach risks create a Database USER for Python module with GRANTS to only schema objects and privileges required to execute import processes. Replace hostname from `%` to hostname of database such as `localhost` to only allow USER access from single location. (`mysql_user_and_grants.sql` in repository)
### 4. Settings.env steps
Setting environment variables `ERROR`,`COMBINED`, `VHOST`, `CSV2MYSQL`, `USERAGENT` and `GEOIP` = 0 processes nothing but does insert a record into `import_load` TABLE indicating `processLogs` was executed.

`COMBINED` processes ***common*** and ***combined*** LogFormats. `ERROR` processes ***default*** and ***additional*** ErrorLogFormats.

Most configurations will only process a single LogFormat and ErrorLogFormat. Set required formats = 1. 

Make sure logFormats are in correct logFormat folders. Application does not detect logFormats and data will not import properly.

Use backslash `\` for Windows paths and forward slash `/` for Linux and MacOS paths. 

settings.env with default settings for Ubuntu.
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=apache_upload
MYSQL_PASSWORD=password
MYSQL_SCHEMA=apache_logs
WATCH_LOG=2
WATCH_PATH=/home/will/apacheLogs/
WATCH_RECURSIVE=1
WATCH_INTERVAL=15
BACKUP_DAYS=0
BACKUP_PATH=/home/will/apacheLogs_backup/
ERROR=1
ERROR_PROCESS=2
ERROR_LOG=2
ERROR_PATH=/home/will/apacheLogs/**/*error*.*
ERROR_RECURSIVE=1
ERROR_SERVER=mydomain.com
ERROR_server_port=443
COMBINED=1
COMBINED_PROCESS=2
COMBINED_LOG=2
COMBINED_PATH=/home/will/apacheLogs/combined/**/*access*.*
COMBINED_RECURSIVE=1
COMBINED_SERVER=mydomain.com
COMBINED_server_port=443
VHOST=1
VHOST_PROCESS=2
VHOST_LOG=2
VHOST_PATH=/home/will/apacheLogs/vhost/**/*access*.*
VHOST_RECURSIVE=1
CSV2MYSQL=1
CSV2MYSQL_PROCESS=2
CSV2MYSQL_LOG=2
CSV2MYSQL_PATH=/home/will/apacheLogs/csv2mysql/**/*access*.*
CSV2MYSQL_RECURSIVE=1
USERAGENT=1
USERAGENT_PROCESS=1
USERAGENT_LOG=2
GEOIP=1
GEOIP_PROCESS=1
GEOIP_LOG=2
GEOIP_CITY=/usr/share/GeoIP/maxmind/GeoLite2-City.mmdb
GEOIP_ASN=/usr/share/GeoIP/maxmind/GeoLite2-ASN.mmdb
# GEOIP_CITY=/usr/share/GeoIP/dbip/dbip-city-lite.mmdb
# GEOIP_ASN=/usr/share/GeoIP/dbip/dbip-asn-lite.mmdb
```
### 5. Rename settings.env file to .env
By default, load_dotenv() looks for standard setting file name `.env`.
### 6. Run Application
If you have log files in the folders already run the logs2mysql.py directly. It will process all the logs in all the folders. If you have empty folders and want to drop files into folders run the watch4logs.py.

Run import process directly:
```
python3 logs2mysql.py
```
Run polling module:
```
python3 watch4logs.py
```
