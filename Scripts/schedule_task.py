import os
import sys
import requests
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions, ChromeService
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
"""
testing
# create webdriver object
driver = webdriver.Chrome()
# get google.co.in
driver.get(URL)
get_username = driver.find_element(By.ID,"username")
get_password = driver.find_element(By.ID,"password")
get_username.send_keys(username)
get_password.send_keys(password)
sign_in = driver.find_element(By.ID,"login")
sign_in.click()
#opts = ChromeOptions()
"""
def authenicate(username, password, url):

    login_url = url 

    # login_payload = {
    #     "username": username,
    #     "password": password,
    # }

    driver = webdriver.Chrome()

    driver.get(login_url)

    get_username = driver.find_element(By.ID,"username")
    get_password = driver.find_element(By.ID,"password")

    # input username and password into the input fields
    get_username.send_keys(username)
    get_password.send_keys(password)

    # clicking the sign in button
    sign_in = driver.find_element(By.ID,"login")
    sign_in.click()
    
    cookies = driver.get_cookies() 

    sess = requests.Session()

    for cookie in cookies:
        sess.cookies.set(cookie['name'], cookie['value'])

    res= sess.get("https://www.abdn.ac.uk/mytimetable/timetable/myTimetable")
    if check_status(res) is None:
        return None
    else:
        print(res.text)
    
    driver.quit()


        
def check_status(response) -> None:
    if response.status_code == 200:
        print("Successfully logged in!")
    else:
        print(f"Error!, status code {response.status_code}")
        return None
    
def schedule_classes(email, password, task, date, time):
    print("Scheduling task...")

authenicate(username, password, URL)
