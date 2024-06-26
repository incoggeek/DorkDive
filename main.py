import requests,time,re,mydesign
from bs4 import BeautifulSoup as bsoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from art import tprint
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
 
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

    # Get the list of proxies from the API
    response = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text')

    # Check if the request was successful
    if response.status_code == 200:
    # Split the response text into a list of proxies
        proxy_list = response.text.strip().split('\n')
        
        # Create a dictionary to store the proxies
        proxies_dict = {}
        # Parse each proxy and add to the dictionary with the same address as key and value
        for proxy in proxy_list:
            proxy = proxy.strip()  # Remove any leading/trailing whitespace
            if proxy:
                # Use the same address for key and value
                proxies_dict[proxy] = proxy
    
    else:
        print(f"Failed to retrieve proxies: {response.status_code}")

    # Create a ChromeOptions object
    chrome_options = Options()

    # Add the `--headless` argument to enable headless mode
    chrome_options.add_argument("--headless")

    # Add the argument to disable logging of console messages
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

    # Tool Banner
    
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
            
            # \To avoid too many requests
            user_agent = UserAgent().random

            base_url = 'https://www.google.com/search'
            headers  = {'User-Agent': user_agent}
            params   = { 'q': dork_query, 'start': page * 10, 'num':100}

            # To avoid too many requests
            time.sleep(10)
            resp = requests.get(base_url, params=params, headers=headers,proxies=proxies_dict)
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
                    resp = requests.get(base_url, params=params, headers=headers,proxies=proxies_dict)
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

