import base64
import subprocess
from _winreg import *


def reg_reader(reg,key):
    Registry = ConnectRegistry(None, reg)
    HKLMKey = key
    RawKey = OpenKey(Registry, HKLMKey)
    return RawKey
def decode(based):
    decoded = base64.b64decode(based)
    decoded = decoded.replace(";", ";\n")
    decoded = decoded.replace("\x00", "")
    for line in decoded.splitlines():
        if ("$K=" or "$k=") in line:
            print line
        else:
            print line.lower()
def run_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)
    return result
def evil_ssp():
    RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SYSTEM\CurrentControlSet\Control\Lsa")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if name == "Security Packages":
                for x in value:
                    if x not in ["kerberos","msv1_0","schannel","wdigest","tspkg","pku2u"]:
                        print "-----------------------------------------------------------------------------------------------------------"
                        print '                    **********  Rouge security support provider dll  **********'
                        print ""
                        print x + " is listed as an SSP"
                        print "-----------------------------------------------------------------------------------------------------------"
            i += 1
    except WindowsError:
        print ""
def disable_machine_acct_change():
    RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SYSTEM\CurrentControlSet\services\Netlogon\Parameters")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if name == "DisablePasswordChange" and value == 1:
                print "-----------------------------------------------------------------------------------------------------------"
                print '                    **********  Machine Account password change disabled  **********'
                print ""
                print "HKLM\SYSTEM\CurrentControlSet\services\Netlogon\Parameters\DisabledPasswordChange is enabled"
                print "-----------------------------------------------------------------------------------------------------------"
            i += 1
    except WindowsError:
        print ""
def misc_debugger():

    binaries = ["Utilman.exe","sethc.exe","osk.exe","Narrator.exe","Magnify.exe"]
    try:
        for binary in binaries:
            RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + binary)
            try:
                i = 0
                while 1:
                    name, value, type = EnumValue(RawKey, i)
                    if "powershell" in value:
                        print "-----------------------------------------------------------------------------------------------------------"
                        print '                    **********  Ease-of-access Center Backdoor (' + binary + ')  **********'
                        print "Name: " + name
                        print"Command: " + value
                        print "-----------------------------------------------------------------------------------------------------------"
                    i += 1
            except WindowsError:
                print ""
    except:
        print ""
def debug_payloads():
    RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Network")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if name == "debug":
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Possible Script Code (HKLM\SOFTWARE\Microsoft\Network\debug)"
                print "-----------------------------------------------------------------------------------------------------------"
                print value
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Base64 Decoded:"
                print "-----------------------------------------------------------------------------------------------------------"
                decode(value)
                print "-----------------------------------------------------------------------------------------------------------"

            i += 1
    except WindowsError:
        print ""
    RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if name == "Debug":
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Possible Script Code (HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Debug)"
                print "-----------------------------------------------------------------------------------------------------------"
                print value
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Base64 Decoded:"
                print "-----------------------------------------------------------------------------------------------------------"
                decode(value)
                print "-----------------------------------------------------------------------------------------------------------"

            i += 1
    except WindowsError:
        print ""
def registry():

    RawKey = reg_reader(HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if "powershell -Win Hidden -enc" in value:
                print "-----------------------------------------------------------------------------------------------------------"
                print '                    ********** Userland Empire persistence found **********'
                print "Name: " + name
                print"Command: " + value
                print "-----------------------------------------------------------------------------------------------------------"
            i += 1
    except WindowsError:
        print ""
    RawKey = reg_reader(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if "powershell -Win Hidden -enc" in value:
                print "-----------------------------------------------------------------------------------------------------------"
                print '                    ********** Elevated Empire persistence found **********'
                print"Name: " + name
                print "Command: " + value
                print "-----------------------------------------------------------------------------------------------------------"

            i += 1
    except WindowsError:
        print ""

def schtasks():
    result = run_cmd("schtasks /query /fo csv /V")
    for line in result:
        if "powershell.exe -NonI -W hidden" in line:
            print "-----------------------------------------------------------------------------------------------------------"
            print '                    ********** Found Evil Scheduled Task **********'
            TaskName = line.split(',')[1]
            TaskName = TaskName.replace("\\", "")
            print 'Name: ' + TaskName
            TaskCommand = line.split(',')[8]
            print 'Command :' + TaskCommand
            print "-----------------------------------------------------------------------------------------------------------"
def wmi():
    readPayload = 0
    evilcode = ""
    result = run_cmd("powershell Get-WMIObject -Namespace root\Subscription -Class __EventConsumer")
    for line in result:
        if "powershell.exe -NonI -W hidden -enc" in line:
            print "-----------------------------------------------------------------------------------------------------------"
            print '                    ********** Found Evil WMI subscription **********'
            readPayload = 15
            print "-----------------------------------------------------------------------------------------------------------"
        if readPayload > 0:
            evilcode += line
            readPayload = readPayload - 1
    print evilcode
    base64evil = evilcode.split('-enc ')[1]

    print "-----------------------------------------------------------------------------------------------------------"
    print "                    Base64 Decoded"
    print "-----------------------------------------------------------------------------------------------------------"
    decode(base64evil)
    print "-----------------------------------------------------------------------------------------------------------"

evil_ssp()
disable_machine_acct_change()
misc_debugger()
schtasks()
registry()
wmi()
debug_payloads()
