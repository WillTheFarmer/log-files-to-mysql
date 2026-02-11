## Python handles File processing & Database handles Data processing
![Entity Relationship Diagram](./images/import_load_summary.png)
`main:process_files` Import Load Summary from ingesting log files included in repository.

### Application runs on Windows, Linux & MacOS - Database runs on MySQL & MariaDB
***JSON data-driven*** App & MySQL schema to automate import of access & error files, normalize log data into database and generate a well-documented data lineage audit trail.

## two Collections and Factory Method

`config.json` has ***Processes*** and ***Observers*** configured to share the seven (7) log format folders in repository `/data/` folder.

### Process properties - application Processes
![Process Properties](./images/process_properties.png)

### Observer properties - application watchdog Observers
![Observers Properties](./images/observer_properties.png)

1) Some ***Processes*** load files from folders into staging LOAD TABLES `data_file_loader.py`, some execute MySQL stored procedures `database_module.py` and some processes perform Data Enhancements - `data_enrichment_geoip.py` and `data_enrichment_useragent.py`.

2) All ***Process Datasets*** have an `attributes` property. The attributes property can have any number of properties the ***Process Module*** requires.

`data_file_loader.py` module has attribute properties for `log_format`, `load_table`, `path`, `recursive`, `server`, `server_port` values.

`database_module.py` module has attribute properties `module_name` and `module_parm1` values.

To process different log format files in different directories the `config.json` Process collection is populated with different combinations of ***Process Datasets***. 

Many `config.json` Process datasets contain `database_module.py` and `data_file_loader.py` for ***module_name*** property. These 2 modules are often reused with different `attributes` property values.

### The data-driven properties allow flexibility and expandability

3) All ***Process Modules*** have `process` method and ***ProcessProperties*** subclass `properties_process.py`. 

4) `main:process_files` can be passed a ***collection filter*** parameter. It can be a Process list (processID) to execute for any number of reasons. This makes the App more integrable and adaptable.

If no parameter is passed `main:process_files` executes `config.json` Processes for status = 'Active'.

5) All ***Observers*** watch using ***Observer datasets*** : `path`, `recursive`, `interval` for the arrival of new files in `path` values.

Each Observer dataset also has `process_list` property. The `process_list` holds a Python List of `[processid]`. It is a subset of `id` property from `config.json` Processes collection.

List of Observers Watching:
![Observers Watching](./images/observers_running.png)

The `process_list` property and watchdog `event.src_path` property are passed to `main:process_files` which will override configured Process executions.

Multiple folders and formats can be processed running different Observers with properties for different log formats and paths.

All processing stages (child processes) are encapsulated within one `main:process_files` (parent process) that captures process metrics, notifications and errors into database import tables.

### Every log data record is traceable back to the computer, path, file, load process, parse process and import process the data originated.

Multiple access and error logs and formats can be loaded, parsed and imported along with User Agent parsing and IP Address Geolocation retrieval processes within a single `main:process_files` execution. 

`main:process_files` executions (`config.json` file) can be configured to only load logs to Server (single process) leaving other processes to be executed within another `main:process_files` execution (`config.json` file) on a centralized computer.

### Python handles polling of log file folders and executing database LOAD DATA, Procedures, Functions and SQL Statements.

## Data Enrichments
### IP Geolocation data integration
using [MaxMind GeoIP2](https://pypi.org/project/geoip2/) Python API provides IP country, subdivision, city, system organization, 
network and coordinates information stored and normalized into 6 database schema tables.

Application requires two GeoLite databases - ***City*** & ***ASN***. GeoLite databases are subsets of the commercial databases with reduced coverage and accuracy. Application tested with these databases: 
1) GeoLite2 databases at [MaxMind](https://www.maxmind.com/en/geolite-free-ip-geolocation-data) available under MaxMind continues to incorporate Creative Commons into our GeoLite End User Agreement (EULA).

2) DB-IP Lite databases at [DB-IP](https://db-ip.com/db/lite.php) available under Creative Commons Attribution 4.0 International License.
### User-Agent data integration
using [user-agents](https://pypi.org/project/user-agents/) provides browser, device and operating system information stored and normalized into 11 database schema tables.

## Required Python Packages
Single quotes around 'PyMySQL[rsa]' package required on macOS.
|Python Package|Installation Command|GitHub Repository|
|--------------|---------------|------------|
|[PyMySQL](https://pypi.org/project/PyMySQL/)|python -m pip install PyMySQL|[PyMySQL/PyMySQL](https://github.com/PyMySQL/PyMySQL)|
|[user-agents](https://pypi.org/project/user-agents/)|python -m pip install pyyaml ua-parser user-agents|[selwin/python-user-agents](https://github.com/selwin/python-user-agents)|
|[watchdog](https://pypi.org/project/watchdog/)|python -m pip install watchdog|[gorakhargosh/watchdog](https://github.com/gorakhargosh/watchdog/tree/master)|
|[python-dotenv](https://pypi.org/project/python-dotenv/)|python -m pip install python-dotenv|[theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)|
|[geoip2](https://pypi.org/project/geoip2/)|python -m pip install geoip2|[maxmind/GeoIP2-python](https://github.com/maxmind/GeoIP2-python)|
|[tabulate](https://pypi.org/project/tabulate/)|python -m pip install tabulate|[astanin/python-tabulate](https://github.com/astanin/python-tabulate)|

## Database designed for HTTP log data analysis
![Entity Relationship Diagram](./images/entity_relationship_diagram.png)

## MySQL database schema DDL and build scripts
[mysql-schema-http-logs](https://github.com/willthefarmer/mysql-schema-http-logs) includes all ***database DDL and build scripts*** for the database schema used in this repository.

Application determines what files have been processed using `import_file` TABLE. 
Each imported file has record with name, path, size, created, modified attributes inserted during `main:process_files`.

Application runs with no need for user interaction. File deletion is not required by application if files desired for later reference.

## new NGINX log formats and data - not tested yet

From documentation read NGINX standard access logformat is same as Apache combined. I have not verified yet.

### Repository NGINX files are standard access and error formats from new NGINX server

NGINX log files in `/data/nginx_combined/` and `/data/nginx_error/` are from new NGINX server.

Apache log formats have been thoroughly researched and tested. 

### new NGINX MySQL procedural code - not tested yet

Each log format has a Stored Procedure. More information will be added over new few days.

The Apache and NGINX code demonstrates how to incorporate without code modification of current processes.

## Visual Interface App
in my development queue [MySQL2ApacheECharts](https://github.com/willthefarmer/mysql-to-apache-echarts) is a ***visualization tool*** for the database schema. The Web interface consists of [Express](https://github.com/expressjs/express) web application frameworks with [W2UI](https://github.com/vitmalina/w2ui) drill-down data grids for Data Point Details.

## Other Documents

[Installation Instructions](INSTALL.md)

[Apache Format Information](APACHE_FORMATS.md)

[Support Information](SUPPORT.md)

[Change Log](CHANGELOG.md)
