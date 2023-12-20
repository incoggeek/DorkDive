import requests,time
from bs4 import BeautifulSoup as bsoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from art import tprint
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

# One-liner dorking
def start_dorking(resp):
    if resp.status_code == 200:
        soup = bsoup(resp.text, 'html.parser')
        links = soup.findAll("div", { "class" : "yuRUbf" })
        for link in links:
            print(f"[+] {link.find('a').get('href')}")
    else:
        print("-"*50)
        print(f"HTTP Response code: {resp.status_code}")
        print("-"*50)
        exit()


# Live google dorks extraction from GHDB site
def live_dorks_extract(table_rows):
    for row in table_rows:
        link_td = row.find_element(By.XPATH, ".//td[2]")  
        links = link_td.find_elements(By.TAG_NAME, "a")

        for link in links:
            print(f"[+] {link.get_attribute('innerText')}")

def get_numeric_choice():
    while True:
        user_choice = input("Choice >> ")

        # Check if numeric or not
        if not user_choice.isdigit() or int(user_choice) >=4:
           print("invalid")
        else:
            return int(user_choice)

if __name__ == "__main__":
    
    tprint('DorkDive')
    print('\tv1.0')
    print('\tBy incoggeek')
    print('-'*50)

    print("1. Live Dorks Extraction \n2. One-liner Dorking \n3. WithFile Dorking")
    print('-'*50)
    opt = get_numeric_choice()

    if opt == 1:

        try:

            # Create a ChromeOptions object
            chrome_options = Options()

            # Add the `--headless` argument to enable headless mode
            chrome_options.add_argument("--headless")

            # Add the argument to disable logging of console messages
            chrome_options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Establishing connection and crawling webpage
            driver.get("https://www.exploit-db.com/google-hacking-database/")

            # 5 Second delay to load the site properly
            driver.implicitly_wait(5)

            # Extract data from the first page
            table_rows = driver.find_elements(By.XPATH, "//table[@id='exploits-table']/tbody/tr")
            live_dorks_extract(table_rows)
        
        except (requests.exceptions.RequestException, WebDriverException, KeyboardInterrupt) :
            print("Something went wrong!")

    
    elif opt == 2:

        try:

            dork_query = input("Enter a dork >>> ")
            page = int(input("Page No. >>> "))
            user_agent = UserAgent().random
            base_url = 'https://www.google.com/search'
            headers  = {'User-Agent': user_agent}
            params   = { 'q': dork_query, 'start': page * 10}

            resp = requests.get(base_url, params=params, headers=headers)
            start_dorking(resp)

        except (requests.exceptions.RequestException, KeyboardInterrupt):
            print("Something went wrong!")

    
    elif opt == 3:

        try:
            # Establishing connection to search dorks
            file = input("Enter filepath >>> ")
            page = int(input("Enter page >>> "))

            with open(file, 'r') as file:
                for dork in file:
                    base_url = 'https://www.google.com/search'
                    headers  = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
                    params   = { 'q': dork, 'start': page * 10}

                    # To avoid too many requests
                    time.sleep(5)
                    # Response of the web server
                    resp = requests.get(base_url, params=params, headers=headers)
                    start_dorking(resp)
        
        except (requests.exceptions.RequestException, FileNotFoundError, KeyboardInterrupt):
            print("Something went wrong!")
