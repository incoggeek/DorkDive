import requests, time
from bs4 import BeautifulSoup as bsoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from art import tprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# One-liner dorking
def one_liner_dork(resp):
    soup = bsoup(resp.text, 'html.parser')
    links = soup.findAll("div", { "class" : "yuRUbf" })
    for link in links:
        print(f"[+] {link.find('a').get('href')}")


# Live google dorks extraction from GHDB site
def live_dorks_extract(table_rows):
    for row in table_rows:
        link_td = row.find_element(By.XPATH, ".//td[2]")  
        links = link_td.find_elements(By.TAG_NAME, "a")

        for link in links:
            print(f"[+] {link.get_attribute('innerText')}")


# Dorking with file
def upload_dorks_file(file,search_box):

    try:
        # Open the file in read mode
        with open(file, 'r') as file:
             for line in file:

                # Passing file's text line by line to search box
                search_box.send_keys(line.strip())

                 # Simulate pressing the Enter key to perform the search
                search_box.send_keys(Keys.RETURN)

                # Wait for a moment to see the results (you might want to use WebDriverWait for more complex scenarios)
                driver.implicitly_wait(5)

                # Capture the search results
                search_results = driver.find_elements(By.TAG_NAME,"cite")

                for link in search_results:
                    print(f"[+] {link.text.strip()}")
                
        # # Click the "Next" button and repeat the process for the next pages
        # while True:
        #     try:

        #         next_button = WebDriverWait(driver, 20).until(
        #         EC.f((By.CLASS_NAME, "//*[@id='botstuff']/div/div[3]/div[4]/a[1]"))
        #         )
        #         print("Next button is interactable:", next_button.is_enabled())

        #         next_button.click()

        #         time.sleep(2)  # Adjust this sleep time based on your page load time

        #         # Capture the search results
        #         search_results = driver.find_elements(By.TAG_NAME,"cite")
        #         for link in search_results:
        #             print(f"[+] {link.get_attribute('innerText')}")


        #     except Exception as e:
        #         print(e)
        #         break

        # Close the browser window
        driver.quit()

    except FileNotFoundError:
        print(f"File not found: {file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    
    tprint('DorkDive')
    print('\tv1.0')
    print('\tBy incoggeek')

    # Create a ChromeOptions object
    chrome_options = Options()

    # Add the `--headless` argument to enable headless mode
    chrome_options.add_argument("--headless")

    # Add the argument to disable logging of console messages
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

    print("1. Live Dorks Extraction \n2. One-liner Dorking \n3. WithFile Dorking")

    opt = int(input("\nChoose an option: "))

    if opt == 1:
        
        # Establishing connection and crawling webpage
        driver.get("https://www.exploit-db.com/google-hacking-database/")

        # 5 Second delay to load the site properly
        time.sleep(5)
        # Extract data from the first page
        table_rows = driver.find_elements(By.XPATH, "//table[@id='exploits-table']/tbody/tr")
        live_dorks_extract(table_rows)
    
    elif opt == 2:

        query = input("Enter a dork: ")
        base_url = 'https://www.google.com/search'
        headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
        params   = { 'q': query, 'start': 10}

        resp = requests.get(base_url, params=params, headers=headers)
        one_liner_dork(resp)

    
    elif opt == 3:

        # Establishing connection to search dorks
        driver.get("https://www.google.com/")

        # 5 Second delay to load the site properly
        time.sleep(5)

        # Take file path as input from the user
        file = input("Enter the path to the file: ")
        
        # Search box
        one_liner_dork_box = driver.find_element(By.XPATH,"//*[@id='APjFqb']")
        upload_dorks_file(file,one_liner_dork_box)
    else:
        print("Invalid options")
