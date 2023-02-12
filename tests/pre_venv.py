import os
import unittest

class TestVenv(unittest.TestCase):
    def test_venv(self):
        current_directory = os.getcwd() + '/.venv'
        if 'VIRTUAL_ENV' in os.environ:
            self.assertEqual(os.environ['VIRTUAL_ENV'], current_directory)
        else:
            self.assertTrue(False, "No virtual environment found")

if __name__ == '__main__':
    unittest.main()