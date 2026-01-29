# version 4.0.1 - 01/24/2026 - Proper Python code, NGINX format support and Python/SQL repository separation - see changelog
class app:
  """ required DATA for import_device TABLE Primary ID """
  deviceid = ''
  platformNode = ''
  platformSystem = ''
  platformMachine = ''
  platformProcessor = ''

  """ required DATA for import_client TABLE Primary ID """
  ipaddress = ''
  login = ''
  expandUser = ''
  platformRelease = ''
  platformVersion = ''

  """ application properties shared among all import_processes and other module files """
  importDeviceID = 0
  importClientID = 0
  importLoadID = 0
  importProcessID = 0

  # shared app-level connection and cursor
  dbConnection = None
  cursor = None

  # host_name and host_port used for print messages for main.py functions
  host_name = ''
  host_port = 0
  
  # pymysql_connection_json.py - get_connection default parameters if parameters not passed
  mysql = None
  
  # used in main:process_files and main:update_importProcess for print messages and UPDATE import_process
  processStart = 0
  processSeconds = 0.0000  

  # app-level error handler
  error = None
  errorCount = 0
  error_details = False

  # used in main:execute_process - process becomes importProcess (import_process TABLE) before execution and updated afer execution.
  executeStart = 0
  executeSeconds = 0.0000

  # backup attributes at app-level & process-level property classes
  backup_days = 0
  backup_path = ''
