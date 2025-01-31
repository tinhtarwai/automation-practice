from calendar import month

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(service = Service("C:/Users/A_R_T/AppData/Local/Drivers/chromedriver-win64/chromedriver.exe")) ## Chrom Driver
# driver = webdriver.Edge(service = Service("C:/Users/A_R_T/AppData/Local/Drivers/edgedriver_win64/msedgedriver.exe")) ## Edge Driver
# driver = webdriver.Firefox(service = Service("C:/Users/A_R_T/AppData/Local/Drivers/geckodriver-v0.35.0-win64/geckodriver.exe")) ## Firefox Driver

driver.get("https://super-agent-webapp-dev.herokuapp.com/")
driver.maximize_window()
# time.sleep(5)
print(driver.title)

source = Select(driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
source.select_by_visible_text("Yangon (ရန်ကုန်)")
print(len(source.options))

for source_des in source.options:
    print(source_des.text)

source = Select(driver.find_element(By.XPATH, "//select[@id='selectTo']"))
source.select_by_visible_text("Mandalay (မန္တလေး)")
print(len(source.options))

month_year = "February 2025"
date = "7"
driver.find_element(By.XPATH, "//div[@class='area-departure-date']").click()

while True:
    mon_yr = driver.find_element(By.XPATH, "//div[@id='month-year-label']").text
    if mon_yr == month_year:
        break
    else:
        driver.find_element(By.XPATH, "//div[@id='header']//div[3]").click()
days = driver.find_elements(By.XPATH, "//div[@id='day-cell']/div/div/div")

for day in days:
    if day.text == date:
        day.click()
        break

driver.find_element(By.XPATH, "//input[@id='myanmar']").click()
driver.find_element(By.XPATH, "//div[@class='area-search-button']").click()

# try:
#     # Open the target web page
#     driver.get("https://www.example.com")  # Update this URL
#
#     # Wait for the dropdown to be present
#     dropdown_locator = (By.ID, "dropdown_id")  # Use the appropriate locator for the dropdown
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located(dropdown_locator))
#
#     # Click the dropdown to reveal the search field
#     dropdown = driver.find_element(*dropdown_locator)
#     dropdown.click()
#
#     # Wait for the search input to be visible (adjust the locator as needed)
#     search_box_locator = (By.XPATH, "//input[@type='text']")  # Update to the actual search box locator
#     search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(search_box_locator))
#
#     # Type the search query into the search box
#     search_query = "Your Search Query"  # Replace with your desired search text
#     search_box.send_keys(search_query)
#
#     # Optionally, wait for the results to be filtered based on the input
#     time.sleep(2)  # Adjust as necessary
#
#     # Select the option you want; this depends on how options are rendered
#     option_locator = (By.XPATH, "//div[contains(@class, 'option-class') and text()='Desired Option']")  # Update accordingly
#     desired_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(option_locator))
#     desired_option.click()
#
# finally:
#     # Close the driver
#     driver.quit()



# driver.find_element(By.XPATH, "//small[@id='increment-icon']").click()



time.sleep(15)
# driver.close()