# Plot Covid-19 data

Based on daily report data (https://github.com/CSSEGISandData/COVID-19).

## Origin

The project was originated as one of the [52-coding-challenges](https://github.com/tao-pr/52-challenges). I decided to spin it off here.

## Prerequisites

First of all, create a new virtual environment and install python packages by:

```bash

$ virtualenv covidenv
$ source covidenv/bin/activate
$ pip3 install -r requirements.txt
```

Clone the Covid-19 daily case data repo somewhere

```bash
$ git clone https://github.com/CSSEGISandData/COVID-19.git
```

## Generate reports

Make sure you have the virtual env activated, then do following:

```bash

$ python3 -m covid19.plot {PATH_TO_COVID19_GIT_REPOPATH}
```

For example:

```bash
$ python3 -m covid19.plot $HOME/3rd/COVID-19/
```

The program will show several plots

## Sample plots

![Days taken to double cases](plot/days-taken-to-double.png)

![Days taken to recover](plot/days-taken-to-recover.png)

![mortal over recovery rate](plot/mortal-over-recovery.png)

![Recovery per day](plot/recover-per-day.png)

## Licence

MIT

