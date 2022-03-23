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
def convert_to_date_time_append_to_df(df, field):
    df[field] = pd.to_datetime(df[field])
    # df['year'] = df[field].map(get_year)
    # df['month'] = df[field].map(get_month)
    df['date'] = df[field].map(get_date)
    # df['day'] = df[field].map(get_day)
    # df['hour'] = df[field].map(get_hour)
    # df['dow'] = df[field].map(get_day_of_week)
    return df


# %% steps
steps = pd.read_csv("data/StepCount.csv")
steps = convert_to_date_time_append_to_df(steps, "startDate")
steps.sample(5)
# %%
steps_by_date = steps.groupby(["date"])["value"].sum().reset_index(name="Steps")
print(steps_by_date.head())
print(steps_by_date.shape)


# %% restingHR
restingHR = pd.read_csv("data/RestingHeartRate.csv")
restingHR = convert_to_date_time_append_to_df(restingHR, "startDate")
restingHR.sample(5)
# %%
# find double values
print("Unique Dates:", len(restingHR["date"].unique()))
print("Number of entries:", restingHR.shape[0])
restingHR.groupby(["date"]).count().sort_values(by="startDate")
# %%
# replace with mean of the day
restingHR_by_day = restingHR.groupby(["date"])["value"].mean().reset_index(name="Steps")
print(restingHR_by_day.head())
print(restingHR_by_day.shape)


# %% vo2max
vo2max = pd.read_csv("data/VO2Max.csv")
vo2max = convert_to_date_time_append_to_df(vo2max, "startDate")
vo2max.sample(5)
# %% 
# replace with mean
vo2max_by_day = vo2max.groupby(["date"])["value"].mean().reset_index(name="Steps")
print(vo2max_by_day.head())
print(vo2max_by_day.shape)


# %% sleep
sleep = pd.read_csv("data/SleepAnalysis.csv")
sleep["startDate"] = pd.to_datetime(sleep["startDate"])
sleep["endDate"] = pd.to_datetime(sleep["endDate"])
sleep["creationDate"] = pd.to_datetime(sleep["creationDate"])
sleep["date"] = sleep["startDate"].map(get_date)
sleep.sample(5)
# %% how many of each data source?
sleep.groupby(["sourceName"]).count()
# %% -> only use data from the Apple Watch
# pay attention to the special character between Apple and Watch (U+00a0)  -> maybe use AutoSleep / Apple Watch von Laura
sleep_data = sleep.loc[sleep["sourceName"]=="AutoSleep"]
sleep_data = sleep_data.loc[sleep_data["value"]=="HKCategoryValueSleepAnalysisAsleep"]
sleep_data['time_asleep'] = sleep_data['endDate'] - sleep_data['startDate']
sleep_data.head()
#%%
sleep_data = sleep_data.groupby('creationDate').agg(total_time_asleep=('time_asleep', 'sum'),
    bed_time=('startDate', 'min'), 
    awake_time=('endDate', 'max'), 
    sleep_counts=('creationDate','count'))
# %%
sleep_data['time_in_bed'] = sleep_data['awake_time'] - sleep_data['bed_time']
sleep_data['restless_time'] = sleep_data['time_in_bed'] - sleep_data['total_time_asleep']
sleep_data = sleep_data.reset_index()
sleep_data["date"] = sleep_data["creationDate"].map(get_date)
sleep_data.head()
# %% plot
sleep_data['time_in_bed'] = (sleep_data['time_in_bed'].dt.total_seconds()/60)
sleep_data['total_time_asleep'] = (sleep_data['total_time_asleep'].dt.total_seconds()/60)
sleep_data[['time_in_bed','total_time_asleep']].plot(use_index=True)
plt.show()


# %% active calories burned
activeEnergy = pd.read_csv("data/ActiveEnergyBurned.csv")
activeEnergy = convert_to_date_time_append_to_df(activeEnergy, "startDate")
activeEnergy.sample(5)
# %%
activeEnergy_by_date = activeEnergy.groupby(["date"])["value"].sum().reset_index(name="activeEnergy")
activeEnergy_by_date.head()


# %%
