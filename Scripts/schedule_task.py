import os
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient


# Load the environment variables
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

# read environment variables
username = os.getenv('LOCAL_LOGIN_USERNAME')
password = os.getenv('LOCAL_LOGIN_PASSWORD')
# print(username, password)

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

    # ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00','15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

    pixel_locations = range(1, 1441, 60)
    # [1, 61, 121, 181, 241, 301, 361, 421, 481, 541, 601, 661, 721, 781, 841, 901, 961, 1021, 1081, 1141, 1201, 1261, 1321, 1381]

    # all the scheduled classes for each day
    Monday_classes = timetable_.find("div", id="timetable-day-event-column-0")
    Tuesday_classes = timetable_.find("div", id="timetable-day-event-column-1")
    Wednesday_classes = timetable_.find("div", id="timetable-day-event-column-2")
    Thursday_classes = timetable_.find("div", id="timetable-day-event-column-3")
    Friday_classes = timetable_.find("div", id="timetable-day-event-column-4")

    # get all the classes for each day
    classes_monday = Monday_classes.find_all("div", class_="timetable-event")
    classes_tuesday = Tuesday_classes.find_all("div", class_="timetable-event")
    classes_wednesday = Wednesday_classes.find_all("div", class_="timetable-event")
    classes_thursday = Thursday_classes.find_all("div", class_="timetable-event")
    classes_friday = Friday_classes.find_all("div", class_="timetable-event")

    """ add classes as objects to the timetable_data list"""
    for class_divs in classes_monday:
        start_time_index,end_time_index = get_index_time(class_divs, pixel_locations)
        if start_time_index == -1 or end_time_index == -1:
            continue
        start_time = timez[start_time_index]
        end_time = timez[end_time_index]
        class_name = class_divs.find("p", class_="event-title ellipsis").text # eg CS3205
        class_location_name = class_divs.find("div", class_="event-details").find("a").text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-details").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        
        class_constructer = {
            "class_name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "start_time": start_time,
            "end_time": end_time
        }

        timetable_data.append({
            "day": "Monday",
            "class": class_constructer
        })

    for class_divs in classes_tuesday:
        start_time_index,end_time_index = get_index_time(class_divs, pixel_locations)
        if start_time_index == -1:
            continue
        start_time = timez[start_time_index]
        end_time = timez[end_time_index]
        class_name = class_divs.find("p", class_="event-title ellipsis").text # eg CS3205
        class_location_name = class_divs.find("div", class_="event-details").find("a").text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-details").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        
        class_constructer = {
            "class_name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "start_time": start_time,
            "end_time": end_time
        }

        timetable_data.append({
            "day": "Tuesday",
            "class": class_constructer
        })

    for class_divs in classes_wednesday:
        start_time_index,end_time_index = get_index_time(class_divs, pixel_locations)
        if start_time_index == -1:
            continue
        start_time = timez[start_time_index]
        end_time = timez[end_time_index]
        class_name = class_divs.find("p", class_="event-title ellipsis").text # eg CS3205
        class_location_name = class_divs.find("div", class_="event-details").find("a").text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-details").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        
        class_constructer = {
            "class_name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "start_time": start_time,
            "end_time": end_time
        }

        timetable_data.append({
            "day": "Wednesday",
            "class": class_constructer
        })

    for class_divs in classes_thursday:
        start_time_index,end_time_index = get_index_time(class_divs, pixel_locations)
        if start_time_index == -1:
            continue
        start_time = timez[start_time_index]
        end_time = timez[end_time_index]
        class_name = class_divs.find("p", class_="event-title ellipsis").text # eg CS3205
        class_location_name = class_divs.find("div", class_="event-details").find("a").text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-details").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        
        class_constructer = {
            "class_name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "start_time": start_time,
            "end_time": end_time
        }

        timetable_data.append({
            "day": "Thursday",
            "class": class_constructer
        })

    for class_divs in classes_friday:
        start_time_index,end_time_index = get_index_time(class_divs, pixel_locations)
        if start_time_index == -1:
            continue
        start_time = timez[start_time_index]
        end_time = timez[end_time_index]
        class_name = class_divs.find("p", class_="event-title ellipsis").text # eg CS3205
        class_location_name = class_divs.find("div", class_="event-details").find("a").text # eg Fraser Noble 1
        class_location_google_maps_link = class_divs.find("div", class_="event-details").find("a")["href"] # eg https://www.google.com/maps/search/?api=1&query=57.1645,-2.1017
        
        class_constructer = {
            "class_name": class_name,
            "class_location_name": class_location_name,
            "class_location_google_maps_link": class_location_google_maps_link,
            "start_time": start_time,
            "end_time": end_time
        }

        timetable_data.append({
            "day": "Friday",
            "class": class_constructer
        })
    

    return timetable_data

def get_index_time(class_divs, pixel_locations) -> int:
    start_time_index,end_time_index = -1,-1
    height_value = -1
    top_value = -1
    ads = class_divs['style'] # get the style attributes
    list1 = ads.strip(' ').split(';') # divide the style attributes into a list
    for item in list1:
        key_item = item.split(':')[0].strip(' ')
        # get the value of the height attribute
        if key_item == 'height':
            height_item_value = item.split(':')[1].strip(' ') 
            height_value = int(height_item_value.strip('px')) + 1 # 59 + 601 = 660 ERROR 59 + 601 + 1 = 661 CORRECT
        if key_item == 'top': # find the top attribute
            top_item_value = item.split(':')[1].strip(' ') # get the value of the top attribute
            top_value = int(top_item_value.strip('px'))

    for i in pixel_locations:
        if top_value == i:
            start_time_index = pixel_locations.index(int(top_value))
        if top_value + height_value == i:
            end_time_index = pixel_locations.index(int(top_value + height_value))

    return start_time_index,end_time_index

def get_access_token(client_id, client_secret, tenant_id):
    authority = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }

    res = requests.post(authority, data=payload)

    if res.status_code == 200:
        print("Successfully retrieved access token")
        return res.json()['access_token']
    else:
        return None
    
def parse_timetable_data(event, day):
    # extract data from event
    class_name = event['class_name']
    class_location_name = event['class_location_name']
    class_location_google_maps_link = event['class_location_google_maps_link']
    start_time = event['start_time'] # 10:00
    end_time = event['end_time'] # 11:00

    days = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday':4
    }
    # get the current date
    current_date = datetime.now()

    # Find the day number for the input day name
    day_number = days.get(day)

    date_difference = (day_number - current_date.weekday() + 7) % 7

    new_date = current_date + timedelta(days=date_difference)

    # get the date in the correct format
    date = new_date.strftime("%Y-%m-%d") # 2024-01-21
    
    # Add leading zero to the hour if it's a single digit
    if len(start_time) == 4:
        start_time = "0" + start_time
    if len(end_time) == 4:
        end_time = "0" + end_time

    # '2024-01-21T00:00:00'
    # '2024-01-26T11:00:00'

    outlook_start_time = f"{date}T{start_time}:00"
    outlook_end_time = f"{date}T{end_time}:00"

    print(class_name, class_location_name, class_location_google_maps_link, outlook_start_time, outlook_end_time)
    return class_name, class_location_name, class_location_google_maps_link, outlook_start_time, outlook_end_time



""" Main method """
data = get_timetable_data(authenicate(username, password, URL))
client_id = "d08ae928-43ff-4fdd-8d35-ec6a76b031f4" # user_id
tenant_id = "f6b8542a-8c6e-464a-9981-64d3419c30ea"
client_secret = "XtT8Q~p4MncSfU0RisiwswkFkJejmJcHsA40vdoA"
personal_access_token = get_access_token(client_id, client_secret, tenant_id)
print(personal_access_token)
for item in data:
   class_name, class_location_name, class_location_google_maps_link, outlook_start_time, outlook_end_time=parse_timetable_data(item['class'], item['day']) 


