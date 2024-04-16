from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
]


service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
random_user_agent = random.choice(user_agents)
options.add_argument(f'user-agent={random_user_agent}')
options.add_argument('--disable-extensions')

SECONDS_WAIT = 5

HEADLESS = False

def scrap_page_start_up(driver, seconds_wait, my_list):
    time.sleep(1)
    page_start_ups = WebDriverWait(driver, seconds_wait).until(
        EC.presence_of_all_elements_located((By.ID, "searchResults"))
    )

    length = len(page_start_ups)
    i = 0
    while i < length:
        try:
            discover_button = WebDriverWait(driver, SECONDS_WAIT).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ui button rounded  black']"))
            )
            driver.execute_script("arguments[0].click();", discover_button[i])
            location = WebDriverWait(driver, SECONDS_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='ui header']"))
            )
        except:
            print('error detected.')
            continue
        my_list.append(location.text)
        print(location.text)
        i = i + 1
        driver.back()  

def pages_available(driver, seconds_wait=10):
    try:
        last_page_icon = WebDriverWait(driver, seconds_wait).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to last page"]'))
        )
        driver.execute_script("arguments[0].click();", last_page_icon)
        
        WebDriverWait(driver, seconds_wait).until(
            EC.staleness_of(last_page_icon)
        )

        pages_count = WebDriverWait(driver, seconds_wait).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]'))
        )
        last_num_pages = pages_count.text.split("\n")
        last_num_page = int(last_num_pages[-1]) 

        first_page_icon = WebDriverWait(driver, seconds_wait).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to first page"]'))
        )
        driver.execute_script("arguments[0].click();", first_page_icon)

        print("Total pages: " + str(last_num_page))
        return last_num_page
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if HEADLESS:
    options.add_argument('--headless')
    
driver = uc.Chrome(service=service,options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get('https://startup.registroimprese.it/isin/home')


try:
    elem = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_element_located((By.ID, "filtroAvanzatoLnk"))
    )
    elem.click()
    region_dropdown = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_element_located((By.ID, "valueRegione"))
    )
    region_dropdown.click()
    regions_name = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='menu transition visible']//div[@class='item']//span"))
    )

    for region in regions_name:
        option_text = region.text
        option_to_select = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_element_located((By.XPATH, f"//div[@class='menu transition visible']//span[text()=\"{option_text}\"]"))
        )
        driver.execute_script("arguments[0].click();", option_to_select) 

    search_btn = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "searchBtnVetrina"))
    )
    driver.execute_script("arguments[0].click();", search_btn)

    start_ups = []

    number_of_page = 1
    print('Page: ' + str(number_of_page))
    pages = pages_available(driver)

    scrap_page_start_up(driver,SECONDS_WAIT, start_ups)

    while(number_of_page < int(pages)):  
        forward_icon = WebDriverWait(driver, SECONDS_WAIT).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to next page" and @rel="next"]'))
        )
        driver.execute_script("arguments[0].click();", forward_icon)    
        number_of_page = number_of_page + 1
        print('Page: ' + str(number_of_page))
        scrap_page_start_up(driver,SECONDS_WAIT, start_ups)     
finally:
    
    driver.close()