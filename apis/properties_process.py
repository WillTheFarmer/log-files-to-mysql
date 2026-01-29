# version 4.0.1 - 01/24/2026 - Proper Python code, NGINX format support and Python/SQL repository separation - see changelog
class ProcessProperties:
    """ standard process properties required for all import_process modules """
    # columns in import_process TABLE
    filesFound = 0
    filesProcessed = 0
    recordsProcessed = 0
    errorCount = 0
    # passed from child process to Import Load (main:process_files) as print message - not required - display only 
    # set to process error message on failure. Import Load (main:process_files) continues to execute next child process.
    # processStatus included in process_list[]. Displayed at end of main:process_files 
    processStatus = None
    # backup attributes at both app-level & process-level property classes
    backup_days = 0
    backup_path = ""

    @classmethod
    def set_defaults(cls):
        """ properties shared by all import_processes - reset process variables at start of process() """
        cls.filesFound = 0
        cls.filesProcessed = 0
        cls.recordsProcessed = 0
        cls.errorCount = 0
        cls.processSeconds = 0.000000
        cls.processStatus = None

    @classmethod
    def process_report(cls):
        process_data = {
            "Files Found": cls.filesFound,
            "Files Loaded": cls.filesProcessed,
            "Records Loaded": cls.recordsProcessed,
            "Process Errors":  cls.errorCount,
            "Process Seconds":  cls.processSeconds,
            "Status":  cls.processStatus
          }
        return process_data

class DataFileLoader(ProcessProperties):
    """properties unique to data_file_loader.py - each variation of data_file_loader.py uses different values """
    log_format = "none"
    load_table = "none"
    log_path = "."
    log_recursive = False
    display_log = 1
    log_server = "mydomain.com"
    log_server_port = 443

class DatabaseModule(ProcessProperties):
    """properties used by each process execution of database_module.py"""

class DataEnrichmentGeoIP(ProcessProperties):
    """properties used by each process execution of data_enrichment_geoIP.py"""

class DataEnrichmentUserAgent(ProcessProperties):
    """properties used by each process execution of data_enrichment_userAgent.py"""
