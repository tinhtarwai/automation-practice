import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    service=Service("C:/Users/A_R_T/AppData/Local/Drivers/chromedriver-win64/chromedriver.exe"))  ## Chrom Driver
# driver = webdriver.Edge(service = Service("C:/Users/A_R_T/AppData/Local/Drivers/edgedriver_win64/msedgedriver.exe")) ## Edge Driver
# driver = webdriver.Firefox(service = Service("C:/Users/A_R_T/AppData/Local/Drivers/geckodriver-v0.35.0-win64/geckodriver.exe")) ## Firefox Driver

driver.get("https://super-agent-webapp-dev.herokuapp.com/")
driver.maximize_window()
print(driver.title)

# choose a source location
source = Select(driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
source.select_by_visible_text("Yangon (ရန်ကုန်)")
print("\nTotal available destination in 'From' field : ", len(source.options))

# get all destination in From field
for source_des in source.options:
    print(source_des.text)

# choose a destination location
destination = Select(driver.find_element(By.XPATH, "//select[@id='selectTo']"))
destination.select_by_visible_text("Mandalay (မန္တလေး)")
print("\nTotal available destination in 'To' field : ", len(destination.options))

# select a departure date
month_year = "February 2025"
date = "8"
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

# driver.find_element(By.XPATH, "//button[@id='increment-counter']").click() # increase seat count to 2

count_display = driver.find_element(By.XPATH, "//span[@id='countDisplay' and not(contains(@class, 'text-muted'))]").text # get total selected seat count (eg. 2 seats)
# print(count_display)
seat_count = int(count_display.split()[0]) # 2
print("\nTotal selected seat : ", seat_count, " seat(s)")

driver.find_element(By.XPATH, "//input[@id='myanmar']").click() # select radio button of Local Traveler (Myanmar Nationality)
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='area-search-button']").click() # click on Search Now button
time.sleep(2)
print("\n\t** Trip Search is working fine")
# select the first trip of Trip results List
try:
    sel_trip = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//body[1]//div[@class='area-action']//a[span[contains(text(),'Select Trip')]])[1]"))
    )
    if sel_trip.is_displayed():
        # print("\nElement is present and clickable")
        sel_trip.click()
    else:
        print("\nElement is not displayed.")
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(2)
print("\n\t** Select Trip is working fine")
# choose the first available seat from seat plan (1 seat)
driver.find_element(By.XPATH, "(//table//tbody//tr/td//a[@data-seat-number])[1]").click()

#choose the first available seats (more than 1 seat)

# for seat in range(1, seat_count+1):
#     driver.find_element(By.XPATH, f"(//table//tbody//tr/td//a[@data-seat-number])[{seat}]").click()
#
driver.find_element(By.XPATH, "//div[@class='card-body border-top']//button[@type='submit' and @class='btn btn-primary btn-block seatSelectionSubmitButton']").click() # click "Continue To Traveler" button
time.sleep(2)
print("\n\t** Seat Selection is working fine")

# Fill traveler info fields and submit
time.sleep(2)


driver.find_element(By.XPATH, "//input[@id='name']").send_keys('test auto')
# driver.find_element(By.XPATH, "//input[@id='radio-MIXED']").click()
driver.find_element(By.XPATH, "//input[@id='radio-FEMALE_ONLY']").click()

driver.find_element(By.XPATH, "//input[@id='phoneNumber']").send_keys('09979964737')
driver.find_element(By.XPATH, "//input[@id='email']").send_keys('tinhtarwai106330@gmail.com')
driver.find_element(By.XPATH, "//input[@id='specialRequest']").send_keys('This is a test request for automation testing practice')
time.sleep(2)
driver.find_element(By.XPATH, "//button[@id='traveller-info-submit-button']").click()
print("\n\t** Traveler Info section is working fine")
time.sleep(2)
# select Mock Pay from payment list
try:
    mock_pay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='Mock Pay']"))
    )
    if mock_pay.is_displayed():
        print("\nMock pay is present and clickable")
        mock_pay.click()
    else:
        print("\nElement is not displayed.")
except Exception as e:
    print(f"An error occurred: {e}")
time.sleep(2)

driver.find_element(By.XPATH,"//div[@class='bg-light p-2 clickable-area']").click() # click on 'Promo code' section to apply

try:
    promo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Promo Code']"))
    )
    if promo.is_displayed():
        print("\nPromo field is displayed")
        promo.send_keys('tdg2000')
except Exception as e:
    print(f"An error occurred: {e}")

try:
    apply_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Apply']"))
    )
    if apply_btn.is_displayed():
        print("\nApply promo code btn is present and clickable")
        apply_btn.click()
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(3)
driver.find_element(By.XPATH, "//a[normalize-space()='Proceed To Pay']").click() # click "Proceed To Pay" button

# wait for new page loading (uat pay link)
try:
    pin_box = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='meaningOfLife']"))
    )
    print("Payment page loaded successfully.")
    pin_box.send_keys('whatever')
except Exception as e:
    print(f"An error occurred while waiting for the new payment page: {e}")

driver.find_element(By.XPATH, "//button[normalize-space()='Pay Now']").click()
print("\n\t** Payment process is working fine")

# redirect to merchant page
try:
    return_to_mer = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Return to Merchant']"))
    )
    return_to_mer.click()
except Exception as e:
    print(f"An error occurred while redirecting to merchant page")

# redirect to booking complete page
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='success-text']"))
    )
    print("Your Booking process is successful and confirmed.")
except Exception as e:
    print(f"An error occurred while redirecting to booking complete page.")

time.sleep(10 )
# driver.close()
