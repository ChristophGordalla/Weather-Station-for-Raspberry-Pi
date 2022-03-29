# Weather Station for Raspberry Pi

## Project Description

This project shows how to set up the software part of a weather station for a Raspberry Pi. It handles temperature, pressure, and humidity data that is measured every 15 minutes from sensors attached to the Pi and generates plots from it. 

### Web Server Content

The web page shows the measured data at the last measurement time. Furthermore plots are displayed that show different quantities depending on the time periods that they represent: 

* Last 24 hours: plots for temperature, sea level pressure, and relative humidity
* Last 7 days: plots for temperature, sea level pressure
* Last 31 days: a plot showing the minimum, average, and maximum temperature all at once, as well as a plot of the sea level pressure
* Last 365 days: a plot showing the minimum, average, and maximum temperature all at once, as well as a plot of the sea level pressure

### Mail Notifications

Each night at 00:05 o'clock, an image with the weather data from the day before is sent by mail.

## Hardware

The project has been tested on a Raspberry Pi B+ and a Raspberry Pi 4. The following sensors have been used:

* BMP085 for pressure and temperature measurements
* AM2321 for humidity measurements.

## Software Prerequisites

* Install Python 3 with Matplotlib.
* Install the libraries needed for your sensors (in my case BMP085 and AM2321).
* Set up a web server on your Pi. This could e.g. be an `nginx` or an `apache2` server. 

## Files and Usage

Configurations and sensor acquisition files. *Adjust them to your needs!*

* `acqui.py`: Acquires data and writes them to files. 
* `config.py`: Project configuration.
* `config_mail.py`: Mail configuration, split from `config.py` because it contains sensitive information.

Main file, must have executable permissions:

* `main.py`: Main file to execute various tasks of the project. Run this script with one of the following parameters: `./main.py continuous` for continuous data acquisition or `./main.py daily` to generate and send plots from the weather data of the day before.

Other project files:

* `constants.py`: Defines all non-configurable constants. 
* `mail.py`: Sends the images by mail.
* `plot.py`: Generates the images to be displayed or sent.
* `reader.py`: Reads data from the data files.
* `utils.py`: Class-independent utility functions for the project.
* `writer.py`: Writes data to the data files.

## Project Setup

Adjust the settings in `config.py` to your needs, especially take a looks at the paths and create them if necessary. 

Modify the code in `acqui.py` if you are using different sensors than those mentioned above.

Give execution permissions to `main.py` (by `chmod +x main.py`) and add the following lines to your crontab (entering `crontab -e` will open your crontab in an editor):

```
*/15 * * * * <PATH/TO/PROJECT>/./main.py continuous 
5 0 * * * <PATH/TO/PROJECT>/./main.py daily
```

The first line will make sure to acquire data every 15 minutes, the second line will send an email with a plot of last day's data every day at 00:05 o'clock.
