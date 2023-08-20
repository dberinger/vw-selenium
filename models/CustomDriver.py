from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class CustomDriver(webdriver.Chrome):
    def __init__(self, win_username: str, chrome_profile: str, *args, **kwargs):
        self.win_username = win_username
        self.profile_name = chrome_profile
        self.options = self.get_options()
        self.service = Service()
        super(self.__class__, self).__init__(options=self.options, service=self.service, *args, **kwargs)
        self.maximize_window()

    def get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            fr"--user-data-dir=C:\Users\{self.win_username}\AppData\Local\Google\Chrome\User Data")
        options.add_argument(fr'--profile-directory={self.profile_name}')

        return options
