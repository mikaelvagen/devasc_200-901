import os
import json
import meraki
from pprint import pprint

def get_ID(item:dict):
    """ Returns ID-field of dict-item """
    return item["id"]

if __name__ == '__main__':
    # Fetch Meraki DevNet sandbox key stored in separate file
    path_to_auth_file = os.getcwd() + '/authentication.json'
    with open(path_to_auth_file) as auth_file:
        auth_keys = json.load(auth_file)
    API_KEY = auth_keys['meraki_dashboard']

    # Establish session to Meraki Dashboard API
    dashboard = meraki.DashboardAPI(API_KEY)

    # Get network device for specific organization to simplify output
    organizations = dashboard.organizations.getOrganizations()
    org_ID = get_ID(organizations[2])
    networks = dashboard.organizations.getOrganizationNetworks(org_ID)
    net_ID = get_ID(networks[1])
    devices = dashboard.networks.getNetworkDevices(net_ID)
    dev_ID = devices[0]['serial']
    
    # Fetch all clients connected to the device the last month
    clients = dashboard.devices.getDeviceClients(dev_ID)
    if clients: print(clients)
    else: print(f"No clients on device with serial number: {dev_ID}.")
    