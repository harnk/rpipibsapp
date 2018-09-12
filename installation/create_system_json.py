import json

# parameters
filename = '/home/pi/pibs_client/system.json'


# functions

def getMacAddress():
    import netifaces
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

def getIPAddress():
    import commands
    RetMyIP = commands.getoutput("hostname -I") # returns the IP address of local host as a string
    return RetMyIP


def create_system_json():
    macAddress = getMacAddress()

    myconfig = {
        "mac_address": macAddress,
        "broker_name": "fmnc.cse.nd.edu",
        "initial_topics": [
            "pibs/clients/command/"+macAddress,
            "pibs/clients/command/command_to_all",
            "pibs/clients/status/"+macAddress
            ],
        "ip_address": getIPAddress(),
        "sensors": [
            {"type": "sensors.clock.RaspberryClock", "hardware_id": "1"},
            {"type": "sensors.locationing.DummyGPS",
             "hardware_id": "2",
             "latitude": 41.704909999999998,
             "longitude": -86.240613999999994,
             "altitude": 777}
            ],
        "init_tasks": [{"task_name": "tasks.test.echo",
                    "arguments": {"topic": "pibs/clients/command/"+macAddress, "echo_text": "initialization"}}]
        }

    with open(filename,'w') as fp:
        json.dump(myconfig,fp,indent=4,sort_keys=True,separators=(',',':'))
         
        
if __name__=="__main__":
    create_system_json()
