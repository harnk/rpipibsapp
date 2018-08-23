import os
import inspect
import json
import socket
import subprocess
import commands
import platform
from definitions import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    import netifaces
except ImportError:
    print bcolors.WARNING + "Module netifaces not installed" + bcolors.ENDC

#------------------------------------------------------------------
def updateDirInit(directory, iterative=False):
    if iterative:
        directories = [x[0] for x in os.walk(directory)]
    else:
        directories = [directory]

    for directory in directories:
        files = os.listdir(directory)
        pyfiles = filter(lambda x: x[-3:] == '.py' and \
                                   '__init__.py' not in x,
                         files)
        subdirs = next(os.walk(directory))[1]
        with open(os.path.join(directory, '__init__.py'), 'wb') as f:
            for subdir in subdirs:
                f.write('import ' + subdir + '\n')
            f.write('\n')
            for pyfile in pyfiles:
                f.write('import ' + pyfile[0:-3] + '\n')

#------------------------------------------------------------------
def getAllClassesDict(base_package):
    packages = [base_package] + getSubPackages(base_package, iterative=True)
    modules = []
    for package in packages:
        modules += getModules(package)
    classes = []
    for a_module in modules:
        classes += getClasses(a_module)
    classes_dict = {}
    for a_class in classes:
        classes_dict[getObjPath(a_class)] = a_class
    print 'Available sensors found'
    print '--------------------------'
    for i in sorted(classes_dict.keys()):
        print i
    print '--------------------------'
    return classes_dict

#------------------------------------------------------------------
def getAllFunctionsDict(base_package):
    packages = [base_package] + getSubPackages(base_package, iterative=True)
    modules = []
    for package in packages:
        modules += getModules(package)
    functions = []
    for a_module in modules:
        functions += getFunctions(a_module)
    functions_dict = {}
    for a_function in functions:
        functions_dict[getObjPath(a_function)] = a_function
    print 'Available tasks found'
    print '--------------------------'
    for i in sorted(functions_dict.keys()):
        print i
    print '--------------------------'
    return functions_dict

#------------------------------------------------------------------
def getUserFunctionsDict(base_package):
    functions_dict = getAllFunctionsDict(base_package)
    user_functions = []
    for i in sorted(functions_dict.keys()):
         if '<lambda>' not in i and 'tools' not in i:
             user_functions.append(i)
    return user_functions

#------------------------------------------------------------------
def getObjPath(obj_in):
    return obj_in.__module__+'.'+obj_in.__name__

#------------------------------------------------------------------
def getClasses(module):
    out = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            out.append(obj)
    return out

#------------------------------------------------------------------
def getFunctions(module):
    out = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            out.append(obj)
    return out

#------------------------------------------------------------------
def getModules(package):
    out = []
    for name, obj in inspect.getmembers(package):
        if inspect.ismodule(obj) and \
           inspect.getsourcefile(obj)[-11:] != '__init__.py':
            out.append(obj)
    return out

# ------------------------------------------------------------------
def getSubPackages(package, iterative=False):
    if not iterative:
        out = []
        for name, obj in inspect.getmembers(package):
            if inspect.ismodule(obj) and \
                            inspect.getsourcefile(obj)[-11:] == '__init__.py':
                out.append(obj)
        return out
    else:
        out = []

        # iterative depth first search
        s = []
        s.insert(0, package)
        while len(s) != 0:
            v = s.pop(0)
            if v not in out:
                out.append(v)
                for x in getSubPackages(v):
                    s.insert(0, x)
        return out

#------------------------------------------------------------------
def announceError(node, task_name, err):
    print("missing argument: %s" % err)
    payload = {key_message: task_name, 'payload': 'missing argument: ' + str(err)}
    node.messenger.publish(PIBS_MQTT_STATUS_TOPIC_BASE + node.mac_address, payload=json.dumps(payload))

#------------------------------------------------------------------
def getMacAddress():
    # find the network interfaces available
    ifaces = netifaces.interfaces()
    # preference is given to ethernet cord
    if 'eth0' in ifaces:
        info = netifaces.ifaddresses('eth0')[netifaces.AF_LINK]
    elif 'en0' in ifaces:
        info = netifaces.ifaddresses('en0')[netifaces.AF_LINK]
    elif 'wlan0' in ifaces:
        info = netifaces.ifaddresses('wlan0')[netifaces.AF_LINK]
    else:
        # if there is no connection, return a default and hope for best
        print('**ERROR: Unable to determine mac address....')
        print('-> Continuing and hoping for the best!')
        print('-> Using default mac address: 00:00:00:00:00:00')
        return '000000000000'
    # get the mac address from the info
    mac = info[0]['addr']
    # remove colons (':')
    mac = mac.replace(':','')
    return mac

#------------------------------------------------------------------
def disk_usage(path):
    ''' returns the total, used, and available memory in GB for a given path'''
    df = subprocess.Popen(["df", path, "-h"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
            output.split("\n")[1].split()
    return size, used, available

#------------------------------------------------------------------
def get_disk_free():

    # Determine free disk space
    size, used, available = disk_usage('/')
    return available

#------------------------------------------------------------------
def get_disk_used():

    # Determine disk spaced used
    size, used, available = disk_usage('/')
    return used

#------------------------------------------------------------------
def read_os_version():
    '''
    This function determines the OS version of the local host
    (assuming it is a Raspberry Pi).  This is achieved by reading
    the file /etc/os-release and returning a formatted version of
    the PRETTY_NAME.

    by Nik Kleber, 5/1/17
    '''
    # open file /etc/os-release and read PRETTY_NAME (first line)
    with open('/etc/os-release','r') as fp:
        myline = fp.readline()

    # remove \n and whitespace
    myline = myline.strip()
    # get rid of label PRETTY_NAME
    components = myline.split('=')
    # get rid of extra quotes
    myOS = components[1].strip('"')

    return myOS
#------------------------------------------------------------------
def read_hardware_version():
    '''
    This function determines the hardware revision number of the
    local host (assuming it is a Raspberry Pi).  This is achieved by
    reading the file /proc/cpuinfo and returning a formatted version
    of the Revision value.

    by Nik Kleber, 5/1/17
    '''
    # open file /proc/cpuinfo, find 'Revision', print field, remove 1000
    # in front (if it is there at all):
    process = subprocess.Popen( \
        "cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}' | sed 's/^1000//'", \
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()

    if error != '':
        print("WARNING: error in reading hardware version!")
        return "Error"
    else:
        return result.strip()

# ------------------------------------------------------------------
def get_host_name():
    return socket.gethostname()

# ------------------------------------------------------------------
def check_network_connection(address,timeout=.1):
    timeout=1
    response = os.system("ping -c 1 -W " +str(timeout) + " " + address + ">> /dev/null")
    if response == 0:
        return True
    else:
        return False

# ------------------------------------------------------------------
def getIPAddress():
    # check platform
    myOS = platform.system()
    # reboot based on platform
    if myOS == "Linux":
        RetMyIP = commands.getoutput("hostname -I") # returns the IP address of local host as a string
    #elif myOS == "Windows":
    #    os.system("shutdown -r -t 1")
    else:
        print("Command does not work outside Linux")
        RetMyIP = ''
    return RetMyIP
