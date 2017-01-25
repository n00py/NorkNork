import base64
from _winreg import *
import subprocess

def registry():
    Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    HKLMKey = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    RawKey = OpenKey(Registry, HKLMKey)


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


    Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
    HKCUKey = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    RawKey = OpenKey(Registry, HKCUKey)


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

    Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
    DebugKey = "SOFTWARE\Microsoft\Windows\CurrentVersion"
    RawKey = OpenKey(Registry, DebugKey)

    try:
        i = 0
        while 1:
            name, value, type = EnumValue(RawKey, i)
            if name == "Debug":
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Possible Script Code (Debug)"
                print "-----------------------------------------------------------------------------------------------------------"
                print value
                payload = base64.b64decode(value)
                payload = payload.replace(";", ";\n")
                payload = payload.replace("\x00", "")
                print "-----------------------------------------------------------------------------------------------------------"
                print "                    Base64 Decoded:"
                print "-----------------------------------------------------------------------------------------------------------"
                print payload
                print "-----------------------------------------------------------------------------------------------------------"

            i += 1
    except WindowsError:
        print""

def schtasks():
    command= "schtasks /query /fo csv /V"
    result = []
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        if "powershell" in line:
            print "-----------------------------------------------------------------------------------------------------------"
            print '                    ********** Found Evil Scheduled Task **********'
            TaskName = line.split(',')[1]
            TaskName = TaskName.replace("\\", "")
            print 'Name: ' + TaskName
            TaskCommand = line.split(',')[8]
            print 'Command :' + TaskCommand
            print "-----------------------------------------------------------------------------------------------------------"
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)




def wmi():
    keepgoing = 0
    evilcode = ""
    command = "powershell Get-WMIObject -Namespace root\Subscription -Class __EventConsumer"
    result = []
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    evilstring ="powershell"
    for line in result:
        #print line
        if evilstring in line:
            print "-----------------------------------------------------------------------------------------------------------"
            print '                    ********** Found Evil WMI subscription **********'
            #print line
            #evilcode += line
            keepgoing = 15
            print "-----------------------------------------------------------------------------------------------------------"
        if keepgoing > 0:
            #print line
            evilcode += line
            keepgoing = keepgoing - 1
    print evilcode
    base64evil = evilcode.split('-enc ')[1]
    #print base64evil
    stupid = base64.b64decode(base64evil)
    stupid = stupid.replace(";", ";\n")
    stupid = stupid.replace("\x00", "")
    print "-----------------------------------------------------------------------------------------------------------"
    print "                    Base64 Decoded"
    print "-----------------------------------------------------------------------------------------------------------"
    print stupid
    print "-----------------------------------------------------------------------------------------------------------"
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)


schtasks()
registry()
wmi()
