import sys
import re

def Help():
    if '-h' in sys.argv or len(sys.argv)==1:
        print("Usage: ./util.py [OPTION]... [FILE]\nSupported options:\n---------------------\n  -h, --help         Print help\n  -f, --first=NUM    Print first NUM lines\n  -l, --last=NUM     Print last NUM lines\n  -t, --timestamps   Print lines that contain a timestamp in HH:MM:SS format\n  -i, --ipv4         Print lines that contain an IPv4 address, matching IPs\n                     are highlighted\n  -I, --ipv6         Print lines that contain an IPv6 address (standard\n                     notation), matching IPs are highlighted")

logfile = ""
LogLen = 0
ipv4 = False
ipv6 = False
time = False
CopyFile = []

def First():
    ok = False
    if '-f' in sys.argv:
        n = sys.argv.index('-f')
        ok = True
    elif'--first' in sys.argv:
        n = sys.argv.index('--first')
        ok = True
    if ok == True and NumCheck(n) != -1:
        M = NumCheck(n)
        if M > LogLen:
            M = LogLen
        if M != -1:
            print("\nFirst ", M)
            for I in range(0,M):
                print(CopyFile[I], end = '')

def Last():
    ok = False
    if '-l' in sys.argv:
        n = sys.argv.index('-l')
        ok = True
    elif'--last' in sys.argv:
        n = sys.argv.index('--last')
        ok = True
    if ok == True and NumCheck(n) != -1:
        M = NumCheck(n)
        if M != -1:
            if M > LogLen:
                M = 0
            else:
                print("Last ", M)
                M = LogLen - M
            for I in range(M-1,LogLen):
                print(CopyFile[I], end = '')

def ListCheck(): #list all lines with ipv4 or ipv6 adresses
    if ipv4 or ipv6 or time:
        for I in range(0,LogLen):
            again = False #prevent printing same line twice
            if ipv4:
                if re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}",CopyFile[I]): #regex for all ipv4
                    print(CopyFile[I], end = '')
                    again = True
            if ipv6 and again == False:
                if re.search("([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)",CopyFile[I]): #regex for all ipv6
                    print(CopyFile[I], end = '')
                    again = True
            if time and again == False:
                if re.search("(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)",CopyFile[I]): #regex for all ipv6
                    print(CopyFile[I], end = '')

def NumCheck(index): #checks if next argument is a number (returns the number if correct, -1 if not)
    try:
        index += 1
        num = int(sys.argv[index])
        return num
    except IndexError:
        print("Error: Missing number of lines or invalid input.")
        return -1

def FileOk(): #Trys to open file given
    if len(sys.argv)>2:
        try:
            global logfile
            logfile=open(sys.argv[len(sys.argv)-1],"r")
            global CopyFile
            CopyFile = logfile.readlines().copy()
            
            for I in CopyFile:
                global LogLen
                LogLen += 1
                
            return True
        except IOError:
           print("Error: File could not be open or does not exist.")
           return False


if FileOk():
    Last() # Checks if user wants some lines from the bottom of file and how many
    First() # Checks if user wants some lines from the top of file and how many    
    #if user wants ipv4, ipv6, timestamp or any combination 
    if '-i' in sys.argv or '--ipv4' in sys.argv:
        ipv4 =True
    if '-I' in sys.argv or '--ipv6' in sys.argv:
        ipv6 = True
    if '-t' in sys.argv or '--timestamps' in sys.argv:
        time = True
        
    ListCheck()
    logfile.close()
else:
    Help()
    exit()
