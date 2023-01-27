import yaml
import json
from yaml.loader import SafeLoader
import os
import subprocess
import unittest

ansible_data = yaml.load(open(os.path.join('./clab-bgp/', 'ansible-inventory.yml')), Loader=SafeLoader)
clab_data = json.loads(subprocess.run(['clab', 'ins', '-a', '-f', 'json'], check=True, text=True, shell=False, stdout=subprocess.PIPE).stdout)


class Test(unittest.TestCase):

    def test_r1_inventory(self):
        r1_inventory = ansible_data['all']['children']['vr-csr']['hosts']['clab-bgp-R1']['ansible_host']
        r1_real = clab_data['containers'][0]['ipv4_address'].removesuffix('/24')
        self.assertEqual(r1_inventory, r1_real, msg='r1 inventory is corrupted')
    
    def test_r2_inventory(self):
        r2_inventory = ansible_data['all']['children']['vr-csr']['hosts']['clab-bgp-R2']['ansible_host']
        r2_real = clab_data['containers'][1]['ipv4_address'].removesuffix('/24')
        self.assertEqual(r2_inventory, r2_real, msg='r2 inventory is corrupted')
        
    def test_r3_inventory(self):
        r3_inventory = ansible_data['all']['children']['vr-csr']['hosts']['clab-bgp-R3']['ansible_host']
        r3_real = clab_data['containers'][2]['ipv4_address'].removesuffix('/24')
        self.assertEqual(r3_inventory, r3_real, msg='r3 inventory is corrupted')

if __name__ == '__main__':
    unittest.main()