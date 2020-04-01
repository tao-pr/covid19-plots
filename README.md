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

![Sample plot](plots/fig-10-AA.png)
![Sample plot](plots/fig-2-AA.png)
![Sample plot](plots/fig-3-AA.png)
![Sample plot](plots/fig-4-AA.png)
![Sample plot](plots/fig-5-AA.png)
![Sample plot](plots/fig-6-AA.png)
![Sample plot](plots/fig-8-AA.png)
![Sample plot](plots/fig-9-AA.png)

## Licence

MIT

