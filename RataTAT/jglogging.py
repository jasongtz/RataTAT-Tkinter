#! /usr/bin/python
### CURRENT STATUS AND LOGGER

import csv, time, datetime
import datetime as dt

#	DAILYDATA CSV FUNCTIONS 

# Creates the blank template of the current status log - only needed for debugging
def create_log():
	with open("log.csv", "w+") as blank:
		topline = [str(dt.date.today()), 1]
		header = ["Batteries", "Displays", "Calibrating", "Calibration Failures"]
		startvalues = [0, 0, 0, 0]
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(topline)
		writer.writerow(header)
		writer.writerow(startvalues)
		writer.writerow(startvalues)

def csvhourlyupdate():
	# Shows (time minus 1 hour) to current time. Eg "10:00 - 11:00"
	times = str(int(time.strftime("%H")) - 1) + ":" + time.strftime("%M") + " - " + \
		time.strftime("%H:%M")
	with open("dailydata.csv", "a") as f:
		writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow([times, readgenius(), gethourlylog()[0], \
			gethourlylog()[2], gethourlylog()[3]])
	# Writes the hourly values back to 0
	writehourlylog([0, 0, 0, 0])

# csv_autolog() uses csvhourlyupdate() from above and runs it once per hour.
# This function is imported and ran by an exterior Python file, csvonly.py.

def csv_autolog():
    from modularui import handover
    while True:
		now = dt.datetime.now()

		#if now.hour == 23:
		if now.minute == 5:
			handover()
			time.sleep(3600)
		
		elif 7 < now.hour < 23:		
			if now.minute == "00":
			    csvhourlyupdate()
			    time.sleep(60)
			else:
				time.sleep(60)
		else:
			time.sleep(60)


##### DUPLICATE CODE from modularui file #######
def readlogfile():
	"""Opens the log file, returns a list where each line of the csv is a list."""
	with open("log.csv", "rb") as file:
		return [row for row in csv.reader(file)]  # List comprehension

def readgenius():
	"""Reads the cell of log.csv where the current number of Geniuses is stored."""
	return int(readlogfile()[0][1])
##### END DUPLICATE ######

def gethourlylog():
	return [int(numbers) for numbers in readlogfile()[3]]
	
def writehourlylog(values):
    status = readlogfile()
    status[3] = values
    with open("log.csv", "wb") as file:
		for num in range(4):
			csv.writer(file, delimiter=",").writerow(status[num])
