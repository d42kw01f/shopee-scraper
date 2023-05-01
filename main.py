from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import pandas as pd
from selenium.webdriver.common.keys import Keys

for page in range(0,4):
    print(page)
    # create object for chrome options
    chrome_options = Options()
    base_url = f'https://shopee.sg/hpofficialshop?page={page}&sortBy=pop'
    print(base_url)
    print('**********************************************************************************************************************************************************************************')

    # set chrome driver options to disable any popup's from the website
    # to find local path for chrome profile, open chrome browser
    # and in the address bar type, "chrome://version"
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('user-data-dir=/home/unknown/Documents/Shopee/Chrome_user_data')
    # To disable the message, "Chrome is being controlled by automated test software"
    chrome_options.add_argument("disable-infobars")
    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2
        })
    # invoke the webdriver
    browser = webdriver.Chrome(executable_path = r'/usr/bin/chromedriver',
                            options = chrome_options)
    browser.get(base_url)
    delay = 5 #secods


    # declare empty lists
    item_cost, item_init_cost, item_loc = [],[],[]
    item_name, items_sold, discount_percent = [], [], []
    link_arr, title_arr, cpu_arr = [], [], []
    try:
        WebDriverWait(browser, delay)
        print ("Page is ready")
        sleep(5)
        # Get the height of the webpage
        height = browser.execute_script("return document.body.scrollHeight")

        # Slowly scroll down the webpage
        for i in range(0, height, 100):
            browser.execute_script("window.scrollTo(0, {});".format(i))
            sleep(0.1)
        sleep(3)
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        #print(html)
        soup = BeautifulSoup(html, "html.parser")

        # find_all() returns an array of elements. 
        # We have to go through all of them and select that one you are need. And than call get_text()
        print('\n')
        for item_n in soup.find_all('a', {'data-sqe': 'link'}):
            link = item_n.get('href')
            link = f'https://shopee.sg{link}'
            title = item_n.get_text()
            print(title)
            print(link)
            print()
            print('----')
            print()
            link_arr.append(link)
            title_arr.append(title)
            # browser1 = webdriver.Firefox()
            # browser1.get(link)
            # WebDriverWait(browser1, delay)
            # sleep(5)

            # html_1 = browser1.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            # soup_1 = BeautifulSoup(html_1, "html.parser")
            
            # all_specs = soup_1.find('div', class_='MCCLkq')
            # cpu = ''
            # try:
            #     for specs in all_specs.find_all('div', class_='dR8kXc'):
            #         spec = specs.find('label', class_='zquA4o eqeCX7')
            #         if spec:
            #             if spec.get_text() == 'Processor Type':
            #                 print(specs.find('div').get_text())
            #                 cpu = specs.find('div').get_text()
            # except:
            #     print('\t\t\t----> ', link)

            # cpu_arr.append(cpu)
            # browser1.close()
            # browser1.quit()
        df = pd.DataFrame({"Link" : link_arr, "Title": title_arr})
        df.to_csv(f'shopee-{page}.csv', index=False)
        browser.close()
        browser.quit()

    except TimeoutException:
        print ("Loading took too much time!-Try again")


    # close the automated browse
