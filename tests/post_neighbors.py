# Standard Imports
import unittest, os, time

# Third-Party Imports
from ansible_vault import Vault
import scrapli

# pull required information to begin test such as ansible vault location and password from the environmental variables

try: 
    vault_pass = os.environ['VAULT_PASS']
    vault_loc = os.environ['VAULT_LOC']
except KeyError:
    raise ValueError('Both VAULT_PASS and VAULT_LOC must be set as environment variables.')

try:
    with open(vault_loc) as f:
        vault = Vault(vault_pass)
        vault_data = vault.load(f.read())
except FileNotFoundError as e:
    raise ValueError(f'Vault file not found: {vault_loc}') from e
except IOError as e:
    raise ValueError(f'Error reading the vault file: {vault_loc}') from e


def establish_connection(vault_data: dict) -> scrapli.driver.core.IOSXEDriver:
    # Receieve the vault data to establish a connection to R2 "hub bgp router" and return the opened connection object to be used for any reason.
    connection = scrapli.driver.core.IOSXEDriver( # https://carlmontanari.github.io/scrapli/user_guide/basic_usage/
        host='clab-bgp-r2',
        auth_username=vault_data['ios_user'],
        auth_password=vault_data['ios_pass'],
        auth_strict_key=False,
    )
    connection.open()
    return connection

def bgp_query(connection: scrapli.driver.core.IOSXEDriver) -> dict:
    # Receive the opened connection object and execute BGP CLI commands and return the data parsed as a dictionary.
    bgp_output = connection.send_command("show ip bgp summary")
    bgp_parsed = bgp_output.genie_parse_output()
    return bgp_parsed['vrf']['default']['neighbor']
    
# stop race conditions from occuring in which the router is recently configured and allow BGP time to establish before testing it.
time.sleep(10) 

# execute the functions regardless of import via module or executed directly.
neighbors = bgp_query(establish_connection(vault_data))

class ConfirmNeighborsR2(unittest.TestCase):
    # test case to confirm that all neighbors returned in the dictionary are established
    # it's important to note that cisco uses a combined "state_pfxrcd" field which is represents 
    # a string if the neighbor is not established and a string which represents a number of 
    # routes received if the neighbor is established.
    def test_r2_neighbors(self):
        for neighbor in neighbors.values():
            self.assertGreaterEqual(int(neighbor['address_family']['']['state_pfxrcd']), 0, 
            msg=f'Neighbor {neighbor} is in not established state. Requires BGP troubleshooting.')

if __name__ == '__main__':
    unittest.main()