#%%
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

    return driver


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


def get_intensity_minutes(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'IntensityMinutes')]")
        return re.findall(r'Mäßige\sIntensität\sheute\s([0-9]+)Hohe\sIntensität\sheute\s([0-9]+)', element.text.replace("\n", ""))[0]
    except:
        return pd.NA, pd.NA


def get_steps(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'StepsCard')]")
        return re.findall(r'([0-9]+,?[0-9]+)Distanz\s', element.text.replace("\n", ""))[0]
    except:
        return pd.NA


def get_stress_values(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'StressCard')]")
        stress_values = re.findall(r'([0-9]+)Pause\s(.*)Niedrig\s(.*)Mittel\s(.*)Hoch\s(.*)$', element.text.replace("\n", ""))[0]
        stress_summary = int(stress_values[0])
        pause_time_min = convert_to_minutes(stress_values[1])
        low_stress_time_min = convert_to_minutes(stress_values[2])
        medium_stress_time_min = convert_to_minutes(stress_values[3])
        high_stress_time_min = convert_to_minutes(stress_values[4])
        return stress_summary, pause_time_min, low_stress_time_min, medium_stress_time_min, high_stress_time_min
    except:
        return pd.NA, pd.NA, pd.NA, pd.NA, pd.NA


def get_body_battery_high_and_low(driver):
    try:
        element = driver.find_element(By.XPATH,u"//h2[contains(@class, 'BodyBatteryPieChart')]")
        high_value = element.text
        element = driver.find_element(By.XPATH,u"//h4[contains(@class, 'BodyBatteryPieChart')]")
        low_value = element.text
        return high_value, low_value
    except:
        return pd.NA, pd.NA


def get_SpO2_and_avg_hr(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'SleepPulseOx')]")
        SpO2_values = re.findall(r'([0-9]+)%Durchschnittlicher SpO₂([0-9]+)%Niedrigster\sSpO2([0-9]+)\sbpm', element.text.replace("\n", ""))[0]
        return SpO2_values
    except:
        return pd.NA, pd.NA, pd.NA


def get_bed_and_wakeup_times(driver):
    try:
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'sleepTimeEditor')]")
        bed_time = re.findall(r'(.*)Schlafenszeit', element.text.replace("\n", ""))[0]
        element = driver.find_element(By.XPATH,u"//div[contains(@class, 'wakeTimeEditor')]")
        wake_time = re.findall(r'(.*)Aufstehzeit', element.text.replace("\n", ""))[0]
        return bed_time, wake_time
    except:
        return pd.NA, pd.NA



#%%
driver = log_in()
time.sleep(5)


#%%
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 2, 28)
delta = datetime.timedelta(days=1)

data = []

while start_date <= end_date:
    print(start_date)

    driver.get("https://connect.garmin.com/modern/daily-summary/" + str(start_date))
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, u"//button[contains(@class, 'MenuBtn')]"))) #Menu_StandardMenuBtn

    rhr = get_resting_heart_rate_bpm(driver)
    vo2_max, training_load = get_vo2_max_and_training_load(driver)
    cal_rest, cal_activ = get_calories(driver)
    total_sleep, deep_sleep, light_sleep, rem_sleep, awake_sleep = get_sleep_data(driver)
    low_intensity_min, high_intensity_min = get_intensity_minutes(driver)
    total_steps = get_steps(driver)
    stress_val, pause_min, low_stress_min, medium_stress_min, high_stress_min = get_stress_values(driver)
    body_bat_high, body_bat_low = get_body_battery_high_and_low(driver)
    spo2_avg, spo2_min, avg_hr_sleep = pd.NA, pd.NA, pd.NA
    bed_time, wake_time = pd.NA, pd.NA

    if not pd.isna(total_sleep):
        driver.get("https://connect.garmin.com/modern/sleep/" + str(start_date) + "/pulseOx")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, u"//button[contains(@class, 'PillGroup')]"))) #Menu_StandardMenuBtn

        spo2_avg, spo2_min, avg_hr_sleep = get_SpO2_and_avg_hr(driver)
        bed_time, wake_time = get_bed_and_wakeup_times(driver)

    data.append({"date": start_date, "rhr": rhr, "vo2_max": vo2_max, \
        "training_load": training_load,  "cal_rest": cal_rest, "cal_activ": cal_activ, \
        "total_sleep": total_sleep, "deep_sleep": deep_sleep, "light_sleep": light_sleep, \
        "rem_sleep": rem_sleep, "awake_sleep": awake_sleep, "low_intensity_min": low_intensity_min, \
        "high_intensity_min": high_intensity_min, "total_steps": total_steps, \
        "stress_val": stress_val, "pause_min": pause_min, "low_stress_min": low_stress_min, \
        "medium_stress_min": medium_stress_min, "high_stress_min": high_stress_min, \
        "body_bat_high": body_bat_high, "body_bat_low": body_bat_low, "spo2_avg": spo2_avg, \
        "spo2_min": spo2_min, "avg_hr_sleep": avg_hr_sleep, "bed_time": bed_time, \
        "wake_time": wake_time})

    start_date += delta


df = pd.DataFrame(data)
print(df.head())

#%%
df.to_csv("output/garmin_data_1-Jan-22_28-Feb-22.csv")


#%%
driver.close()

# %%
