from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Initialize WebDriver with options

import time
import datetime
from datetime import date,timedelta
def calculate_future_date(days_to_add):
    """
    Calculates the date a specified number of days ahead from today.
    
    Parameters:
    days_to_add (int): The number of days to add to the current date.

    Returns:
    int: The future date in YYYYMMDD format as an integer.
    """
    # Get today's date
    current_date = date.today()
    
    # Calculate the future date
    future_date = current_date + timedelta(days=days_to_add)
    
    # Format the future date as YYYYMMDD and return as an integer
    return (future_date.strftime("%m-%d-%Y"))

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 1)
driver.maximize_window()
# Navigate to the website
driver.get("https://foreupsoftware.com/index.php/booking/19348/1470#/login")

# SIGN IN ADD USERNAME/EMAIL AND PASSWORD 
wait.until(EC.presence_of_element_located((By.ID, "login_email"))).send_keys("FILL_IN_USERNAME")
wait.until(EC.presence_of_element_located((By.ID, "login_password"))).send_keys("FILL_IN_PASSWORD")
driver.find_element(By.ID, "submit_button").click()

wait.until(EC.staleness_of(driver.find_element(By.LINK_TEXT, "Reservations")))
reservations_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Reservations")))
reservations_link.click()


max_attempts= 20
attempt= 0 
time_slot_clicked=False

while attempt<max_attempts and not time_slot_clicked:
    try: 
        wait = WebDriverWait(driver, 0.1)
        book_now_button = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
)

        book_now_button.click()

        button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='btn btn-primary' and @data-value='4']") #CHANGE =4 TO DESIRED NUMBER OF PLAYERS 9(IE: FOR 3 PLAYS IT SHOULD BE =3)
    ))

        button.click()

# Input the date into the text field
        wait = WebDriverWait(driver, 1)
        date_field = wait.until(EC.presence_of_element_located((By.ID, "date-field")))
        date_field.click()
        date_field.send_keys(Keys.BACKSPACE * 10)
        date_field.clear()  
        date_field.send_keys(calculate_future_date(3)) # ADD HOW MANY DAYS IN ADVANCE 
        date_field.send_keys(Keys.ENTER)


# List of times in 9-minute intervals starting from 6:00 AM
        time_slots = [
    "6:00am", "6:09am", "6:18am", "6:27am", "6:36am", "6:45am", 
    "6:54am", "7:03am", "7:12am", "7:21am", "7:30am", "7:39am", 
    "7:48am", "7:57am", "8:06am", "8:15am", "8:24am", "8:33am", 
    "8:42am", "8:51am", "9:00am", "9:09am", "9:18am", "9:27am", 
    "9:36am", "9:45am", "9:54am", "10:03am", "10:12am", "10:21am", 
    "10:30am", "10:39am", "10:48am", "10:57am", "11:06am", "11:15am", 
    "11:24am", "11:33am", "11:42am", "11:51am", "12:00pm", "12:09pm", 
    "12:18pm", "12:27pm", "12:36pm", "12:45pm", "12:54pm", "1:03pm", 
    "1:12pm", "1:21pm", "1:30pm", "1:39pm", "1:48pm", "1:57pm", 
    "2:06pm", "2:15pm", "2:24pm", "2:33pm", "2:42pm", "2:51pm", 
    "3:00pm", "3:09pm", "3:18pm", "3:27pm", "3:36pm", "3:45pm", 
    "3:54pm", "4:03pm"]

        wait = WebDriverWait(driver, 0)
        for desired_time in time_slots:
            try:
            
                time_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//div[@class='booking-start-time-label' and text()='{desired_time}']")
                ))

                wait = WebDriverWait(driver, 1)
                clickable_element = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//div[@class='booking-start-time-label' and text()='{desired_time}']")
                ))

                clickable_element.click()
                time_slot_clicked= True
                print(f"Clicked on the first available time slot: {desired_time}")
                input("Time slot clicked. Press Enter to close the browser manually.")
                break  # Exit the loop once the first available time is clicked

            except Exception as e:
                # Log the error and try the next time slot
                print(f"Time slot {desired_time} not available. Error: {str(e)}")
        # Loop through the generated time slots
    except Exception as e: 
        driver.refresh()
        attempt += 1 
        continue

