#! /usr/bin/python

# MODULAR UI


##################
### TO FIX:
	# Search &&& for bugs or new features
	# Get THIS_HOUR stuff working in new class system.
	# Line 305, names importing from saved state
	

# Modules imported
import Tkinter as tk
import time
import datetime as dt
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# APPLICATION FUNCTIONAL CODE

hour_b = 0
hour_d = 0
hour_f = 0

names = [""]
genius = len(names)
current_status = []

############ NEW CONCURRENCY COMMANDS

def create_log():
	with open("log.csv", "w") as blank:
		global names
		topline = [str(dt.date.today()), names]
		header = ["Batteries", "Displays", "Calibrating", "Calibration Failures"]
		startvalues = [0, 0, 0, 0] #time.strftime("%H:%M:%S"), "", 
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(topline)
		writer.writerow(header)
		writer.writerow(startvalues)

# Rounds an integer to the nearest 15
def calc(x):
	return (int(round(x/15)) * 15)

# &&& FIXED already issue with multiple names, done
# TO FIX: Start point too low. 0.25 for bat, 0.5 for disp
# How did I do this before...?

def quote_battery(bq, dq):
	global genius
	tat = float(calc(15.0 + (((bq + dq)/genius) * 15))) / 60
	return "\n Quote %s hours." % tat
def quote_display(bq, dq, dc, df):
	global genius
	tat = float(calc((((bq + dq + dc + df) / genius) * 15 + 30))) / 60
	return "\n Quote %s hours." % tat



class Repairs(object):
	def __init__(self, index, exitmessage):
			self.index = index
			self.exitmessage = exitmessage

	def add(self):
		# Reads the log.csv, sets it into var status, adds 1 to int at self.index
		with open("log.csv", "rb") as file:
			status = [row for row in csv.reader(file)]  #List comprehension
			status[2][self.index] = int(status[2][self.index]) + 1

		with open("log.csv", "wb") as file:
			for number in range(3):
				csv.writer(file, delimiter=",").writerow(status[number])
		global current_status
		current_status = [int(numbers) for numbers in status[2]]
		if self.index == 0:
			return quote_battery(current_status[0], current_status[1])
		elif self.index == 1:
			return quote_display(current_status[0], current_status[1], \
				current_status[2], current_status[3])

	def remove(self):
		# Reads the log.csv, sets it into var status, subtracts 1 to int at self.index
		with open("log.csv", "rb") as file:
			status = [row for row in csv.reader(file)]  #List comprehension
			x = int(status[2][self.index])
			if x > 0:
				status[2][self.index] = x - 1
			else:
				return "\nError!"
		with open("log.csv", "wb") as file:
			for number in range(3):
				csv.writer(file, delimiter=",").writerow(status[number])	
		global current_status
		current_status = [int(numbers) for numbers in status[2]]
		if self.index == [3]:
			pass
		else:
			return self.exitmessage

# Instantiates all repair/movement types
battery = Repairs(0, "\nBattery complete.")
display = Repairs(1, "\nDisplay awaiting calibration.")
calib = Repairs(2, "\nDisplay complete.")
fail = Repairs(3, None)

def run_b():
	to_print.set(battery.add())
	eachactionupdate()
def run_nb():
	to_print.set(battery.remove())
	eachactionupdate()
def run_d():
	to_print.set(display.add())
	eachactionupdate()
def run_dc():
	to_print.set(display.remove()) 
	if to_print.get() == "\nError!":
		pass
	else:
		calib.add()
	eachactionupdate()
def run_df():
	fail.add()
	to_print.set("\nDisplay failed, attempt again.")
	eachactionupdate()
def run_nd():
	to_print.set(calib.remove())
	with open("log.csv", "rb") as file:
		status = [row for row in csv.reader(file)]  #List comprehension
		if int(status[2][3]) > 0:
			fail.remove()
	eachactionupdate()

def refresh():
	with open("log.csv", "rb") as file:
		status = [row for row in csv.reader(file)]  #List comprehension
		global current_status
		current_status = [int(numbers) for numbers in status[2]]
	eachactionupdate()






def hourly_log():
	global hour_d
	global hour_b
	global hour_f
	
	# Checks if hourly_log is cleared. If so: resets the hour values to zero
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
		if lines[1] == "Cleared":
			hour_d = 0
			hour_b = 0
			hour_f = 0

	# Updates the hourly log file.
	with open("hourly_log.txt", "w") as log:
		log.write(str(names) + "\n%d\n%d\n%d" % (hour_b, hour_d, hour_f))



#### DAILYDATA CSV FUNCTIONS 

## Creates the blank csv with layout info, to be called at application start.
def create_csv():
	with open("dailydata.csv", "w") as blank:
		todays_date = [str(dt.date.today())]
		header = ["Time", "Names", "Batteries", "Displays", "Calibration Failures"]
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(todays_date)
		writer.writerow(header)

# Formats the hourly progress information from hourly_log.txt,
# writes this into dailydata.csv.
def csvlog():
	done = []
	times = time.strftime("%H:%M")
	
	# Reads hourly_log.txt, each line becomes an item in the list "done".
	with open("hourly_log.txt", "r+") as log:
		done = log.readlines()
		
	# Checks if the hourly_log.txt has been cleared
	# If so, sets var hourly_data to zero values.
	# Otherwise, grabs that hour's progress to var hourly_data, and clears hourly_log.txt.
	if "Cleared" not in done:
		hourly_data = times, done[0], int(done[1]), int(done[2]), int(done[3])
		with open("hourly_log.txt", "w") as log:
			log.write(done[0] + "Cleared")
	else:
		hourly_data = times, done[0], 0, 0, 0

	# Appends the CSV with the values in hourly_data.
	with open("dailydata.csv", "a") as f:
		#declare the writing variable
		writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(hourly_data)

# csv_autolog() imports csvlog() from above and runs it once per hour.
# This function is imported and ran by an exterior Python file, csvonly.py.
def csv_autolog():
	while True:
		now = dt.datetime.now()
		if 8 < int(now.strftime("%H")) < 22:		
			if now.strftime("%M") == "00":
				csvlog()
				time.sleep(60)
			else:
				time.sleep(60)
		else:
			time.sleep(60)



### EMAIL REPORT FUNCTION

def sendreport():
	
	# Reads txt file to pull recipient and login info
	with open("emaildata.txt", "r") as file:
		data = file.readlines()
		
	recip = data[0].strip("\n")
	email = data[1].strip("\n")
	password = data[2].strip("\n")

	# Generates the message
	msg = MIMEMultipart()
	msg['Subject'] = "Modular Report for %s" % str(dt.date.today())
	msg['From'] = email
	msg['To'] = recip
	msg.preamble = "Daily report."
	msg.attach(MIMEText("Report attached."))
	file = "dailydata.csv"
	fp = open(file, "rb")
	to_attach = MIMEText(fp.read())
	fp.close()
	to_attach.add_header("Content-Disposition", "attachment", \
		 filename = "modular %s.csv" % str(dt.datetime.today()))
	msg.attach(to_attach)

	# Connects to server, sends message
	smtpserver = smtplib.SMTP('smtp.mail.me.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(email, password)
	smtpserver.sendmail(email, recip, msg.as_string())
	smtpserver.quit()


### TKINTER UI FUNCTIONAL CODE which calls from functional code above

def get_status():
	statusvar.set("\n%d batteries, %d displays awaiting repair. \nThere are %d phones "\
		 "in or awaiting calibration/testing. \n" \
		"%s repairs completed this hour.\n" % \
		(current_status[0], current_status[1], current_status[2], 645326234)) # &&&


def eachactionupdate():
	global names
	names = namevar.get().split(", ")
	global genius
	genius = len(names)

	#with open("status.txt", "a") as status:
	#	status.write(time.strftime("%H:%M:%S") + "\n" \
	#		 + tats("write") + "%s \n\n" % names)
	hourly_log()
	get_status()


# All functional buttons relocated above, near class system

def clearbutton():
	to_print.set("\n" + tats("clear"))
	eachactionupdate()
def report():
	to_print.set("\nGenerating report...")
	sendreport()
	to_print.set("\nClosing report submitted.")
def newsession():
	create_csv()
	with open("hourly_log.txt", "w") as log:
		log.write("\nCleared")
	create_log()	
def importstatus():
	global hour_d
	global hour_b
	global hour_f
	global names
	
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
		if lines[1] != "Cleared":
			# &&& Get the names importing to work - infinte loop, /""/"s etc
			names = lines[0]
			
			namevar.set(names)
			
			hour_d = int(lines[1])
			hour_b = int(lines[2])
			hour_f = int(lines[3])

	refresh()
	
# &&& To do: Import status from log.csv


### TKINTER UI APPEARANCE CODE

root = tk.Tk()
apptitle = "RataTAT v0.1"
root.wm_title(apptitle)
root.geometry("800x600")

to_print = tk.StringVar()
namevar = tk.StringVar()
title_text = tk.StringVar()
statusvar = tk.StringVar()

# initial message
to_print.set("\nEnter your names above.")		
statusvar.set("\nChoose Start or Import below.\n")

# &&& To implement, v0.2:
#			pull StringVar data out of a csv or txt on each refresh - DONE
#			therefore, REFRESH button - DONE
# 			how to do genius names, length? - TO DO TO DO TO DO

# Title
titleframe = tk.Frame(root)
titlelabel = tk.Label(titleframe, text = "\n" + apptitle, font = ("Heiti TC", 32))
titlelabel.pack()
titleframe.pack()

# Title and names

nameframe = tk.Frame(root)
namesofgeniuseslabel = tk.Label(nameframe, text = "\nNames of Geniuses:", \
	font = ("Heiti TC", 12))
namesofgeniuseslabel.pack()
namesinput = tk.Entry(nameframe, textvariable = namevar)
namesinput.pack()
spacerhead = tk.Label(nameframe, text = "")
spacerhead.pack()
namesinput.insert(0, "")
nameframe.pack()


# Buttons and interactivity

buttonframe = tk.Frame(root)

batteryquote = tk.Button(buttonframe, pady = 2, padx= 9, \
	 text = "Quote Battery", command = run_b)
batteryquote.grid(row=0, column=0)
batterycomplete = tk.Button(buttonframe, text = "Battery Complete", command = run_nb)
batterycomplete.grid(row=1, column=0)

spacer1 = tk.Label(buttonframe, text="             \n\n")
spacer1.grid(row=0, column=1)

displayquote = tk.Button(buttonframe, text = "Quote Display", command = run_d)
displayquote.grid(row=0, column=2)

displaycalib = tk.Button(buttonframe, text = "Display Calibrating", command = run_dc)
displaycalib.grid(row=0, column=4)

spacer2 = tk.Label(buttonframe, text="  ")
spacer2.grid(row=0, column=3)

displayfail = tk.Button(buttonframe, text = "Display Failed", command = run_df)
displayfail.grid(row=1, column=2)

displaycomplete = tk.Button(buttonframe, text = "Display Complete", command = run_nd)
displaycomplete.grid(row=1, column=4)

buttonframe.pack()


# Console output frame

consoleframe = tk.Frame(root)
console = tk.Label(consoleframe, textvariable=to_print, font = ("Heiti TC", 24))
console.pack()
status = tk.Label(consoleframe, textvariable=statusvar, font = ("Heiti TC", 15))
status.pack()

clearbutton = tk.Button(consoleframe, text = "Clear all", command=clearbutton)
#clearbutton.pack()
#####################
# &&& instead of clear, new AUDIT mode - recheck what's on the shelf

reportbutton = tk.Button(consoleframe, text = "Submit EoD Report", command=report)
reportbutton.pack()
newsessionbutton = tk.Button(consoleframe, text = "Start Session", command = newsession)
newsessionbutton.pack()
importstatusbutton = tk.Button(consoleframe, text = "Import Saved Status", \
	command = importstatus)
importstatusbutton.pack()

copyrightlabel = tk.Label(consoleframe, text = "\n\nDesigned by Jason in London", \
	font = ("Heiti TC", 10))
copyrightlabel.pack()
consoleframe.pack()


if __name__ == "__main__":
	title_text.set("Enter your names.")
	root.mainloop()













########### TO REMOVE
def tats(command):
	
	# import global variables used by this function	
	global genius
	global hour_b
	global hour_d
	global hour_f
	global rep_q
	global calib_q
	global fail
	
	# Math to calculate turnaround times, using calc() to round 
	# the value to the nearest 15.
	
	# Return TATs or status based on input
		
		### REMOVED EVERYTHING HERE, built into new class system above
	
	if command == "write":
		return "%d to repair.\n%d phones "\
		 "awaiting calibration/testing." % (rep_q, calib_q)
	
	#debugging tools
	elif command == "clear":
		rep_q = 0
		calib_q = 0
		fail = 1
		return "Cleared all queues."
	elif command == "set":
		rep_q = int(raw_input("Rep_q: "))
		calib_q = int(raw_input("Calib_q: "))
		fail = 1
		return "Rep_q set to %d.\nCalib_q set to %d.\n" \
		"Fail reset to default." % (rep_q, calib_q)
	
	else:
		return "Error!"
