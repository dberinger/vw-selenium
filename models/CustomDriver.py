from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class CustomDriver(webdriver.Chrome):
    def __init__(self, win_username: str, chrome_profile: str, dev_mode: bool, *args, **kwargs):
        self.win_username = win_username
        self.profile_name = chrome_profile
        self.dev_mode = dev_mode
        self.options = self.get_options()
        self.service = Service()
        super(self.__class__, self).__init__(options=self.options, service=self.service, *args, **kwargs)
        if not self.dev_mode:
            self.maximize_window()

    def get_options(self):
        options = webdriver.ChromeOptions()
        if self.dev_mode:
            options.add_experimental_option("debuggerAddress", "localhost:9222")
            print("Running in dev mode. Make sure to launch Chrome on port 9222.")
        else:
            options.add_argument(
                fr"--user-data-dir=C:\Users\{self.win_username}\AppData\Local\Google\Chrome\User Data")
            options.add_argument(fr'--profile-directory={self.profile_name}')

        return options
