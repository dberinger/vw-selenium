import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.SheetBots import VwBot
from models.CustomDriver import CustomDriver
from private.private import G_SERVICE_ACCOUNT_CREDS_PATH


def extract_price(text: str):
    # regular expression to find price in 'od xx xxx zł' text
    regexp = r'od\s(.*?)\szł'
    match = re.search(regexp, text)
    if match:
        return match.group(1).replace(' ', '')


bot = VwBot(G_SERVICE_ACCOUNT_CREDS_PATH,'1WPSCNLxT1mwd09kQp_xcTVr7EMhSHTpH4P3dYyCn4Ps', 'vw')
car_data = bot.get_input()

driver = CustomDriver('Daniel', 'Profile 2', True)

for car in car_data:
    driver.get(f'https://www.volkswagen.pl/pl/modele/{car["slug"]}.html')
    full_price_txt = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//li[contains(span, "Cena katalogowa")]'))).get_attribute("innerHTML")
    monthly_txt = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//span[contains(span, "netto/m")]'))).get_attribute("innerHTML")

    if car['monthly'] == extract_price(monthly_txt):
        car['qa_monthly'] = True

    if car['price'] == extract_price(full_price_txt):
        car['qa_price'] = True

    else:
        car['qa_monthly'] = False
        car['qa_price'] = False

    car['qa_done'] = True

    bot.fill_qa(car_data)
    bot.update_t()

driver.quit()
