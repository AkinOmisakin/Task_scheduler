import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv



# Load the environment variables
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

# read environment variables
username = os.getenv('LOCAL_LOGIN_USERNAME')
password = os.getenv('LOCAL_LOGIN_PASSWORD')
print(username, password)

# login_url
URL="https://www.abdn.ac.uk/mytimetable/sessions/login"

""" This method signs into the mytimetable portal and returns a session object"""
def authenicate(username, password, url):

    login_url = url 

    driver = webdriver.Chrome()

    try:
        driver.get(login_url)

        get_username = driver.find_element(By.ID,"username")
        get_password = driver.find_element(By.ID,"password")

        # input username and password into the input fields
        get_username.send_keys(username)
        get_password.send_keys(password)

        # clicking the sign in button
        sign_in = driver.find_element(By.ID,"login")
        sign_in.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loggedinuserinfo"))
        )

        print("Successfully logged in!")
        return driver

    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
    
""" Webscrapes dynamically loaded timetable data from the mytimetable portal"""   
def get_timetable_data(driver):

    # wait for the page to load
    driver.implicitly_wait(10)
    
    # get the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # holds all the timetable data
    timetable_data = []

    # holds all the class times
    timez = []

    timetable_ = soup.find("div", id="timetable")

    # get all the class times
    time_entries = timetable_.find("div", id="timetable-timeblock-header")

    for times in time_entries:
        timez.append(times.text)
    print(timez)

    # all the scheduled classes for each day
    #todays_classes = timetable_entries.find_all("div", class_="timetable-day-column today")
    Monday_classes = soup.find("div", id="timetable-day-event-column-0") ; print(Monday_classes)
    Tuesday_classes = timetable_.find("div", id="timetable-day-event-column-1") ; print(Tuesday_classes)
    Wednesday_classes = timetable_.find("div", id="timetable-day-event-column-2") ; print(Wednesday_classes)
    Thursday_classes = timetable_.find("div", id="timetable-day-event-column-3") ; print(Thursday_classes)
    Friday_classes = timetable_.find("div", id="timetable-day-event-column-4") ; print(Friday_classes)

    # get all the classes for each day
    classes_monday = Monday_classes.find_all("div", class_="timetable-event")
    classes_tuesday = Tuesday_classes.find_all("div", class_="timetable-event")
    classes_wednesday = Wednesday_classes.find_all("div", class_="timetable-event")
    classes_thursday = Thursday_classes.find_all("div", class_="timetable-event")
    classes_friday = Friday_classes.find_all("div", class_="timetable-event")

    # get class name and type of class
    class_constructer = []

    for class_divs in classes_monday:
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })

    for class_divs in classes_tuesday:
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })

    for class_divs in classes_wednesday:
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })
    for class_divs in classes_thursday:
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })

    for class_divs in classes_friday:
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })
    
    print(timetable_data)

    return timetable_data, timez

""" This method parses the timetable data and schedules the classes"""
def parse_timetable_data(timetable_data, time_data):
    pass

def schedule_classes(email, password, task, date, time):
    print("Scheduling task...")


""" Main method """
#authenicate(username, password, URL)
data,time_data = get_timetable_data(authenicate(username, password, URL))
#print(data)
#parse_timetable_data(data)
