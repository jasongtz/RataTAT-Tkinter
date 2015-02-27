#! /usr/bin/python
# RataTAT!

### TO FIX:
	# Search &&& for bugs or new features
	# Possible alternative, next vers: sign in with your name only
	# &&& When changing number of geniuses, takes an extra turn to take effect!
	

#	Modules imported
import Tkinter as tk
import time
import datetime as dt
from fractions import Fraction
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
hour_b = None
hour_d = None
hour_f = None

#	DAILYDATA CSV FUNCTIONS 

## Creates the blank csv with layout info, to be called at application start.
def create_csv():
	with open("dailydata.csv", "w") as blank:
		todays_date = [str(dt.date.today())]
		header = ["Time", "Names", "Batteries", "Displays", "Calibration Failures"]
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(todays_date)
		writer.writerow(header)

# Formats the hourly progress information from hourly_log.txt, then writes this 
# into dailydata.csv. This is called once per hour by csv_autolog() below.
def csvlog():
	done = []
	# Shows (time minus 1 hour) to current time. Eg "10:00 - 11:00"
	times = str(int(time.strftime("%H")) - 1) + ":" + time.strftime("%M") + " - " + \
		time.strftime("%H:%M")

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


#	CURRENT AND HOURLY LOGGING FUNCTIONS

# Creates the blank template of the current status log
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

# Imports the current hourly_log values.
def hourly_in():
	global hour_d
	global hour_b
	global hour_f
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
	if lines[1] == "Cleared":
		hour_d = 0
		hour_b = 0
		hour_f = 0
	else:
		hour_d = int(lines[1])
		hour_b = int(lines[2])
		hour_f = int(lines[3])

# Writes the update data to the hourly_log file.
def hourly_log():
	global hour_d
	global hour_b
	global hour_f
	with open("hourly_log.txt", "w") as log:
		log.write(str(names) + "\n%d\n%d\n%d" % (hour_b, hour_d, hour_f))


#	EMAIL REPORT FUNCTION
def sendemail(recip, subject, message):
	# Reads txt file to pull recipient and login info
	with open("emaildata.txt", "r") as file:
		data = file.readlines()
	if "Feedback" in subject:	
		recip = data[0].strip("\n")
	elif "Report" in subject:
		recip = data[1].strip("\n")
	email = data[2].strip("\n")
	password = data[3].strip("\n")

	# Generates the message
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = email
	msg['To'] = recip
	msg.preamble = None
	msg.attach(MIMEText(message))
	
	# Attaches the daily report
	if "Report" in subject:
		msg.attach(MIMEText("Report attached."))
		file = "dailydata.csv"
		fp = open(file, "rb")
		to_attach = MIMEText(fp.read())
		fp.close()
		to_attach.add_header("Content-Disposition", "attachment", \
			 filename = "modular %s.csv" % str(dt.datetime.today()))
		msg.attach(to_attach)
	
	smtpserver = smtplib.SMTP('smtp.mail.me.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(email, password)
	smtpserver.sendmail(email, recip, msg.as_string())
	smtpserver.quit()


#	APPLICATION FUNCTIONAL CODE

names = [""]
genius = len(names)
current_status = []

# Rounds an integer to the nearest 15
def calc(x):
	return (int(round(x/15)) * 15)

def round_tat(num):
	if num.is_integer() == False:
		remain = num%1
		return str(int(num-remain)) + " and " + str(Fraction(remain))
	else:
		return int(num)

# &&& CHECK IF FIXED: Start point off?
# &&& Also fix that it takes an extra update for changes in int(genius) to take effect!

def quote_battery(bq, dq):
	global genius
	num = float(calc((((bq + dq)/genius) * 15 + 30))) / 60
	return "\n Quote %s hours." % round_tat(num)
def quote_display(bq, dq, dc, df):
	global genius
	num = float(calc((((bq + dq + dc + df) / genius) * 15 + 45))) / 60
	return "\n Quote %s hours." % round_tat(num)

class Repairs(object):
	def __init__(self, index, exitmessage):
			self.index = index
			self.exitmessage = exitmessage

	def add(self):
		# Reads the log.csv, sets it into var status, adds 1 to int at self.index
		with open("log.csv", "rb") as file:
			status = [row for row in csv.reader(file)]  #List comprehension
			status[2][self.index] = int(status[2][self.index]) + 1
			status[0][1] = names
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
			status[0][1] = names
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

#	TKINTER UI FUNCTIONAL CODE which calls from functional code above

def get_status():
	statusvar.set("\n%d batteries, %d displays awaiting repair. \nThere are %d phones "\
		 "in or awaiting calibration/testing. \n" \
		"%s repairs completed this hour.\n" % \
		(current_status[0], current_status[1], current_status[2], (hour_b + hour_d)))

def eachactionupdate():
	global names
	names = namevar.get().split(", ")
	global genius
	genius = len(names)
	hourly_log()
	get_status()

# Button respond functions

def run_b():
	hourly_in()
	to_print.set(battery.add())
	eachactionupdate()
def run_nb():
	hourly_in()
	global hour_b
	if current_status[0]>=1:
		hour_b += 1
	to_print.set(battery.remove())
	eachactionupdate()
def run_d():
	hourly_in()
	to_print.set(display.add())
	eachactionupdate()
def run_dc():
	hourly_in()
	to_print.set(display.remove()) 
	if to_print.get() == "\nError!":
		pass
	else:
		calib.add()
	eachactionupdate()
def run_df():
	hourly_in()
	global hour_f
	if current_status[1]>=1:
		hour_f += 1
	fail.add()
	to_print.set("\nDisplay failed, attempt again.")
	eachactionupdate()
def run_nd():
	hourly_in()
	global hour_d
	if current_status[2]>=1:
		hour_d += 1		
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

def newsession():
	# In case new session is created because of a crash, sends daily report.
	report()	
	#Sets up all variables to blank, creates new log files.
	create_csv()
	with open("hourly_log.txt", "w") as log:
		log.write("\nCleared")
	global names
	names = namevar.get()
	global hour_d
	global hour_b
	global hour_f
	hour_b = 0
	hour_d = 0
	hour_f = 0
	create_log()
	hourly_log()
	refresh()
	to_print.set("\nFire when ready.")	
def importstatus():
	global hour_d
	global hour_b
	global hour_f
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
		if lines[1] != "Cleared":
			hour_d = int(lines[1])
			hour_b = int(lines[2])
			hour_f = int(lines[3])

			setnames = lines[0].replace("\n", "").replace("[", "").\
					replace("]", "").replace("'", "")
			namevar.set(setnames)	
	refresh()

def report():
	to_print.set("\nGenerating report...")
	sendemail("gwartz@icloud.com", "Modular Report for %s" % str(dt.date.today()), \
		"Report attached.")
	to_print.set("\nClosing report submitted.")
def sendfeedback():	
	sendemail("gwartz@icloud.com", "RataTAT Feedback", 	\
		"%s: \n\n %s" % (names, feedbackvar.get()))
	feedbackvar.set("Feedback submitted. Thanks!")

### TKINTER UI APPEARANCE CODE
#&&& TO DO: add in comments for all these classes

class App(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()

# Title and names
class NameFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		titlelabel = tk.Label(self, text = "\n" + \
			apptitle, font = ("Heiti TC", 32)).pack()
		namesofgeniuseslabel = tk.Label(self, text = "\nNames of Geniuses:", \
			font = ("Heiti TC", 12)).pack()
		namesinput = tk.Entry(self, textvariable = namevar).pack()
		spacerhead = tk.Label(self, text = "").pack()
		namesinput.insert(0, "")

# Buttons and interactivity
class ButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
		batteryquote = tk.Button(self, pady = 2, padx= 9, \
			 text = "Quote Battery/Other", command = run_b)
		batteryquote.grid(row=0, column=0)
		batterycomplete = tk.Button(self, text = "Battery/Other Complete", \
			command = run_nb)
		batterycomplete.grid(row=1, column=0)
		spacer1 = tk.Label(self, text="             \n\n")
		spacer1.grid(row=0, column=1)
		displayquote = tk.Button(self, text = "Quote Display", command = run_d)
		displayquote.grid(row=0, column=2)
		displaycalib = tk.Button(self, text = "Display Calibrating", command = run_dc)
		displaycalib.grid(row=0, column=4)
		spacer2 = tk.Label(self, text="  ")
		spacer2.grid(row=0, column=3)
		displayfail = tk.Button(self, text = "Display Failed", command = run_df)
		displayfail.grid(row=1, column=2)
		displaycomplete = tk.Button(self, text = "Display Complete", command = run_nd)
		displaycomplete.grid(row=1, column=4)

# Console output frame
class ConsoleFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global to_print
		global statusvar
		console = tk.Label(self, textvariable=to_print, font = ("Heiti TC", 24)).pack()
		status = tk.Label(self, textvariable=statusvar, font = ("Heiti TC", 15)).pack()
		
	# &&& instead of clear, new AUDIT mode - recheck what's on the shelf

		refreshbutton = tk.Button(self, text = "Refresh Status", \
		command = refresh).pack()
		spacer1 = tk.Label(self, text = "").pack()
		newsessionbutton = tk.Button(self, text = "Start New Session", \
		command=newsession).pack()
		importstatusbutton = tk.Button(self, text = "Import Saved Status", \
			command = importstatus).pack()
		spacer2 = tk.Label(self, text = "").pack()
		reportbutton = tk.Button(self, text = "Email EoD Report", command=report).pack()
		copyrightlabel = tk.Label(self, text = "\n\nDesigned by Jason in London\n", \
			font = ("Heiti TC", 10)).pack()

class FeedbackFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global feedbackvar
		feedbackinput = tk.Entry(self, width=30, textvariable = feedbackvar).pack()
		feedbackbutton = tk.Button(self, text = "Submit Feedback", \
			 command = sendfeedback).pack()

def for_import():
	global statusvar
	statusvar = tk.StringVar()
	global to_print
	to_print = tk.StringVar()
	global feedbackvar
	feedbackvar = tk.StringVar()
	global namevar
	namevar = tk.StringVar()
	importstatus()
	global names

def main():
	root = tk.Tk()
	global apptitle
	apptitle = "RataTAT v0.1.1"
	root.wm_title(apptitle)
	root.geometry("600x700")

	global statusvar
	statusvar = tk.StringVar()
	global to_print
	to_print = tk.StringVar()
	global feedbackvar
	feedbackvar = tk.StringVar()
	global namevar
	namevar = tk.StringVar()
	
	to_print.set("\nEnter your names above.")		
	statusvar.set("\nChoose Start or Import below.\n")
	
	NameFrame(root).pack()
	ButtonFrame(root).pack()
	ConsoleFrame(root).pack()
	FeedbackFrame(root).pack()
	
	root.mainloop()

if __name__ == "__main__":
	main()	
