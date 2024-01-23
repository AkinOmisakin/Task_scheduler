
import os
from Scripts.Scrap_timetable import authenicate, get_timetable_data, parse_timetable_data
from datetime import datetime


if __name__ == "__main__":
    
    URL="https://www.abdn.ac.uk/mytimetable/sessions/login"

    # Load the environment variables
    # dotenv_path = Path('./.env')
    # load_dotenv(dotenv_path=dotenv_path)

    username = os.getenv('LOCAL_LOGIN_USERNAME')
    password = os.getenv('LOCAL_LOGIN_PASSWORD')

    # print(username, password)

    data = get_timetable_data(authenicate(username, password, URL))

    for Class in data:
        class_name, class_location_name, class_location_google_maps_link, outlook_start_time, outlook_end_time = parse_timetable_data(
                                                                                                                    Class['class'],
                                                                                                                    Class['day'])
        
    