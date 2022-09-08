import os
import json
import requests
from pprint import pprint

class MerakiNetworkDevices():

    def __init__(self, auth_key:str):
        self.base_url = 'https://api.meraki.com/api/v1'
        self.headers = {
            'X-Cisco-Meraki-API-Key': auth_key,
            'Accept': 'application/json'
            }      
    
    def get_ID(self, item:dict):
        """ Returns ID-field of dict-item """
        return item["id"]

    def get_organizations(self):
        """ Fetches and adds accessible organizations to self.orgs """
        url = self.base_url + '/organizations'
        organizations = requests.get(url, headers=self.headers).json()
        return organizations

    def get_networks(self, org_ID:str):
        """ Returns all networks for a specific organization """
        url = self.base_url + f'/organizations/{org_ID}/networks'
        networks = requests.get(url, headers=self.headers).json()
        return networks

    def get_network_devices(self, network_ID:str):
        """ Returns network devices in a specific network_ID """
        url = self.base_url + f'/networks/{network_ID}/devices'
        devices = requests.get(url, headers=self.headers).json()
        return devices

if __name__ == '__main__':
    # Fetch Meraki DevNet sandbox key stored in separate file
    path_to_auth_file = os.getcwd() + '/authentication.json'
    with open(path_to_auth_file) as auth_file:
        auth_keys = json.load(auth_file)
    API_KEY = auth_keys['meraki_dashboard']

    # Instantiate custom meraki_network_device object and establish session to Meraki cloud
    meraki_network_devices = MerakiNetworkDevices(auth_key=API_KEY)

    # Fetch all accessible organizations and store in list
    organizations = meraki_network_devices.get_organizations()

    # Fetch all networks in organization 3 (chosen randomly) and store in list
    org_ID = meraki_network_devices.get_ID(organizations[2])
    org_networks = meraki_network_devices.get_networks(org_ID)

    # Fetch devices in network number 2 and store in list
    net_ID = meraki_network_devices.get_ID(org_networks[1])
    devices = meraki_network_devices.get_network_devices(net_ID)

    # Filter out some uninteresting information and display network devices and corresponding org/network
    formatted_devices = []
    filter = ["model", "networkId", "mac", "wirelessMac"]
    for device in devices:
        d = {}
        for key, val in device.items():
            if key in filter: d[key] = val
        formatted_devices.append(d)
    print('='*120)
    print(f'Network device list for network {net_ID} in organization {organizations[2]["name"]}:\n')
    for device in formatted_devices: print(device)
    print('='*120)