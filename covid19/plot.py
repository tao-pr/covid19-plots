import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d

from termcolor import colored

from covid19.data import *

lockdown = {
  "France": "2020-03-17",
  "Germany": "2020-03-22",
  "Italy": "2020-03-11"
}

markers = {
  "Thailand": "red",
  "Germany": "black",
  "Italy": "teal",
  "Spain": "orange",
  "France": "blue",
  "UK": "gray",
  "US": "magenta",
  "South Korea": "maroon",
  "China": "yellow"
}

def save_fig(figno, fig):
  """
  Save a plot figure to an image, named by its figure number
  """
  fig.savefig("plots/fig-{}-AA.png".format(figno))

def plot_daily_cases(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    if max_days:
      cnt = cnt[cnt.index < max_days]
    thick = 3 if c in highlight else 1
    plt.plot(gaussian_filter1d(cnt["Confirmed"], sigma=1), label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Days from 100th case")
  plt.ylabel("Cases")
  plt.title("Accumulated Cases Daily, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)

def plot_daily_patients(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case

    if max_days:
      cnt = cnt[cnt.index < max_days]

    thick = 3 if c in highlight else 1
    plt.plot(gaussian_filter1d(cnt["Patients"], sigma=2), label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")


  plt.figure(figno)
  plt.xlabel("Days from 100th case")
  plt.ylabel("Cases")
  plt.title("Accumulated Active Patients Daily, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_daily_increment(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    if max_days:
      cnt = cnt[cnt.index < max_days]

    # Movine average for smoothening
    # cnt["sma"] = 100 * cnt["new_confirmed"].rolling(window=5).mean()
    cnt.loc[:,"sma"] = 100 * gaussian_filter1d(cnt["new_confirmed"], sigma=1)
    thick = 3 if c in highlight else 1
    plt.plot(cnt["sma"], label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Days from 100th case")
  plt.ylabel("% Increase")
  plt.title("Case Incremental Rate %, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)

def plot_recovery_rate(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    if max_days:
      cnt = cnt[cnt.index < max_days]
    cnt.loc[:,"ratio_recovered"] = 100 * cnt["ratio_recovered"]
    thick = 3 if c in highlight else 1
    plt.plot(gaussian_filter1d(cnt["ratio_recovered"], sigma=1), label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Days from 100th case")
  plt.ylabel("% Recovered")
  plt.title("Percentage of recovery, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_mortal_rate(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    if max_days:
      cnt = cnt[cnt.index < max_days]
    cnt.loc[:,"ratio_death"] = 100 * cnt["ratio_death"]
    thick = 3 if c in highlight else 1
    plt.plot(cnt["ratio_death"], label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Days from 100th case")
  plt.ylabel("% Mortal")
  plt.title("Mortal rate, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_mortal_minus_recovery_rate(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    if max_days:
      cnt = cnt[cnt.index < max_days]
    thick = 3 if c in highlight else 1
    plt.plot(cnt["ratio_death-rec"], label=c, linewidth=thick, color=markers[c])

    if c in ["Thailand"]:
      # Draw cutoff vertical line at latest case of Thailand
      x = cnt.tail(1).index.tolist()[0]
      plt.axvline(x=x, ymin=0, ymax=1000, linestyle="dotted")

  plt.xlabel("Days from 100th case")
  plt.ylabel("Ratio of (Mortal - Recovery)")
  plt.title("Mortal rate weighted by recovery, since 100th case")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_time_to_double_cases(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)

  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case

    xbasis = [100]
    while len(xbasis)<7: xbasis.append(xbasis[-1]*2)
    ybasis = []
    for ncase in xbasis:
      cases = cnt[cnt["Confirmed"]>ncase]
      if len(cases)>0:
        ndays = cases.head(1).index.tolist()[0]
        ybasis.append(ndays)
    xbasis = xbasis[:len(ybasis)]

    if c=="Thailand":
      last_confirmed = cnt["Confirmed"].tail(1).tolist()[0]
      last_ndays = cnt.tail(1).index.tolist()[0]

      # Extend the line with latest observation
      ybasis.append(last_ndays)
      xbasis.append(last_confirmed)

      strcase = "{} cases in {} days after 100th".format(
        last_confirmed,
        last_ndays)

      y = last_ndays
      x = last_confirmed
      plt.annotate(strcase, xy=(x,y), xytext=(x+20,y-5), arrowprops=dict(arrowstyle="->"))
    
    thick = 3 if c in highlight else 1
    plt.plot(xbasis, ybasis, label=c, linewidth=thick, color=markers[c])

  plt.xlabel("Number of confirms")
  plt.ylabel("Days taken")
  plt.title("Days taken to double number of cases")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_time_to_recover(figno, step, countries, max_days=None, highlight=[]):
  """
  Starting from 1th case
  """
  fig = plt.figure(figno)

  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=1)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 1st case

    xbasis = np.arange(0,1500).tolist()
    ybasis = []
    for nrecovered in xbasis:
      recov = cnt[cnt["Recovered"]>nrecovered]
      if len(recov)>0:
        ndays = recov.head(1).index.tolist()[0]
        ybasis.append(ndays)
    xbasis = xbasis[:len(ybasis)]

    if c in ["Thailand"]:
      last_recov = cnt["Recovered"].tail(1).tolist()[0]
      last_ndays = cnt.tail(1).index.tolist()[0]

      # Extend the line with latest observation
      ybasis.append(last_ndays)
      xbasis.append(last_recov)


      strcase = "{}: {:.0f} recovered in {} days".format(
        "Slowest" if c == "Thailand" else "Fastest",
        last_recov,
        last_ndays)

      y = last_ndays
      x = last_recov
      y_ = y-30 if c=="Thailand" else y+15
      plt.annotate(strcase, xy=(x,y), xytext=(x-20,y_), arrowprops=dict(arrowstyle="->"))
    
    thick = 3 if c in highlight else 1
    plt.plot(xbasis, ybasis, label=c, linewidth=thick, color=markers[c])

  plt.xlabel("Number of Recovered cases")
  plt.ylabel("Days taken")
  plt.title("Days taken to recover")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


def plot_recovery_over_days(figno, step, countries, max_days=None, highlight=[]):
  """
  Start from 100th case
  """
  fig = plt.figure(figno)

  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.loc[:,"days"] = np.arange(0, len(cnt))
    cnt.loc[:,"recover_per_day"] = cnt["Recovered"] / cnt["days"]
    cnt.loc[:,"recover_per_day"] = cnt["recover_per_day"].fillna(0)
    cnt = cnt[cnt["recover_per_day"]>0] # Cut off, starting from 1st recovery
    cnt = cnt.set_index("days")

    # Start showing from 10th day after first case
    cnt = cnt[cnt.index >= 10]

    thick = 3 if c in highlight else 1
    plt.plot(cnt["recover_per_day"], label=c, linewidth=thick, color=markers[c])

  plt.xlabel("Days")
  plt.ylabel("Avg recovered / day")
  plt.title("Average number of recovery per day")
  plt.legend()
  fig.show()
  save_fig(figno, fig)

def plot_remaining_patients_vs_confirms(figno, step, countries, max_days=None, highlight=[]):
  """
  X : number of confirm cases
  Y : ratio of outstanding patients (excluding deaths, recovered)
  """
  fig = plt.figure(figno)

  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt = cnt.set_index("Confirmed")

    thick = 3 if c in highlight else 1
    plt.plot(cnt["ratio_outstanding"]*100, label=c, linewidth=thick, color=markers[c])

    keys = {
      "Spain": "Under control",
      "Italy": "Under control",
      "Germany": "Under control",
      "South Korea": "Ending soon"
    }

    if c in keys:
      last_y = cnt["ratio_outstanding"].tail(1).tolist()[0]*100
      last_x = cnt.tail(1).index.tolist()[0]

      y_pos = last_y-15 if c=="Spain" else last_y+15
      if c=="Germany":
        y_pos += 7

      strcase = "{}: {:.0f} % left recovering".format(keys[c], last_y)
      plt.annotate(strcase,
        xy=(last_x,last_y),
        xytext=(last_x+100,y_pos), arrowprops=dict(arrowstyle="->"))

    if c in ["US"]:
      last_y = cnt["ratio_outstanding"].tail(1).tolist()[0]*100
      last_x = cnt.tail(1).index.tolist()[0]

      strcase = "Outbreak: {:.0f} % outstanding".format(last_y)
      plt.annotate(strcase, 
        xy=(last_x,last_y),
        xytext=(last_x-40000,last_y-15), arrowprops=dict(arrowstyle="->"))

  plt.xlabel("Total Confirmed Cases")
  plt.ylabel("% Remaining recovering patients")
  plt.title("Remaining COVID-19 patients in each country (Apr-12)")
  plt.legend()
  fig.show()
  save_fig(figno, fig)


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

  countries = ["Thailand","Germany","Italy","Spain","France","UK","US","South Korea"]

  # Configure matplot
  # NOTE: Font can be inspected by
  # 
  # > import matplotlib.font_manager
  # > matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
  #
  plt.style.use('seaborn') # REF: https://matplotlib.org/3.1.0/gallery/style_sheets/style_sheets_reference.html
  #plt.rcParams['font.sans-serif'] = ['HatchwayM'] + plt.rcParams['font.sans-serif']
  plt.rcParams.update({
    "figure.figsize": (10,5),
    "axes.titlesize": 15,
    "legend.fontsize": "medium"
  })

  print(plt.rcParams)

  max_days = None
  highlight = ["Thailand", "Germany"]

  excep = lambda cnt,c: list(set(cnt)-set([c]))

  # Plot
  # plot_daily_cases(1, step, countries, max_days, highlight)
  plot_daily_patients(2, step, countries, max_days, highlight)
  plot_daily_increment(3, step, countries, max_days, highlight)
  plot_recovery_rate(4, step, countries, max_days, highlight)
  plot_mortal_rate(5, step, countries, max_days, highlight)
  plot_mortal_minus_recovery_rate(6, step, countries, max_days, highlight)
  # plot_time_to_double_cases(7, step, countries, max_days, highlight)
  plot_time_to_recover(8, step, countries, max_days, highlight)
  plot_recovery_over_days(9, step, excep(countries,"UK"), max_days, highlight)
  plot_remaining_patients_vs_confirms(10.3, step, countries, max_days, highlight)
  input("Press RETURN to end ...")