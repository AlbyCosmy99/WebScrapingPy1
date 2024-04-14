from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

service = webdriver.ChromeService()
options = webdriver.ChromeOptions()

SECONDS_WAIT = 5

HEADLESS = True

def scrap_page_start_up(driver, seconds_wait, my_list):
    page_start_ups = WebDriverWait(driver, seconds_wait).until(
        EC.presence_of_all_elements_located((By.ID, "searchResults"))
    )
    # while page_start_ups[0].text.startswith("Traceback"):
    #     page_start_ups = WebDriverWait(driver, seconds_wait).until(
    #         EC.presence_of_all_elements_located((By.ID, "searchResults"))
    #     )
    for page_start_up in page_start_ups:
        my_list.append(page_start_up)

def check_pages_availability(driver):
    try:
        forward_icon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to next page" and @rel="next"]'))
        )
        # span = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui.pagination.menu.grid.customNavigator a > i.caret.right.icon"))
        # )
        if not forward_icon:
            return [False, None]
        elif forward_icon.get_attribute('disabled') is not None:
            return [False, forward_icon]
        else:
            print(forward_icon.get_attribute('disabled'))
            return [True, forward_icon]
    except StaleElementReferenceException:
        return [True, None]
    except TimeoutException:
        forward_icon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ui pagination menu grid customNavigator"]//a[@title="Go to next page" and @rel="next" and @disabled="disabled"]'))            
        )
        if forward_icon:
            return [False, forward_icon]

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

    scrap_page_start_up(driver,SECONDS_WAIT, start_ups)

    number_of_page = 1
    print('Page: ' + str(number_of_page))
    there_are_pages = check_pages_availability(driver)
    #1-github
    #2-estrarre informazioni startup per ogni pagina
    #3-andare a vedere numero massimo pagine e mettere un limite in un if su number of pages
    #4-estrarre le informazioni desiderate dopo il test del punto 2
    while(there_are_pages[0]):
        if there_are_pages[1] is not None:
            try:
                driver.execute_script("arguments[0].click();", there_are_pages[1])
                number_of_page = number_of_page + 1
                print('Page: ' + str(number_of_page))
                if(number_of_page == 15):
                    break
                scrap_page_start_up(driver,SECONDS_WAIT, start_ups)
            except StaleElementReferenceException:
                blank = True          
        there_are_pages = check_pages_availability(driver)
    #to do for each start up in start_ups list
    # discover_button = WebDriverWait(start_ups[0], SECONDS_WAIT).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[@class='ui button rounded  black']"))
    # )
    # driver.execute_script("arguments[0].click();", discover_button)
    # location = WebDriverWait(driver, SECONDS_WAIT).until(
    # EC.presence_of_element_located((By.XPATH, "//div[@class='ui grid']//div[@class='twelve wide column']//h2"))
    # )

    # print(location.text)

    #wait
    # region_dropdown = WebDriverWait(driver, SECONDS_WAIT).until(
    #     EC.presence_of_element_located((By.ID, "fdsfvd"))
    # )
    # region_dropdown.click()

finally:
    driver.close()
