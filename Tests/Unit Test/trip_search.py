import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Tests.Utils.webdriver_setup import get_driver, open_url

class TestTripSearch (unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        open_url(self.driver, "https://super-agent-webapp-dev.herokuapp.com/")
        self.test_failed = False

    # test for empty value in source location
    def test_empty_source(self):
        source = self.driver.find_element(By.XPATH, "//select[@id='selectFrom']")
        self.driver.find_element(By.XPATH, "//div[@class='area-search-button']").click()  # click on Search Now button
        validation_message = self.driver.execute_script("return arguments[0].validationMessage;", source)
        self.assertEqual(validation_message, "Please select an item in the list.",
                         "Validation message is different with specification.")
        if not self.test_failed:
            print("Test passed : Proper error message is displayed when source location field is empty.\n")
        time.sleep(3)

    # test for empty value in destination location
    def test_empty_destination(self):
        source = Select(self.driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
        source.select_by_visible_text("Yangon (ရန်ကုန်)")

        destination = self.driver.find_element(By.XPATH, "//select[@id='selectTo']")
        self.driver.find_element(By.XPATH, "//div[@class='area-search-button']").click()  # click on Search Now button
        validation_message = self.driver.execute_script("return arguments[0].validationMessage;", destination)
        self.assertEqual(validation_message, "Please select an item in the list.",
                         "Validation message is different with specification.")
        if not self.test_failed:
            print("Test passed : Proper error message is displayed when destination location field is empty.\n")
        time.sleep(3)

    # check for invalid input in source or destination fields
    def test_invalid_input(self):
        source = self.driver.find_element(By.XPATH, "//span[@title='From']")
        source.click()
        search_key = self.driver.find_element(By.XPATH, "//input[@role='searchbox']")
        search_key.send_keys("Yannn")
        empty_result = self.driver.find_element(By.XPATH, "//ul[@id='select2-selectFrom-results']//li").text
        print(f"Message for empty result in 'From' field : {empty_result}")
        self.assertEqual(empty_result, "No results found", "Message for no result is different with specification.")
        time.sleep(2)
        source.click() # click again to quit
        time.sleep(2)
        destination = self.driver.find_element(By.XPATH, "//span[@title='To']")
        destination.click()
        search_key = self.driver.find_element(By.XPATH, "//input[@role='searchbox']")
        search_key.send_keys("Mannnn")
        empty_result = self.driver.find_element(By.XPATH, "//ul[@id='select2-selectTo-results']").text
        print(f"Message for empty result in 'To' field : {empty_result}")
        self.assertEqual(empty_result, "No results found", "Message for no result is different with specification.")
        if not self.test_failed:
            print("Test passed : Proper validation message is displayed for no result matched with search keyword.\n")

        time.sleep(3)

    # test for empty value in departure date
    def test_empty_depart_date(self):
        source = Select(self.driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
        source.select_by_visible_text("Yangon (ရန်ကုန်)")
        destination = Select(self.driver.find_element(By.XPATH, "//select[@id='selectTo']"))
        destination.select_by_visible_text("Mandalay (မန္တလေး)")
        self.driver.find_element(By.XPATH, "//div[@class='area-search-button']").click()  # click on Search Now button
        time.sleep(3)
        depart_date = self.driver.find_element(By.XPATH, "//div[@class='area-departure-date']")
        # validation_message = self.driver.execute_script("return arguments[0].validationMessage;", depart_date)
        validation_message = self.driver.execute_script("""
            var form = document.querySelector('form');
            if (!form.checkValidity()) {
                // Find the first invalid field
                var invalidField = form.querySelector(':invalid');
                return invalidField ? invalidField.validationMessage : 'No validation message found';
            }
            return 'Form is valid';
        """)
        # print(validation_message)
        self.assertEqual(validation_message, "Please fill out this field.",
                         "Validation message is different with specification.")
        if not self.test_failed:
            print("Test passed : Proper error message is displayed when departure date field is empty.\n")
        time.sleep(3)

    # test for not choosing Nationality field
    def test_not_choosing_nationality(self):
        source = Select(self.driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
        source.select_by_visible_text("Yangon (ရန်ကုန်)")
        destination = Select(self.driver.find_element(By.XPATH, "//select[@id='selectTo']"))
        destination.select_by_visible_text("Mandalay (မန္တလေး)")
        month_year = "February 2025"
        date = "15"
        self.driver.find_element(By.XPATH, "//div[@class='area-departure-date']").click()
        while True:
            mon_yr = self.driver.find_element(By.XPATH, "//div[@id='month-year-label']").text
            if mon_yr == month_year:
                break
            else:
                self.driver.find_element(By.XPATH, "//div[@id='header']//div[3]").click()
        days = self.driver.find_elements(By.XPATH, "//div[@id='day-cell']/div/div/div")
        for day in days:
            if day.text == date:
                day.click()
                break

        self.driver.find_element(By.XPATH, "//div[@class='area-search-button']").click()
        time.sleep(3)

        # nationality = self.driver.find_element(By.XPATH, "//div[@class='area-nationality d-flex']")
        # validation_message = self.driver.execute_script("return argument[0].validationMessage;", nationality)

        validation_message = self.driver.execute_script("""
                    var form = document.querySelector('form');
                    if (!form.checkValidity()) {
                        // Find the first invalid field
                        var invalidField = form.querySelector(':invalid');
                        return invalidField ? invalidField.validationMessage : 'No validation message found';
                    }
                    return 'Form is valid';
                """)
        self.assertEqual(validation_message, "Please select one of these options.", "Validation message is different with specification.")
        if not self.test_failed:
            print("Test passed : Proper error message is displayed for not choosing nationality.")

    # check the maximum and minimum count of seat
    def test_max_seat_count(self):
        exp_max_seat = 4

        plus_btn = self.driver.find_element(By.XPATH, "//button[@id='increment-counter']")
        while not plus_btn.get_attribute("disabled"):
            plus_btn.click()
        count_display = self.driver.find_element(By.XPATH,"//span[@id='countDisplay' and not(contains(@class, 'text-muted'))]").text
        seat_count = int(count_display.split()[0])
        self.assertEqual(seat_count, exp_max_seat, f"Maximum seat count {seat_count} is not the same with system's specification." )
        if not self.test_failed:
            print(f"Test passed : Maximum seat count {seat_count} is the same with system's specification.")

    def test_min_seat_count(self):
        exp_min_seat = 1

        plus_btn = self.driver.find_element(By.XPATH, "//button[@id='increment-counter']")
        while not plus_btn.get_attribute("disabled"):
            plus_btn.click()
        time.sleep(2)
        minus_btn = self.driver.find_element(By.XPATH, "//button[@id='decrement-counter']")
        while not minus_btn.get_attribute("disabled"):
            minus_btn.click()
        count_display = self.driver.find_element(By.XPATH, "//span[@id='countDisplay' and not(contains(@class, 'text-muted'))]").text
        seat_count = int(count_display.split()[0])
        self.assertEqual(seat_count, exp_min_seat,
                         f"Minimum seat count {seat_count} is not the same with system's specification.")
        if not self.test_failed:
            print(f"Test passed : Minimum seat count {seat_count} is the same with system's specification.")

    # check for selecting same location in source and destination fields
    def test_choose_same_location(self):
        source = Select(self.driver.find_element(By.XPATH, "//select[@id='selectFrom']"))
        source.select_by_visible_text("Yangon (ရန်ကုန်)")
        source_loc = self.driver.find_element(By.XPATH, "//span[@id='select2-selectFrom-container']").text
        destination = self.driver.find_element(By.XPATH, "//span[@title='To']")
        destination.click()

        # find the location in the list which is disabled
        disabled_loc = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span//ul[@id='select2-selectTo-results']//li[@aria-disabled='true']"))
        )

        if source_loc in disabled_loc.text:
            is_disabled = disabled_loc.get_attribute("aria-disabled")
            self.assertEqual(is_disabled, "true", "Test failed : Same location is still clickable.")
            if not self.test_failed:
                print("Test Passed: Same location is disabled and not clickable.")
            else:
                try:
                    disabled_loc.click()
                    time.sleep(3)
                    print("Test failed : Same location is still clickable.")
                except Exception as e:
                    print("Test Passed: Same location is disabled and not clickable.")

    # check for searching with valid inputs

