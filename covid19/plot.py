import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d

from termcolor import colored

from covid19.data import *

def plot_daily_cases(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    plt.plot(gaussian_filter1d(cnt["Confirmed"], sigma=2), label=c)

  plt.xlabel("Day")
  plt.ylabel("Cases")
  plt.title("Accumulated Cases Daily, since 100th case")
  plt.legend()
  fig.show()

def plot_daily_patients(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    plt.plot(gaussian_filter1d(cnt["Patients"], sigma=2), label=c)

    if c=="Thailand":
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")


  plt.figure(figno)
  plt.xlabel("Day")
  plt.ylabel("Cases")
  plt.title("Accumulated Active Patients Daily, since 100th case")
  plt.legend()
  fig.show()


def plot_daily_increment(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case

    # Movine average for smoothening
    # cnt["sma"] = 100 * cnt["new_confirmed"].rolling(window=5).mean()
    cnt.loc[:,"sma"] = 100 * gaussian_filter1d(cnt["new_confirmed"], sigma=2)
    plt.plot(cnt["sma"], label=c)

  plt.xlabel("Day")
  plt.ylabel("% Increase")
  plt.title("Case Incremental Rate %, since 100th case")
  plt.legend()
  fig.show()

def plot_recovery_rate(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    cnt.loc[:,"ratio_recovered"] = 100 * cnt["ratio_recovered"]
    plt.plot(gaussian_filter1d(cnt["ratio_recovered"], sigma=2), label=c)

  # Plot recovery pivot point (7 days)
  plt.axvline(x=7, ymin=0, ymax=100, linestyle="dotted")

  plt.xlabel("Day")
  plt.ylabel("% Recovered")
  plt.title("Percentage of recovery, since 100th case")
  plt.legend()
  fig.show()


def plot_mortal_rate(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    cnt.loc[:,"ratio_death"] = 100 * cnt["ratio_death"]
    plt.plot(gaussian_filter1d(cnt["ratio_death"], sigma=2), label=c)

    if c=="Thailand":
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Day")
  plt.ylabel("% Mortal")
  plt.title("Mortal rate, since 100th case")
  plt.legend()
  fig.show()


def plot_mortal_over_recovery_rate(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    plt.plot(gaussian_filter1d(cnt["ratio_death/rec"], sigma=1), label=c)

    if c=="UK":
      # Draw an arrow pointing at UK's latest spot
      x = cnt.tail(1).index.tolist()[0]
      y = cnt.tail(1)["ratio_death/rec"].tolist()[0]
      plt.annotate("UK", xy=(x,y), xytext=(x-3,y+5), arrowprops=dict(arrowstyle="->"))

    if c=="Thailand":
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Day")
  plt.ylabel("Mortal / Recovery")
  plt.title("Ratio of mortal over recovery, since 100th case")
  plt.legend()
  fig.show()


if __name__ == '__main__':
  """
  Usage:
  
    python3 -m covid19.plot {PATH_TO_COVID19_GIT_REPOPATH}

  """
  path = sys.argv[-1]
  print(colored("Loading daily cases from : ","cyan"), path)
  
  # Load and wrangle daily report data
  daily   = load_daily_cases(path)
  wranged = wrang_data(daily)
  step    = make_daily_step(wranged)

  step = step.reset_index(drop=False)

  countries = ["Thailand","Germany","Italy","France","UK","South Korea"]

  # Configure matplot
  # NOTE: Font can be inspected by
  # 
  # > import matplotlib.font_manager
  # > matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
  #
  plt.rcParams['font.sans-serif'] = ['HatchwayM'] + plt.rcParams['font.sans-serif']

  # Plot
  # plot_daily_cases(1, step, countries)
  plot_daily_patients(2, step, ["Thailand","Germany", "South Korea", "UK", "Italy"])
  plot_daily_increment(3, step, countries)
  plot_recovery_rate(4, step, countries + ["US"])
  plot_mortal_rate(5, step, countries + ["US"])
  plot_mortal_over_recovery_rate(6, step, ["Thailand","Italy","France","US","UK"])
  input("Press RETURN to end ...")