"""
:function: get_device_id
:synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
:author: Will Raymond <farmfreshsoftware@gmail.com>
"""
from platform import system
# Information to identify & register import load clients 
def get_device_id():
    sys_os = system()
    if sys_os == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography") as key:
                return winreg.QueryValueEx(key, "MachineGuid")[0]
        except:
            return "Not Found"
    elif sys_os == "Darwin":
        import subprocess
        return subprocess.check_output("system_profiler SPHardwareDataType | grep 'Serial Number (system)' | awk '{print $4}'", shell=True).decode().strip()
    elif sys_os == "Linux":
        try:
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        except:
            return "Not Found"
    else:
        return "Unsupported Platform"
