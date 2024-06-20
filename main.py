import requests,time,re,mydesign
from bs4 import BeautifulSoup as bsoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from art import tprint
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time, random


# Google Dorking
def start_dorking(resp):
    if resp.status_code == 200:
        soup = bsoup(resp.text, 'html.parser')
        links = soup.findAll("div", { "class" : "yuRUbf" })
        
        # If links found
        if links:
            mydesign.color_style_text(mydesign.MAGENTA,"\nLINKS FOUND\n", mydesign.BOLD)
            for link in links:
                mydesign.green_text(f"[+] {link.find('a').get('href')}")

                # To save output in a file
                with open("Saved_Links.txt", 'a') as f:
                    f.write(f"{link.find('a').get('href')}\n")
        else:
            mydesign.red_text("[i] No result found for this dork")
                
    else:
        print("-"*50)
        print(f"HTTP Response code: {resp.status_code}")
        print("-"*50)
        exit()

# Build dork
def dork_builder(dork, target):
    regex_list = ["site:", "site:*.com.*", "site:.com", "site:gov.*", "site:gov.*"]

    # Remove matching regex patterns
    for regex in regex_list:
        dork = re.sub(regex, '', dork)

    # Add the target site
    dork = dork+ " site:"+target

    return dork

# Live google dorks extraction from GHDB site
def live_dorks_extract(table_rows):
    mydesign.color_style_text(mydesign.MAGENTA,"\nLatest Google Dorks From GHDB\n",mydesign.BOLD)
    for row in table_rows:
        link_td = row.find_element(By.XPATH, ".//td[2]")  
        links = link_td.find_elements(By.TAG_NAME, "a")

        for link in links:
            mydesign.green_text(f"[+] {link.get_attribute('innerText')}")
        
    mydesign.color_style_text(mydesign.BLUE,"\nGet More: https://www.exploit-db.com/google-hacking-database\n",mydesign.UNDERLINE)

# To Avoid entering unwanted inputs
def get_numeric_choice():
    while True:
        user_choice = input("Choice >> ")

        # Check if numeric or not
        if not user_choice.isdigit() or int(user_choice) >=4:
           print("Invalid Choice")
        else:
            return int(user_choice)

if __name__ == "__main__":

    # Create a ChromeOptions object
    chrome_options = Options()

    # Add the `--headless` argument to enable headless mode
    chrome_options.add_argument("--headless")

    # Add the argument to disable logging of console messages
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
            
    # Establishing connection and crawling webpage
    # driver.get("https://free.proxy-sale.com/en/")

    # table_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div[1]/main/div[1]/div/div/div/div/div[1]')
    # list = []

    # for row in table_rows:
    #     link_td = row.find_elements(By.CLASS_NAME, "css-c524v5") 

    #     for _ in link_td:

    #         # Define a regular expression pattern for matching IP addresses
    #         pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    #         # Find all matches of IP addresses in the data
    #         ip_addresses = re.findall(pattern, _.text)

    #         # Append the extracted IP addresses
    #         for ip in ip_addresses:
    #             list.append(ip)
        
    #     print(list)

    
    tprint('DorkDive')
    print('\tv1.1')
    mydesign.cyan_text('\tBy incoggeek\n\nGithub: https://github.com/incoggeek')

    mydesign.green_text('-'*50)
    print("1. Live Dorks Extraction \n2. One-liner Dorking \n3. Custom Dorking")
    mydesign.green_text('-'*50)
    opt = get_numeric_choice()



    if opt == 1:

        try:

            # Establishing connection and crawling webpage
            driver.get("https://www.exploit-db.com/google-hacking-database/")

            # 5 Second delay to load the site properly
            driver.implicitly_wait(5)

            # Extract data from the first page
            table_rows = driver.find_elements(By.XPATH, "//table[@id='exploits-table']/tbody/tr")
            live_dorks_extract(table_rows)

        
        except requests.exceptions.RequestException:
            mydesign.yellow_text("\n[i] Please Check your internet connection!")
                
        except WebDriverException:
            mydesign.red_text("\n[!] Something wrong with web driver!")
        
        except KeyboardInterrupt:
            mydesign.red_text("\nOh, Okay :) ")
            exit()

        except Exception as e:
            mydesign.red_text(str(e))

    
    elif opt == 2:

        try:

            dork_query = input("Enter a dork >>> ")
            page = int(input("Page No. >>> "))
            
            # Session reuse to avoid too many requests
            user_agent = UserAgent().random
            session = requests.Session()

            base_url = 'https://www.google.com/search'
            headers  = {'User-Agent': user_agent}
            params   = { 'q': dork_query, 'start': page * 10, 'num':100}

            # To avoid too many requests
            time.sleep(10)
            resp = session.get(base_url, params=params, headers=headers)
            start_dorking(resp)

        except requests.exceptions.RequestException:
            mydesign.yellow_text("\n[i] Please Check your internet connection!")
                
        except WebDriverException:
            mydesign.red_text("\n[!] Something wrong with web driver!")
        
        except KeyboardInterrupt:
            mydesign.red_text("\nOh, Okay :) ")
            exit()

        except Exception as e:
            mydesign.red_text(str(e))

    
    elif opt == 3:

        try:
            # Establishing connection to search dorks
            file = input("Enter filepath >>> ")
            page = int(input("Enter page >>> "))
            target = input("Enter target domain >> ")
    

            with open(file, 'r') as file:
                for dork in file:

                    # To avoid too many requests
                    session = requests.Session()
                    user_agent = UserAgent().random
                    dork_query = dork_builder(dork,target)

                    mydesign.green_text('-'*50)
                    mydesign.color_style_text(mydesign.MAGENTA,f"\nDORK: {dork_query}\n",mydesign.BOLD)
                    mydesign.green_text('-'*50)
                    
                    base_url = 'https://www.google.com/search'
                    headers  = { 'User-Agent': user_agent}
                    params   = { 'q': dork_query, 'start': page * 10, 'num':100}

                    # To avoid too many requests
                    time.sleep(10)
                    # Response of the web server
                    resp = session.get(base_url, params=params, headers=headers)
                    start_dorking(resp)
        
        except requests.exceptions.RequestException:
            mydesign.yellow_text("\n[i] Please Check your internet connection!")
                
        except WebDriverException:
            mydesign.red_text("\n[!] Something wrong with web driver!")
        
        except KeyboardInterrupt:
            mydesign.red_text("\nOh, Okay :) ")
            exit()

        except Exception as e:
            mydesign.red_text(str(e))

