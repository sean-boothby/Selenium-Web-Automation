from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("date", help="Enter date in format mm/dd/yyyy with '/'")
args = parser.parse_args()
options = webdriver.ChromeOptions()
dates = str(args.date).split('/')
date = dates[2] + '-' + dates[0] + '-' + dates[1]

#Edit the path below, but leave date variable at the end!
directory = 'C:\\Users\\sean\\Desktop\\trash' + '\\' + date 
if not os.path.exists(directory):
    os.makedirs(directory)
prefs = {'download.default_directory' : directory}
options.add_experimental_option('prefs', prefs)
#options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Users\sean\Desktop\python projects\Selenium drivers\chromedriver')

def start():
    try:
        driver.get('https://www.snl.com/web/client?auth=inherit&contextType=external&username=string&enablePersistentLogin=true&OverrideRetryLimit=0&SwitchGetToPostLimit=50000&contextValue=%2Foam&password=secure_string&challenge_url=https%3A%2F%2Fwww.snl.com%2Fweb%2Fclient%3Fauth%3Dinherit&request_id=-2343654539289081584&authn_try_count=0&locale=en_GB&resource_url=https%253A%252F%252Fwww.snl.com%252Finteractivex%252Fdefault.aspx')
        time.sleep(4)
        login()
    except:
        driver.close()
        start()

def login():
    try:
        time.sleep(10)
        username = driver.find_element_by_css_selector("input.form-control.input-sm.snl-widgets-input-text.snl-selectable.action[name=username]")
        password = driver.find_element_by_css_selector("input.form-control.input-sm.snl-widgets-input-text.snl-selectable.action[name=password]")
        username.send_keys('user')
        password.send_keys('pass')
        login_button = driver.find_elements_by_xpath('//button[@class="btn btn-sm snl-widgets-input-button" and @type="button"]')
        login_button[6].click()
        print('You are logged in')
        navigate()
    except:
        driver.close()
        start()

def navigate():
    try:
        time.sleep(4)
        driver.get('https://platform.mi.spglobal.com/web/client?auth=inherit#markets/gasFutures?key=982fafdb-b14f-4c18-b151-75be96d6c2c5')
        time.sleep(7)
        filters = driver.find_element_by_class_name('snl-hui-filter-box-caption')
        filters.click()
        parse_filters(filters)
    except:
        driver.close()
        start()

def parse_filters(filters):
    try:
        buttons = driver.find_elements_by_xpath('//span[@class="filter-option pull-left"]')
        forward_terms = buttons[2]
        regions = buttons[3]
        parse_date()
        parse_terms(forward_terms, regions, filters)
    except:
        driver.close()
        start()

def parse_terms(forward_terms, regions, filters):
    forward_terms.click()
    terms = driver.find_elements_by_class_name('text')
    print(len(terms))
    terms = terms[1:]
    terms = [terms[0], terms[3]]
    forward_terms.click()
    for term in terms:
        try:
            forward_terms.click()
            term.click()
            parse_regions(regions, filters)
        except:
            driver.refresh()
            time.sleep(3)
            continue

def parse_regions(regions, filters):
    regions.click()
    locations = driver.find_elements_by_class_name('text')
    locations = locations[5:]
    regions.click()
    for location in locations:
        try:
            print('You are parsing', location.get_attribute('innerHTML'))
            regions.click()
            location.click()
            apply_filters(filters)
        except:
            driver.refresh()
            time.sleep(3)
            continue

def apply_filters(filters):
    apply = driver.find_element_by_id('Apply_section_1_control_20')
    apply.click()
    time.sleep(3)
    excel_download(filters)

def excel_download(filters):
    drop_down = driver.find_element_by_xpath('//a[@class="snl-three-dots-icon dropdown-toggle"]')
    drop_down.click()
    excel = driver.find_elements_by_class_name('hui-toolbutton')
    time.sleep(2)
    excel = excel[9]
    excel.click()
    filters.click()
    
def parse_date():
    driver.find_element_by_id('section_1_control_31_startdate').click()
    date_input = driver.find_element_by_css_selector('input#section_1_control_31_startdate.form-control.input-sm.single')
    time.sleep(2)
    del_date(date_input)

def del_date(date_input):
    for i in range(11):
        date_input.send_keys(u'\ue003')
    date_input.send_keys(args.date)
        
start()



