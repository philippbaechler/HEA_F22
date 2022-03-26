# HEA_F22

Folder structure should look like:

```
HEA_F22/
    apple/
        apple_health_extractor.ipynb
        data/
            ActiveEnergyBurned.csv
            ActivitySummary.csv
            AppleExerciseTime.csv
            ...
    garmin/
        crawler.py
        credentials.py
        data/
            garmin_data_1-Apr-21_30-Jun-21.csv
            garmin_data_1-Jan-21_31-Mar-21.csv
            garmin_data_1-Jan-22_28-Feb-22.csv
            ...
```

---

## Apple Sport Watch



---

## Garmin Sport Watch




### Rrequired Tools:

1. pip install pandas 
2. pip install selenium
3. sudo apt install chromium-chromedriver


### Usage:

1. Add a credentials.py with your garmin login.

        PWD = "MySuperPassword"
        USER_NAME = "my.super@email.com"

2. ...

---

## Data fields explanation: 

| feature name | unit | explanation | availability |
| ------------ | ---- | ----------- | ------------ |
| date | string | **Date** of the summary in format yyyy-mm-dd. | garmin & apple |
| resting_hr | 1/min | **Resting heart rate (rhr)** is the heart rate of a person in resting state and measured usually in the morning just before getting up. It allows to compare athletes and make assumptions about the health conditions. A lower rhr can be related to better training level (bigger heart). While a sharp rising rhr might be an indicator for emerging disease. | garmin & apple |
| vo2_max | ml / (kg * min) | **Maximum Oxigen Uptake** expresses how much oxygen an ahtlete is capable to take up and burn per minute. To normalize this value it is divided through the body weight of the induvidual. This value is a abstraction of the athletes trainings state. The higher this value, the more energy can be burned. | garmin & apple |
| training_load | - | **Training load** is a summary of the training intensity during the last seven days. Garmin rates the exercises based on hearth rate / variability, oxigen saturation, speed and weight of the athlete. | garmin |
| calories_base | cal | **Calories** which the athlete burnes during the day excluding sporty activities. | garmin & apple |
| calories_active | cal | **Calories** burned during sporty activities. | garmin & apple |
| time_in_bed_min | min | **Time** the person spent in bed. | garmin & apple |
| total_sleep_min | min | Total **Time** spent sleeping during the last night. | garmin & apple |
| deep_sleep_min | min | **Time** spent in deep sleep phase. | garmin |
| light_sleep_min | min | **Time** spent in light sleep phase. | garmin |
| rem_sleep_min | min | **Time** spent in rapid eye movement (rem) phase. | garmin |
| restless_sleep_min | min | **Time** spent awake during the sleep time. E.g. going to the toilet. | garmin & apple |
| low_intensity_min | min | **Time** spent with low physical activities. | garmin |
| high_intensity_min | min | **Time** spent with high physical activities. | garmin |
| total_steps | - | **Total Steps** made by the person during the day. | garmin & apple |
| stress_value | - | **Stress Value** is a summary of stress the day  | garmin |
| pause_min | min | **Time** spent relaxing or haveing a break. | garmin |
| low_stress_min | min | **Time** spent in a low stress phase. | garmin |
| medium_stress_min | min | **Time** spent in a medium stress phase. | garmin |
| high_stress_min | min | **Time** spent in a high stress phase. | garmin |
| body_battery_high | % | **Body Battery** is a measurement developped by garmin to express how exhausted a person is. This is helpful to decide how intense a training should be. E.g. if a person had a stressfull day and the body battery is low - it might be a good idea to do a low intensity traning. Hence, if the body battery is high, the person might be ready for a new or high intensity training. | garmin |
| body_battery_low | % | **Body Battery Low** is the lowest value which the person reachde during the day. Depending on the quality of sleep the battery should recharge. If you calculate the difference between the lowest and highest value (before the night and after the night) you'll get an indicator for how good the sleep was. | garmin |
| oxygen_saturation_avg | % | **Average Oxygen Saturation** during the night. | garmin |
| oxygen_saturation_minimum | % | **Minimal Oxygen Saturation** during the night. A low value could be an indicator for haveing a snoring problem. This might lead to an oxygen undersupply and in the long therm damaging the brain and other organs. | garmin |
| avg_hr_sleep | 1/min | **Average Heart Rate** during the sleep. A lower value might be an indicator for a good sleep. | garmin & "apple" |
| bed_time | time | **Time Point** when the person goes to bed. Regularity in the sleeping behaviour might have a big impact to the quality of the sleep. | garmin & apple |
| wake_up_time | time | **Time Point** when the person get up in the morning. | garmin & apple |
| sleep_counter | - | **Sleep Counter** - the apple watch recognizes when the person has a restless time during sleep. The sleep during a night is divided through these restless events. The counter simply counts how many times the person had a restless time. A high number can be associated with a low sleep quality. | apple |
| respiratory_rate_avg | 1/min | Average **Respiration Rate** during sleep. A lower value might be an indicator of a high quality sleep | apple |
| respiratory_rate_max | 1/min | Maximal **Respiration Rate** during sleep. | apple |
| respiratory_rate_min | 1/min | Minimal **Respiration Rate** during sleep. | apple |
| hand_washing_counter | - | **Hand Washing Counter** counts the times of hand washing events. | apple |
| hand_washing_time_sec | sec | **Hand Washing Time** summs up the time spent with washing hands. | apple |





 
