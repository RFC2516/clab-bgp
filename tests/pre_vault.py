import os
import unittest

class TestVaultLoc(unittest.TestCase):
    def test_VaultLoc(self):
        if 'VAULT_LOC' in os.environ:
            self.assertTrue(True, 'Vault Location environmental variable found.' )
        else:
            self.assertTrue(False, 'No Vault Location environmental variable found.')

    def test_VaultPass(self):
        if 'VAULT_PASS' in os.environ:
            self.assertTrue(True, 'Vault Password environmental variable found.' )
        else:
            self.assertTrue(False, 'No Vault Password environmental variable found.')

if __name__ == '__main__':
    unittest.main()
