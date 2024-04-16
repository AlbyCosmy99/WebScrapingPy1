from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
service = webdriver.ChromeService()
options = webdriver.ChromeOptions()

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
        page_start_ups = WebDriverWait(driver, seconds_wait).until(
            EC.presence_of_all_elements_located((By.ID, "searchResults"))
        )
        discover_button = WebDriverWait(page_start_ups[i], SECONDS_WAIT).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ui button rounded  black']"))
        )
        driver.execute_script("arguments[0].click();", discover_button[i])
        location = WebDriverWait(driver, SECONDS_WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ui grid']//div[@class='twelve wide column']//h2"))
        )
        my_list.append(location.text)
        driver.back()
        i = i + 1

def pages_available(driver):
    try:
        last_page_icon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to last page"]'))
        )
        driver.execute_script("arguments[0].click();", last_page_icon)   
        pages_count = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]'))
        )
        last_num_pages = pages_count.text.split("\n")
        last_num_page = last_num_pages[len(last_num_pages)-1]

        first_page_icon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to first page"]'))
        )
        driver.execute_script("arguments[0].click();", first_page_icon) 

        print(last_num_page)
        return last_num_page
    except:
        return 1 #there is only one page available

if HEADLESS:
    options.add_argument('--headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.add_argument('--disable-extensions')
    
driver = webdriver.Chrome(service=service,options=options)
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

    #1-github
    #2-estrarre informazioni startup per ogni pagina di lista startup
    #3-andare a vedere numero massimo pagine e mettere un limite in un if su number of pages
    #4-estrarre le informazioni desiderate dopo il test del punto 2
    while(number_of_page < pages):  
        forward_icon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to next page" and @rel="next"]'))
        )
        driver.execute_script("arguments[0].click();", forward_icon)    
        print('Page: ' + str(number_of_page))

        scrap_page_start_up(driver,SECONDS_WAIT, start_ups)
        number_of_page = number_of_page + 1
finally:
    driver.close()
