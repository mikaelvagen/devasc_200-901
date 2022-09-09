import os
import json
import meraki

def get_ID(item:dict):
    """ Returns ID-field of dict-item """
    return item["id"]

if __name__ == "__main__":
    # Fetch Meraki DevNet sandbox key stored in separate file
    path_to_auth_file = os.getcwd() + '/authentication.json'
    with open(path_to_auth_file) as auth_file:
        auth_keys = json.load(auth_file)
    API_KEY = auth_keys['meraki_dashboard']

    # Establish session to Meraki Dashboard API
    dashboard = meraki.DashboardAPI(API_KEY)

    # Fetch all accessible organizations and store in list
    organizations = dashboard.organizations.getOrganizations()
    
    # Fetch all networks in organization 3 (chosen randomly) and store in list
    org_ID = get_ID(organizations[2])
    networks = dashboard.organizations.getOrganizationNetworks(org_ID)
    
    # Fetch devices in network number 2 and store in list
    net_ID = get_ID(networks[1])
    devices = dashboard.networks.getNetworkDevices(net_ID)

    # Filter out some uninteresting information and display network devices and corresponding org/network
    formatted_devices = []
    filter = ["model", "networkId", "mac", "wirelessMac"]
    for device in devices:
        d = {}
        for key, val in device.items():
            if key in filter: d[key] = val
        formatted_devices.append(d)
    print('='*120)
    print(f'Device list for network {net_ID} in organization {organizations[2]["name"]}:\n')
    for device in formatted_devices: print(device)
    print('='*120)