#%%
# pip install selenium
# sudo apt install chromium-chromedriver

import imp
import sys
from numpy import empty
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import re
import time
import datetime
import pandas as pd

import credentials


#%%
opts = webdriver.ChromeOptions()
# opts.add_argument('--headless')

#%%

def log_in():
    driver = webdriver.Chrome(options=opts)

    driver.get("https://connect.garmin.com/signin/")
    driver.implicitly_wait(1)
    driver.switch_to.frame("gauth-widget-frame-gauth-widget")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'login-btn-signin')))

    element = driver.find_element(By.ID, "username")
    element.send_keys(credentials.USER_NAME)
    element = driver.find_element(By.ID, "password")
    element.send_keys(credentials.PWD)
    element = driver.find_element(By.ID, "login-btn-signin")
    element.send_keys(Keys.RETURN)

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME("header-nav-link"))))
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "header-nav-link")))

    return driver

#%%
driver = log_in()
time.sleep(5)

#%%
def get_resting_heart_rate_bpm(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'HeartRateCardMain_wrapper')]")
        return re.findall(r'In\sRuhe\s\n([0-9]+)\sbpm', element.text)[0]
    except:
        return pd.NA


def get_vo2_max_and_training_load(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'TrainingStatusCard')]")
        return re.findall(r'VO2\sMax\s\n([0-9]+)\nBelastung\s\n([0-9]+)', element.text)[0]
    except:
        return pd.NA, pd.NA


def get_calories(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'CaloriesCardMain')]")
        return re.findall(r'In\sRuhe\s\n([0-9]+,?[0-9]+)\nAktiv\s\n([0-9]+,?[0-9]+)', element.text)[0]
    except:
        return pd.NA, pd.NA


def convert_to_minutes(time):
    if time == "--":
        return 0
    result = 0
    if len(time.split(" ")) == 2:
        hours, minutes = time.split(" ")
        if hours != "":
            hours = int(hours.split("h")[0])
            result += hours * 60
    else:
        minutes = time
    if minutes != "":
        minutes = int(minutes.split("m")[0])
        result += minutes
    return result


def get_sleep_data(driver):
    total_sleep, deep_sleep, light_sleep, rem_sleep, awake_sleep = pd.NA,pd.NA,pd.NA,pd.NA,pd.NA
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'SleepCard')]")
        sleep_times = re.findall(r'(.*)Tief\s(.*)Leicht\s(.*)REM\s(.*)Wach\s(.*)$', element.text.replace("\n", ""))[0]
        total_sleep = convert_to_minutes(sleep_times[0])
        deep_sleep = convert_to_minutes(sleep_times[1])
        light_sleep = convert_to_minutes(sleep_times[2])
        rem_sleep = convert_to_minutes(sleep_times[3])
        awake_sleep = convert_to_minutes(sleep_times[4])
    except:
        print("error in get_sleep_data")
    return total_sleep, deep_sleep, light_sleep, rem_sleep, awake_sleep



#%%
start_date = datetime.date(2021, 7, 1)
end_date = datetime.date(2021, 12, 31)
delta = datetime.timedelta(days=1)

data = []

while start_date <= end_date:
    print(start_date)
    driver.get("https://connect.garmin.com/modern/daily-summary/" + str(start_date))

    # print(driver.execute_script('return document.readyState;'), end=" ")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, u"//button[contains(@class, 'MenuBtn')]"))) #Menu_StandardMenuBtn

    rhr = get_resting_heart_rate_bpm(driver)
    vo2_max, training_load = get_vo2_max_and_training_load(driver)
    cal_rest, cal_activ = get_calories(driver)
    total_sleep, deep_sleep, light_sleep, rem_sleep, awake_sleep = get_sleep_data(driver)
    
    data.append({"date": start_date, "rhr": rhr, "vo2_max": vo2_max, \
        "training_load": training_load,  "cal_rest": cal_rest, "cal_activ": cal_activ, \
        "total_sleep": total_sleep, "deep_sleep": deep_sleep, "light_sleep": light_sleep, \
        "rem_sleep": rem_sleep, "awake_sleep": awake_sleep})

    start_date += delta

df = pd.DataFrame(data)
print(df.head())

#%%
df.to_csv("garmin_data.csv")







#%%
driver.close()