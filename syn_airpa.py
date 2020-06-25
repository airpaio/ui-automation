import platform
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pick chromedriver based on OS
if platform.system() == 'Windows':
    chromedriver_path = 'chromedriver.exe'
elif platform.system() == 'Linux':
    chromedriver_path = 'chromedriver'

# comment out these options if you want to watch your chromedriver
# in action. These options including headless mode are used when we
# ship to production, run on a server with no gui, Docker, etc.
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--disable-gpu")

class synthetic():
    '''
    synthetic includes methods needed for navigating around the airpa.io web pages 
    '''
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
        self.wait = WebDriverWait(self.driver, 20)

    def goto_url(self, url):
        self.driver.get(url)
    
    def enter_text(self, text, xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(str(text))            
    
    def click_action(self, xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()
    
    def wait_until_element_loads(self, xpath):
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def wait_until_page_loads(self, parent_class):
        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, parent_class)))
    
    def close(self):
        self.driver.quit()

## UI ACTIONS - these are the steps we need to take with their xpaths ##
# navigate to https://airpa.io/login/
# Username text box xpath = //*[@id="authcontainer"]/div[1]/input
# Password text box xpath = //*[@id="authcontainer"]/div[2]/input
# after typing password, click login button xpath = //*[@id="authcontainer"]/div[3]/button
# login banner xpath = //*[@id="authenticator"]/div[1]/h2
# hamburger menu xpath = //*[@id="menuIcon"]/div
# logout button xpath = //*[@id="signoutButton"]
########################################################################

# use your own username and password
username = "username"
password = "password"

ui = synthetic()
start = time.time()
ui.goto_url("https://airpa.io/login/") 
ui.wait_until_page_loads("default")  # initial landing page load completed
landing_page_load_time = time.time() - start

start = time.time()
ui.enter_text(username, '//*[@id="authcontainer"]/div[1]/input')
ui.enter_text(password, '//*[@id="authcontainer"]/div[2]/input')
ui.click_action('//*[@id="authcontainer"]/div[3]/button')
ui.wait_until_element_loads('//*[@id="authenticator"]/div[1]/h2')  # login completed
login_time = time.time() - start

start = time.time()
ui.click_action('//*[@id="menuIcon"]/div')
ui.wait_until_element_loads('//*[@id="signoutButton"]')
ui.click_action('//*[@id="signoutButton"]')
ui.wait_until_page_loads("default")  # logout completed
logout_time = time.time() - start
ui.close()

# print results
print("Landing page load time: \t {}".format(landing_page_load_time))
print("Login time: \t {}".format(login_time))
print("Logout time: \t {}".format(logout_time))