import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from termcolor import colored
from os import listdir
from os.path import isfile, join


def load_daily_cases(d):
  """
  Load all daily cases (CSV per date) from the containing directory
  @param d path to the directory containing daily case CSV files
  """

  def get_date(t):
    [m,d,y] = t.split(".")[0].split("-")
    return "-".join([y,m,d])

  # List all daily case files
  q = join(d, "csse_covid_19_data/csse_covid_19_daily_reports")
  csv_list = [f for f in listdir(q) if isfile(join(q, f)) and f.endswith(".csv")]
  daily = []
  for tag in csv_list:
    print(colored("Reading : ", "cyan"), tag)
    df = pd.read_csv(join(q,tag), header="infer")
    df["date"] = get_date(tag)
    daily.append(df)
  daily = pd.concat(daily)

  print(daily[:5])
  print(daily.columns)
  print(colored("Daily records read : ", "cyan"), len(daily), " rows")
  return daily


def clean_country(cnt):
  """
  Special country names:
    - Others
    - Cruise Ship
  """
  # if type(cnt)==float:
  #   return "Others"

  if cnt=="Viet Nam":
    return "Vietnam"
  if cnt=="United Kingdom":
    return "UK"
  if cnt=="Taipei and environs" or cnt=="Taiwan*":
    return "Taiwan"
  if cnt=="Republic of Korea" or cnt=='Korea':
    return "South Korea"
  if cnt=="Republic of Moldova":
    return "Moldova"
  if cnt=="Republic of Ireland":
    return "Ireland"
  if cnt=="Republic of the Congo" or cnt.startswith("Congo"):
    return "Congo"
  if cnt=="Iran (Islamic Republic of)":
    return "Iran"
  if "U.S." in cnt or "D.C." in cnt:
    return "US"

  # Clean US states
  if "(From Diamond Princess)" in cnt:
    cnt = cnt.replace("(From Diamond Princess)","")

  if len(cnt.replace('"',"").strip())==2: # state codes, eg. TX, CA
    return "US"

  return cnt.strip().replace('"','')


def wrang_data(daily):
  """
  Group data into country level (except large country like USA, China)
  Also drop unnessary column
  """
  daily = daily.iloc[:, :-1] # Drop last column (duplicate Province/State)

  daily.loc[:,"Country/Region"] = daily["Country/Region"].apply(clean_country)
  
  # Group into country level
  daily = daily.groupby(["date","Country/Region"]).agg({
    "Confirmed": "sum",
    "Deaths": "sum",
    "Recovered": "sum"
  })
  daily["Patients"] = daily["Confirmed"] - daily["Recovered"] - daily["Deaths"]

  print(colored("Daily data aggregated", "cyan"))
  print(daily)
  return daily


def make_daily_step(wranged):
  df = wranged.sort_values(by=["Country/Region","date"])
  cnt = df.groupby(["Country/Region"])

  df.loc[:,"new_confirmed"]   = cnt["Confirmed"].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
  df.loc[:,"new_patients"]    = cnt["Patients"].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
  df.loc[:,"ratio_recovered"] = df["Recovered"] / (df["Confirmed"] - df["Recovered"])
  df.loc[:,"ratio_death"]     = df["Deaths"] / (df["Confirmed"] - df["Recovered"])
  df.loc[:,"ratio_death/rec"] = df["Deaths"] / df["Recovered"]
  
  df.loc[:,"ratio_recovered"] = df["ratio_recovered"].fillna(0)
  df.loc[:,"ratio_death"]     = df["ratio_death"].fillna(0)
  df.loc[:,"ratio_death/rec"] = df["ratio_death/rec"].fillna(0)

  return df


if __name__ == '__main__':
  """
  Usage: 
    python3 -m covid19.data {PATH_TO_COVID19_GIT_REPOPATH}
  """
  path = sys.argv[-1]
  print(colored("Loading daily cases from : ","cyan"), path)
  
  daily   = load_daily_cases(path)
  wranged = wrang_data(daily)
  step    = make_daily_step(wranged)