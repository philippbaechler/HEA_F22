# %%
from operator import index
import pandas as pd
import pytz
from datetime import datetime
from matplotlib import pyplot as plt

# %%
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Zurich'))
get_year = lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month) #inefficient
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day) #inefficient
get_day = lambda x: convert_tz(x).day
get_hour = lambda x: convert_tz(x).hour
get_day_of_week = lambda x: convert_tz(x).weekday()


# %%
def convert_to_date_time_append_to_df(df):
    df["creationDateTime"] = pd.to_datetime(df["creationDate"])
    df["startDateTime"] = pd.to_datetime(df["startDate"])
    df["endDateTime"] = pd.to_datetime(df["endDate"])
    df = df.drop(columns=["creationDate", "startDate", "endDate"])
    df["start_date"] = df["startDateTime"].map(get_date)
    df["creation_date"] = df["creationDateTime"].map(get_date)
    return df


# %% steps
steps = pd.read_csv("data/StepCount.csv")
steps = convert_to_date_time_append_to_df(steps)
steps.sample(5)
# %%
steps = steps.loc[steps["sourceName"]=="Apple Watch von Laura"]
steps_by_date = steps.groupby(["start_date"])["value"].sum().reset_index(name="total_steps")
steps_by_date = steps_by_date.rename(columns={"start_date": "date"})
print(steps_by_date.head())
print(steps_by_date.shape)


# %% restingHR
restingHR = pd.read_csv("data/RestingHeartRate.csv")
restingHR = convert_to_date_time_append_to_df(restingHR)
restingHR.sample(5)
# %%
# find double values
print("Unique Dates:", len(restingHR["start_date"].unique()))
print("Number of entries:", restingHR.shape[0])
restingHR.groupby(["start_date"]).count().sort_values(by="startDateTime")
# %%
# replace with mean of the day
restingHR_by_day = restingHR.groupby(["start_date"])["value"].mean().reset_index(name="resting_hr")
restingHR_by_day = restingHR_by_day.rename(columns={"start_date": "date"})
print(restingHR_by_day.head())
print(restingHR_by_day.shape)


# %% vo2max
vo2max = pd.read_csv("data/VO2Max.csv")
vo2max = convert_to_date_time_append_to_df(vo2max)
vo2max.sample(5)
# %% 
# replace with mean
vo2max_by_day = vo2max.groupby(["start_date"])["value"].mean().reset_index(name="vo2_max")
vo2max_by_day = vo2max_by_day.rename(columns={"start_date": "date"})
print(vo2max_by_day.head())
print(vo2max_by_day.shape)


# %% sleep
sleep = pd.read_csv("data/SleepAnalysis.csv")
sleep = convert_to_date_time_append_to_df(sleep)
sleep.sample(5)
# %% how many of each data source?
sleep.groupby(["sourceName"]).count()
# %% -> only use data from the Apple Watch
# pay attention to the special character between Apple and Watch (U+00a0)  -> maybe use AutoSleep / Apple Watch von Laura
sleep_data = sleep.loc[sleep["sourceName"]=="AutoSleep"]
sleep_data = sleep_data.loc[sleep_data["value"]=="HKCategoryValueSleepAnalysisAsleep"]
sleep_data['time_asleep'] = sleep_data['endDateTime'] - sleep_data['startDateTime']
sleep_data.head()
#%%
sleep_data_by_day = sleep_data.groupby('creationDateTime').agg(total_sleep_min=('time_asleep', 'sum'),
    bed_time=('startDateTime', 'min'), 
    wake_up_time=('endDateTime', 'max'), 
    sleep_counts=('creationDateTime','count'))
# %%
sleep_data_by_day['time_in_bed_min'] = sleep_data_by_day['wake_up_time'] - sleep_data_by_day['bed_time']
sleep_data_by_day['restless_sleep_min'] = sleep_data_by_day['time_in_bed_min'] - sleep_data_by_day['total_sleep_min']
sleep_data_by_day = sleep_data_by_day.reset_index()
sleep_data_by_day["date"] = sleep_data_by_day["creationDateTime"].map(get_date)
sleep_data_by_day = sleep_data_by_day.drop(columns=["creationDateTime"])
print(sleep_data_by_day.head())
print(sleep_data_by_day.shape)
# %% plot
# sleep_data_by_day['time_in_bed_min'] = (sleep_data_by_day['time_in_bed_min'].dt.total_seconds()/60)
# sleep_data_by_day['total_sleep_min'] = (sleep_data_by_day['total_sleep_min'].dt.total_seconds()/60)
# sleep_data_by_day[['time_in_bed_min','total_sleep_min']].plot(use_index=True)
# plt.show()


# %% active calories burned
activeEnergy = pd.read_csv("data/ActiveEnergyBurned.csv")
activeEnergy = convert_to_date_time_append_to_df(activeEnergy)
activeEnergy.sample(5)
# %%
activeEnergy_by_date = activeEnergy.groupby(["start_date"])["value"].sum().reset_index(name="calories_active")
activeEnergy_by_date = activeEnergy_by_date.rename(columns={"start_date": "date"})
print(activeEnergy_by_date.head())
print(activeEnergy_by_date.shape)

# %% basal calories burned
basalEnergy = pd.read_csv("data/BasalEnergyBurned.csv")
basalEnergy = convert_to_date_time_append_to_df(basalEnergy)
basalEnergy.sample(5)
# %%
basalEnergy_by_date = basalEnergy.groupby(["start_date"])["value"].sum().reset_index(name="calories_base")
basalEnergy_by_date = basalEnergy_by_date.rename(columns={"start_date": "date"})
print(basalEnergy_by_date.head())
print(basalEnergy_by_date.shape)


# %% respiratory rate
respiratoryRate = pd.read_csv("data/RespiratoryRate.csv")
respiratoryRate = convert_to_date_time_append_to_df(respiratoryRate)
respiratoryRate.sample(5)
# %%
respiratoryRate_by_date = respiratoryRate.groupby("creation_date").agg(
    respiratory_rate_avg=("value", "mean"),
    respiratory_rate_max=("value", "max"),
    respiratory_rate_min=("value", "min")
).reset_index()
respiratoryRate_by_date = respiratoryRate_by_date.rename(columns={"creation_date": "date"})
print(respiratoryRate_by_date.head())
print(respiratoryRate_by_date.shape)
# %%
#respiratoryRate_by_date.set_index("date")[["respiratoryRate_avg", "respiratoryRate_max", "respiratoryRate_min"]].plot()


# %% handwashing
handwashingEvent = pd.read_csv("data/HandwashingEvent.csv")
handwashingEvent = convert_to_date_time_append_to_df(handwashingEvent).drop_duplicates()
handwashingEvent["totalWashingTime"] = handwashingEvent["endDateTime"] - handwashingEvent["startDateTime"]
handwashingEvent.head(20)
# %%
handwashingEvent_by_day = handwashingEvent.groupby(["start_date"]).agg(
    hand_washing_counter=("totalWashingTime", "count"),
    hand_washing_time_sec=("totalWashingTime", "sum")
).reset_index()
handwashingEvent_by_day = handwashingEvent_by_day.rename(columns={"start_date": "date"})
handwashingEvent_by_day


# %%
df = pd.merge(steps_by_date, restingHR_by_day, on="date", how="outer")
df = pd.merge(df, vo2max_by_day, on="date", how="outer")
df = pd.merge(df, sleep_data_by_day, on="date", how="outer")
df = pd.merge(df, activeEnergy_by_date, on="date", how="outer")
df = pd.merge(df, basalEnergy_by_date, on="date", how="outer")
df = pd.merge(df, respiratoryRate_by_date, on="date", how="outer")
df = pd.merge(df, handwashingEvent_by_day, on="date", how="outer")
df.head(10)


# %%
df.to_csv("data/output/apple_data.csv")


# %%
