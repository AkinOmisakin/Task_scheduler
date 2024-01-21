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
    # ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
    # '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

    pixel_locations = range(1, 1441, 60)
    list(pixel_locations)
    time_index = 0
    # [1, 61, 121, 181, 241, 301, 361, 421, 481, 541, 601, 661, 721, 781, 841, 901, 961, 1021, 1081, 1141, 1201, 1261, 1321, 1381]

    # all the scheduled classes for each day
    Monday_classes = timetable_.find("div", id="timetable-day-event-column-0") ; print(Monday_classes)

    """ This section of code is used to get the time of the first class on Monday ( for example purposes only)"""
    # ads = Monday_classes['style']
    # list1 = ads.strip(' ').split(';')
    # for item in list1:
    #     key_item = item.split(':')[0].strip(' ')
    #     if key_item == 'top':
    #         print("key found")
    #         key_item_value = item.split(':')[1].strip(' ')
    #         key_item_value = key_item_value.strip('px')
    #         if key_item_value in pixel_locations:
    #             print("value found")
    #             time_index = pixel_locations.index(int(key_item_value))
    #     else:
    #         print("key not found")
    # time_of_monday_class = timez[time_index]

    Tuesday_classes = timetable_.find("div", id="timetable-day-event-column-1") ; print(Tuesday_classes)
    Wednesday_classes = timetable_.find("div", id="timetable-day-event-column-2") ; print(Wednesday_classes)
    Thursday_classes = timetable_.find("div", id="timetable-day-event-column-3") ; print(Thursday_classes)
    Friday_classes = timetable_.find("div", id="timetable-day-event-column-4") ; print(Friday_classes)

    # get all the classes for each day
    classes_monday = Monday_classes.find_all("div", class_="timetable-event"); print(classes_monday)
    classes_tuesday = Tuesday_classes.find_all("div", class_="timetable-event") ; print(classes_tuesday)
    classes_wednesday = Wednesday_classes.find_all("div", class_="timetable-event") ; print(classes_wednesday)
    classes_thursday = Thursday_classes.find_all("div", class_="timetable-event") ; print(classes_thursday)
    classes_friday = Friday_classes.find_all("div", class_="timetable-event") ; print(classes_friday)

    # get class name and type of class
    class_constructer = []

    for class_divs in classes_monday:
        time_idx = get_index_time(class_divs, pixel_locations)
        time_of_monday_class = timez[time_idx]
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "class_time": time_of_monday_class
        }
        timetable_data.append({
            "day": "Monday",
            "class": class_constructer #
        })

    for class_divs in classes_tuesday:
        time_idx = get_index_time(class_divs, pixel_locations)
        time_of_tuesday_class = timez[time_idx]
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "class_time": time_of_tuesday_class
        }
        timetable_data.append({
            "day": "Tuesday",
            "class": class_constructer
        })

    for class_divs in classes_wednesday:
        time_idx = get_index_time(class_divs, pixel_locations)
        time_wednesday_class = timez[time_idx]
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "class_time": time_wednesday_class
        }
        timetable_data.append({
            "day": "Wednesday",
            "class": class_constructer #
        })
    for class_divs in classes_thursday:
        time_idx = get_index_time(class_divs, pixel_locations)
        time_thursday_class = timez[time_idx]
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "class_time": time_thursday_class
        }
        timetable_data.append({
            "day": "Thursday",
            "class": class_constructer
        })

    for class_divs in classes_friday:
        time_idx = get_index_time(class_divs, pixel_locations)
        time_friday_class = timez[time_idx]
        class_name = class_divs.find("p", class_="event-title  ellipsis").text # eg CS3205
        class_type = class_divs.find("span").text # eg Lecture
        class_name = " ".join([class_name, class_type]) # eg CS3205 Lecture
        class_location_name = class_divs.find("div", class_="event-details").find("a")["href"].text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-location").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        class_constructer = {
            "class name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "class_time": time_friday_class
        }
        timetable_data.append({
            "day": "Friday",
            "class": class_constructer
        })
    
    print(timetable_data)

    return timetable_data

def get_index_time(class_divs, pixel_locations):
    ads = class_divs['style'] # get the style attributes
    list1 = ads.strip(' ').split(';') # divide the style attributes into a list
    for item in list1:
        key_item = item.split(':')[0].strip(' ')
        if key_item == 'top': # find the top attribute
            print("key found")
            key_item_value = item.split(':')[1].strip(' ') # get the value of the top attribute
            key_item_value = key_item_value.strip('px')
            if key_item_value in pixel_locations: # find the index of the top attribute value in the pixel_locations list
                print("value found")
                time_index = pixel_locations.index(int(key_item_value))
        else:
            print("key not found")
    return time_index

""" This method parses the timetable data and schedules the classes"""
def parse_timetable_data(timetable_data):
    pass

def schedule_classes(email, password, task, date, time):
    print("Scheduling task...")


""" Main method """
#authenicate(username, password, URL)
data = get_timetable_data(authenicate(username, password, URL))
#print(data)
#parse_timetable_data(data)
# pixel_locations = range(1, 1441, 60)
# list(pixel_locations)
# print(pixel_locations[10])
parse_timetable_data(data)
