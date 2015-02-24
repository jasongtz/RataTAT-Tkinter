#! /usr/bin/python

# MODULAR UI


##################
### TO FIX:
	# Search &&& for bugs or new features
	

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
rep_q = 0
calib_q = 0
fail = 1

# Rounds an integer to the nearest 15
def calc(x):
	return (int(round(x/15)) * 15)

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
	battery_tat = float(calc(30.0 + ((rep_q/genius) * 15))) / 60
	display_tat = float(calc((((rep_q + calib_q + fail) / genius) * 15 + 30))) / 60

	# Return TATs or status based on input
	if command == "b":
		rep_q += 1
		return "Quote %s hours." % battery_tat
	elif command == "d":
		rep_q += 1
		return "Quote %s hours." % display_tat
	elif command == "-b":
		if rep_q > 0:
			rep_q -= 1
			hour_b += 1
			return "Battery complete."
		else:
			return "Error! No batteries pending."
	elif command == "-d":
		if calib_q > 0:
			calib_q -= 1
			if fail > 0:
				fail -= 1
			hour_d += 1
			return "Display complete."
		else:
			return "Error! No displays calibrating."
	# Display related commands
	elif command == "dc":
		if rep_q > 0:
			rep_q -= 1
			calib_q += 1
			return "Display awaiting calibration."
		else:
			return "Error! No displays pending."
	elif command == "df":
		if calib_q > 0:
			fail += 1
			hour_f += 1
			return "Display failed. Attempt new display."
		else:
			return "Error! No displays calibrating."

	# Application commands
	elif command == "status":
		return "\n%d phones awaiting repair. \nThere are %d phones "\
		 "in or awaiting calibration/testing. \n" \
		"%s repairs completed this hour.\n" % (rep_q, calib_q, (hour_b + hour_d))
	
	elif command == "write":
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

def log():
	global hour_d
	global hour_b
	global hour_f
	
	# Checks if hourly_log is cleared. If so: resets the hour values to zero	.	
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
		if lines[1] == "Cleared":
			hour_d = 0
			hour_b = 0
			hour_f = 0

	# Updates the hourly log file.
	with open("hourly_log.txt", "w") as log:
		log.write(str(names) + "\n%d\n%d\n%d" % (hour_b, hour_d, hour_f))



#### CSV FUNCTIONS 

## Creates the blank csv with layout info, to be called at application start.
def create_csv():
	with open("data.csv", "w") as blank:
		todays_date = [str(dt.date.today())]
		header = ["Time", "Names", "Batteries", "Displays", "Calibration Failures"]
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(todays_date)
		writer.writerow(header)

# Formats the hourly progress information from hourly_log.txt,
# writes this into data.csv.
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
	with open("data.csv", "a") as f:
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
	file = "data.csv"
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
	statusvar.set(tats("status"))

def eachactionupdate():
	global names
	names = namevar.get().split(", ")
	global genius
	genius = len(names)

	with open("status.txt", "a") as status:
		status.write(time.strftime("%H:%M:%S") + "\n" \
			 + tats("write") + "%s \n\n" % names)
	log()
	get_status()

def run_b():
	to_print.set("\n" + tats("b"))
	eachactionupdate()
def run_d():
	to_print.set("\n" + tats("d"))
	eachactionupdate()
def run_nb():
	to_print.set("\n" + tats("-b"))
	eachactionupdate()
def run_nd():
	to_print.set("\n" + tats("-d"))
	eachactionupdate()
def run_dc():
	to_print.set("\n" + tats("dc"))
	eachactionupdate()
def run_df():
	to_print.set("\n" + tats("df"))
	eachactionupdate()
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
def importstatus():
	global genius
	global hour_b
	global hour_d
	global hour_f
	global rep_q
	global calib_q
	global fail
	with open("hourly_log.txt", "r+") as log:
		lines = log.readlines()
		if lines[1] != "Cleared":
			hour_d = int(lines[1])
			hour_b = int(lines[2])
			hour_f = int(lines[3])

# &&& Import working! Now just to adjust active vars like rep_q, calib_q


### TKINTER UI APPEARANCE CODE

root = tk.Tk()
apptitle = "RataTAT v0.1"
root.wm_title(apptitle)
root.geometry("800x600")

to_print = tk.StringVar()
namevar = tk.StringVar()
title_text = tk.StringVar()

statusvar = tk.StringVar()
statusvar.set(tats("status"))


# &&& To implement, v0.2:
#			pull StringVar data out of a csv or txt on each refresh
#			therefore, REFRESH button
# 			how to do genius names, length?

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

to_print.set("\nEnter your names above.")		# initial message
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

copyrightlabel = tk.Label(consoleframe, text = "\n\nBy Gwartz", font = ("Heiti TC", 10))
copyrightlabel.pack()
consoleframe.pack()


if __name__ == "__main__":
	title_text.set("Enter your names.")
	root.mainloop()
