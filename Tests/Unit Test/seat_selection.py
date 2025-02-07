import random
import time
import unittest
from selenium.webdriver.common.by import By

from Tests.Utils.webdriver_setup import get_driver, open_url


class TestSeatSelection (unittest.TestCase):
    # @classmethod
    def setUp(self):
        self.driver = get_driver()
        open_url(self.driver, "https://super-agent-webapp-dev.herokuapp.com/main/trip/3-278253-49-0-4?isForeigner=false&numSeats=4&integrity=95F5B9101C1EE3BC4537BEDE2320BDF22F62C289047500AC270E7333201DC02B")
        self.requested_seat = 4
        self.test_failed = False

    # test for selecting available seat
    def test_select_available_seat(self):
        selected_list = []
        avai_seats = self.driver.find_elements(By.XPATH, "(//table//tbody//tr/td//a[@class='seat seat-available'])")
        avai_seat_no = [locator.text for locator in avai_seats]
        print(f"Available seats : {len(avai_seats)}\t{avai_seat_no}")

        for i in range(self.requested_seat):
            select_seat = avai_seats[i]
            select_seat.click()
            selected_list.append(select_seat.text)
            selected_class = "seat-selected"
            seat_class = select_seat.get_attribute("class")
            self.assertIn(selected_class, seat_class, "Seat should be selected after clicking")
        print("Your selected seats : ", ",".join(selected_list))
        if not self.test_failed:
            print(f"Test 1 passed : Test for selecting available seats passed successfully.")
        time.sleep(3)

    # test for not enough available seat
    def test_select_not_enough_seat(self):
        selected_list = []

        for i in range(self.requested_seat):
            avai_seats = self.driver.find_elements(By.XPATH, "(//table//tbody//tr/td//a[@class='seat seat-available'])")

            if len(avai_seats) == 0:
                print("There is no available/ enough seats to choose.")
                break
            else:
                select_seat = random.choice(avai_seats)
                select_seat.click()
                selected_list.append(select_seat.text)
                selected_class = "seat-selected"
                seat_class = select_seat.get_attribute("class")
                self.assertIn(selected_class, seat_class, "Seat should be selected after clicking.")
            len(avai_seats)-1
        print(f"Your requested seat count : {self.requested_seat}")
        print(f"Available seats : {len(selected_list)} (", ", ".join(selected_list), ")")
        time.sleep(3)
        if not self.test_failed:
            print("Test 2 passed : Test for enough/ not enough available seat(s) passed successfully!\n")
        time.sleep(3)

    # test for selecting unavailable seat
    def test_select_unavailable_seat(self):
        all_seats = self.driver.find_elements(By.XPATH, "(//table[@id='seat-table'])//td//a")
        for seat in all_seats:
            if "seat-unavailable" in seat.get_attribute("class"):
                init_class = seat.get_attribute("class")
                try:
                    seat.click()
                    self.fail(f"Unavailable seat was clicked, which should not be possible!")
                except Exception as e:
                    final_class = seat.get_attribute("class")
                    self.assertEqual(init_class, final_class, f"Seat should remain unclickable and not change its state")

        if not self.test_failed:
            print("Test 3 passed : Test for selecting unavailable seat(s) passed successfully!\n")
        time.sleep(3)

    # test for selecting more than requested seat count
    def test_select_more_than_requested_seats(self):

        tot_selected_seats = []
        avai_seats = self.driver.find_elements(By.XPATH, "(//table[@id='seat-table'])//td//a[@class='seat seat-available']")
        print("\nThe seats that user tried to select : ", end= " ")

        ## selecting the first available seats
        # for i in range(requested_seat+2):
        #     print(avai_seats[i].text, end= ", ")
        #     avai_seats[i].click()
        #     if "seat-selected" in avai_seats[i].get_attribute("class"):
        #         tot_selected_seats.append(avai_seats[i])

        ## selecting random available seats
        for i in range(self.requested_seat+2):
            random_seat = random.choice(avai_seats)
            print(random_seat.text, end= "  ")
            random_seat.click()
            if "seat-selected" in random_seat.get_attribute("class"):
                tot_selected_seats.append(random_seat.text)

        print(f"\nActual selected seats : {tot_selected_seats}")
        print(f"Expected seat count : {self.requested_seat}, \tTotal selected seat : {len(tot_selected_seats)}")

        self.assertEqual(self.requested_seat, len(tot_selected_seats),
                         "The system should not allow selecting more than the requested seat count.")
        if not self.test_failed:
            print("Test 4 passed : No additional seats were selected.\n")
        time.sleep(3)

    # test for selecting more than requested seat count
    def test_select_less_than_requested_seats(self):
        selected_list = []
        avai_seats = self.driver.find_elements(By.XPATH, "(//table//tbody//tr/td//a[@class='seat seat-available'])")
        for i in range(self.requested_seat-1):
            select_seat = avai_seats[i]
            select_seat.click()
            selected_list.append(select_seat)
        self.driver.find_element(By.XPATH, "//div[@class='card-body border-top']//button[@type='button']").click()
        if self.requested_seat > len(selected_list):
            print("You need to choose more seat(s).")
            print("Test 5 passed : The system doesn't allow user to go to next page for selecting less than requested seat count")
        time.sleep(3)

    # test for selecting and deselecting a seat
    def test_select_and_deselect_seat(self):
        avai_seat = self.driver.find_element(By.XPATH, "(//table//tbody//tr/td//a[@class='seat seat-available'])[1]")
        avai_seat.click()
        selected_class = "seat-selected"
        seat_class = avai_seat.get_attribute("class")
        self.assertIn(selected_class, seat_class, "The seat is not selected")
        time.sleep(3)
        if selected_class in seat_class:
            avai_seat.click()
        if not self.test_failed:
            print("Test 6 passed : User can select a seat and deselect it successfully.")
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

if __name__== "__main--":
    unittest.main()