import subprocess,re
import pandas as pd
import io
import csv
# Code to fetch the Bios Version of remote system
def Check_Bios_Version(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} systeminfo | find \"BIOS Version\""
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            match=re.search(r'BIOS Version: (.+)', res)
        except:
            print("Regular expression error")
        return match.group(1).strip()
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity"

def Check_OS_Version(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} systeminfo | find \"OS Version\""
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            match=re.search(r'OS Version: (.+)', res)
        except:
            print("Regular expression error")
        return match.group(1).strip()
    except subprocess.CalledProcessError:
        return f"Error: Check Hostname or network connectivity"

def Check_Servicetag(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic bios get serialnumber"
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        serialnumber_match=re.search(r'SerialNumber\s*([^"\n\r]*)',res)
        return serialnumber_match.group(1).strip() if serialnumber_match else "serial number not found" 
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity"

def Check_SystemStates(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} powercfg -a"
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        supported_states_match=re.search(r'The following sleep states are available on this system',res)
        if supported_states_match:
            return str(res.split("\n")[21:35][0:5][1:5])  
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity"

def System_Restart(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} shutdown -r"
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        return "System Restarted"
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity"
 

def Check_Chipset(system):
    try:
        intel_pattren=r'Intel\(R\) Core\(TM\) [^\s]+'
        AMD_pattren=r'AMD Ryzen[^\n]+'
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic cpu get"
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            match1=re.findall(intel_pattren, res)
            match2=re.search(AMD_pattren,res,re.IGNORECASE)
            if match1:
                return match1
            elif match2:
                return str(match2)
        except:
            print("Reg Errror")
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity"


def Check_System_Model(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} systeminfo | find \"System Model\""
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            match=re.search(r'System Model: (.+)', res)
        except:
            print("Regular expression error")
        return match.group(1).strip()
    except subprocess.CalledProcessError as e:
        return f"Error: Check Hostname or network connectivity {e}"

# def Get_Drive_Controller(system):
#     try:
#         powershell_command = f"Invoke-Command -ComputerName {system} -ScriptBlock {{Get-WmiObject -Class 'Win32_PnPSignedDriver' | Where-Object {{ $_.DeviceClass -eq 'DISKDRIVE'}} | Select-Object -Property Description, DriverVersion }}"
#         psexec_command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\ {system} powershell -Command \"{powershell_command}\""
#         output = subprocess.check_output(psexec_command, shell=True, text=True, stderr=subprocess.STDOUT)
#         return output
#     except subprocess.CalledProcessError as e:
#         return f"Error: Check Hostname or network connectivity {e}"

def get_ram(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} systeminfo"
        res = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            res = subprocess.check_output(command,shell=True,text=True)
            ram_info_line=[line for line in res.split('\n') if 'Total Physical Memory' in line]

            if ram_info_line:
                ram_info = ram_info_line[0].split(':')[1].strip()
                pass
        except:
            print("Regular expression error")
        return ram_info
    except subprocess.CalledProcessError as e:
        return f"Error: Check for system hang or network connectivity {e}" 

def get_gpu(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic path win32_videocontroller get caption"
        gpures = subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        try:
            
            gpu_info_list=gpures.strip().split('\n')[1:]
          
            return gpu_info_list[21]    
        except:
            print("Regular expression error")
        
    except subprocess.CalledProcessError as e:
        return f"Error: Check for system hang or network connectivity {e}" 
          
    
def getDriveModel(system):
    try:
        psexec_command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic diskdrive get model > drive_models.csv"
        #psexec_command1 = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic diskdrive list brief"
        #res=subprocess.check_output(psexec_command1,shell=True,text=True)
        subprocess.check_output(psexec_command,shell=True,text=True)

        # micron_list=re.findall(r'\bMicron_\w+', res)
        # if micron_list:
        #     return micron_list[0]
        # else:
        df=pd.read_csv('drive_models.csv')
        df.columns = df.columns.str.strip()
        return df['Model']    

    except subprocess.CalledProcessError as e:
        return f"Error: Check for system hang or network connectivity {e}"    
    
def getDriveCount(system):
    try:
        command = f"C:\\Windows\\System32\\PSTools\\PsExec.exe \\\\{system} wmic diskdrive list brief"
        drvrs=subprocess.check_output(command,shell=True,text=True,stderr=subprocess.STDOUT)
        pattern=r'\\\.\\PHYSICALDRIVE'
        
        matches=re.findall(pattern,drvrs)
        count=len(matches)
        return count
    
    except subprocess.CalledProcessError as e:
        return f"Error: Check for system hang or network connectivity {e}" 
    
 
def Get_Drive_Controller(system):
    try:
        cmd_command = ["wmic", "/node:" + system, "path", "Win32_PnPSignedDriver", "get", "Description,DriverVersion", "/format:csv"]
        output = subprocess.check_output(cmd_command, text=True, stderr=subprocess.STDOUT)

        # Filter out only the storage controller driver info
        lines = output.strip().split('\n')
        filtered_lines = [line.split(',')[1:] for line in lines if "intel rst vmd managed controller" in line.lower()
                          or "microsoft storage spaces controller" in line.lower()]

        # Format the filtered lines into a table format
        table_data = []
        for line in filtered_lines:
            if len(line) == 2:
                table_data.append({"Description": line[0].strip(), "DriverVersion": line[1].strip()})
       
        return table_data
    except subprocess.CalledProcessError as e:
        return f"Error: Check for system hang or network connectivity: {e}"
    

def Get_manufacturer_info(system): 
    try:
        cmd_command = ["wmic", "/node:" + system, "path", "Win32_ComputerSystem", "get", "Manufacturer", "/format:csv"]
        output = subprocess.check_output(cmd_command, text=True, stderr=subprocess.STDOUT)
        lines = output.strip().split('\n')
        if len(lines) > 1:
            manufacturer = lines[-1].strip()
            return manufacturer.split(",")[1].strip()
            #return manufacturer
        else:
            return "Manufacturer information not available "
    except subprocess.CalledProcessError as e:
        return f"Error:Check for system hang or network connectivity : {e}"

