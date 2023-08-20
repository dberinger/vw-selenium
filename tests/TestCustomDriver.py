import unittest
from ..models.CustomDriver import CustomDriver  # Adjust the import as needed
import tracemalloc
tracemalloc.start()


class TestCustomDriver(unittest.TestCase):
    test_user = {
        'username': 'Dan',
        'profile': 'Default'
    }

    def setUp(self):
        self.driver = None

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_custom_driver_initialization(self):
        win_username = self.test_user['username']
        profile_name = self.test_user['profile']
        self.driver = CustomDriver(win_username, profile_name)
        self.assertEqual(self.driver.win_username, win_username)
        self.assertEqual(self.driver.profile_name, profile_name)
        self.assertEqual(self.driver.options.arguments, self.driver.get_options().arguments)
        self.assertEqual(self.driver.service, self.driver.service)

    def test_get_options(self):
        win_username = self.test_user['username']
        profile_name = self.test_user['profile']
        self.driver = CustomDriver(win_username, profile_name)
        options = self.driver.get_options()
        self.assertTrue(options.arguments)
        self.assertIn(fr"--user-data-dir=C:\Users\{win_username}\AppData\Local\Google\Chrome\User Data",
                      options.arguments)
        self.assertIn(f'--profile-directory={profile_name}', options.arguments)


if __name__ == '__main__':
    unittest.main()
