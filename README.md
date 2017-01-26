# NorkNork - Tool for identifying Empire persistence payloads

## ABOUT:
This script was designed to identify Powershell Empire persistence payloads on Windows systems.  
It currently supports checks for these persistence methods:
- Scheduled Tasks
- Auto-run
- WMI subscriptions
- Security Support provider
- Ease of Access Center backdoors
- Machine account password disable


## INSTALL:

You can run this script with python 2.7 or by downloading the pyinstaller exe.  Run the binary or the script in a powershell window. 

## USAGE:

### Running the python script
```
PS C:\Users\>python norknork.py
```
### Running the binary
```
PS C:\Users\> .\norknork.exe
```
### Save the data into a text file
```
PS C:\Users\> .\norknork.exe > results.txt

```
![alt tag](https://github.com/n00py/NorkNork/blob/master/norknork.png)
###FAQ:

Q: Why didn't you just create this in powershell?

A: I was too lazy to learn powershell. 

Q: Will this find APT?

A: Certainly not. 
