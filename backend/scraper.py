 # backend/scraper.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def final_diagnostic_test():
    url = "https://www.naukri.com/python-developer-jobs"

    print("--- STARTING FINAL DIAGNOSTIC TEST ---")
    print("Setting up the browser...")

    options = webdriver.ChromeOptions()
    # We force the browser to be visible
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    print(f"Opening URL: {url}")
    driver.get(url)
    time.sleep(5) # Give page 5 seconds to load anything

    print("\n--- ACTION REQUIRED ---")
    print("The Chrome browser window is now open and will stay open.")
    print("Please look at it carefully.")
    
    # This line will pause the entire script until you press Enter
    input("===> After you have examined the page, press Enter in this terminal to close the browser and end the script... ")

    driver.quit()
    print("--- TEST COMPLETE ---")

if __name__ == "__main__":
    final_diagnostic_test()