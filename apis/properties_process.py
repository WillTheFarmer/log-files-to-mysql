# version 4.0.2 - 02/13/2026 - INT to BIGINT, PyMSQL to MySQLdb, mysql procedures for each server & format - see changelog
class ProcessProperties:
    """ standard process properties required for all import_process modules """
    # process-level metrics - columns in import_process TABLE
    files_found = 0
    files_processed = 0
    records_processed = 0
    error_count = 0
    warning_count = 0
    # passed from child process to Import Load (main:process_files) as print message - not required - display only 
    # set to process error message on failure. Import Load (main:process_files) continues to execute next child process.
    # process_status included in process_list[]. Displayed at end of main:process_files 
    process_status = None
    # backup attributes at both app-level & process-level property classes
    backup_days = 0
    backup_path = ""

    @classmethod
    def set_defaults(cls):
        """ properties shared by all import_processes - reset process variables at start of process() """
        cls.files_found = 0
        cls.files_processed = 0
        cls.records_processed = 0
        cls.error_count = 0
        cls.warning_count = 0
        cls.process_seconds = 0.000000
        cls.process_status = None

    @classmethod
    def process_report(cls):
        process_data = {
            "Files Found": cls.files_found,
            "Files Processed": cls.files_processed,
            "Records Processed": cls.records_processed,
            "Warnings":  cls.warning_count,
            "Errors":  cls.error_count,
            "Process Seconds":  cls.process_seconds,
            "Status":  cls.process_status
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
