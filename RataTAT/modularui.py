#! /usr/bin/python

# RataTAT!
# Search &&& for bugs or new features

import time, csv, smtplib, math
import jglogging as log
import Tkinter as tk
import datetime as dt
from fractions import Fraction
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

apptitle = "RataTAT v0.4"



#	EMAIL REPORT FUNCTION
def sendemail(subject, message):
	# Reads txt file to pull recipient and login info
	# Line-by-line setup of the 'emaildata.txt' file:
	#	1 = feedbackrecip
	#	2 = reportrecip
	#	3 = sending
	#	4 = password
	
	with open("emaildata.txt", "r") as file:
		data = file.readlines()
	if "Feedback" in subject:	
		recip = data[0].strip("\n")
	elif "Report" in subject:
		recip = data[1].strip("\n")
	else:
	    return None
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
		file = "dailydata.csv"
		fp = open(file, "rb")
		to_attach = MIMEText(fp.read())
		fp.close()
		to_attach.add_header("Content-Disposition", "attachment", \
			 filename = "modular %s.csv" % str(dt.date.today()))
		msg.attach(to_attach)
	
	# Attaches the daily, hourly, and current log files to a feedback submission
	if "Feedback" in subject:
		file1 = "dailydata.csv"
		fp1 = open(file1, "rb")
		to_attach1 = MIMEText(fp1.read())
		fp1.close()
		to_attach1.add_header("Content-Disposition", "attachment", filename = file1)
#		file2 = "hourly_log.txt"
#		fp2 = open(file2, "rb")
#		to_attach2 = MIMEText(fp2.read())
#		fp2.close()
#		to_attach2.add_header("Content-Disposition", "attachment", filename = file2)
		file3 = "log.csv"
		fp3 = open(file3, "rb")
		to_attach3 = MIMEText(fp3.read())
		fp3.close()
		to_attach3.add_header("Content-Disposition", "attachment", filename = file3)
		msg.attach(to_attach1) 
#		msg.attach(to_attach2)
		msg.attach(to_attach3)
	
	smtpserver = smtplib.SMTP('smtp.mail.me.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(email, password)
	smtpserver.sendmail(email, recip, msg.as_string())
	smtpserver.quit()

#	LOGGING CSV FUNCTIONS moved to external file

def handover():

	with open("dailydata.csv", "rb") as f:
		wholedaydata = [row for row in csv.reader(f)]	
	batteries = 0
	displays = 0
	fails = 0	
	for x in range(2, len(wholedaydata)):
		try:
			batteries += int(wholedaydata[x][2])
		except:
			pass
		try:
			displays += int(wholedaydata[x][3])
		except:
			pass
		try:
			fails += int(wholedaydata[x][4])
		except:
			pass

	# Appends the dailydata.csv with daily totals
	with open("dailydata.csv", "a") as f:
		writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(["", "", "", "", ""])
		writer.writerow(["DAILY TOTALS", "", batteries, displays, fails])

	message = "Daily totals:\nBatteries: %d\n Displays: %d \nTOTAL: %d\n\n" \
		"To hand over for the morning: \n%d batteries, %d display to repair, " \
		"%d in the calibration machines." % (batteries, displays, (batteries+displays), \
		getcurrentstatus()[0], getcurrentstatus()[1], getcurrentstatus()[2])
	send_report(message)

	# Saves the dailydata.csv as a file with the date as the filename
	with open("dailydata.csv", "rb") as file:
		report = [row for row in csv.reader(file)]
		with open("previous daily logs/%s.csv" % str(dt.date.today()), "w") as write:
			writer = csv.writer(write, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
			for x in range(len(report)):
				writer.writerow(report[x])
	
	# Resets the dailydata.csv file to default
	with open("dailydata.csv", "w") as blank:
		writer = csv.writer(blank, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow([str(dt.date.today() + dt.timedelta(days=1))])
		writer.writerow(["Time", "Geniuses", "Batteries", \
			"Displays", "Calibration Failures"])

	# Changes the current log file's date
	status = readlogfile()
	status[0][0] = str(dt.date.today() + dt.timedelta(days=1))
	with open("log.csv", "wb") as file:
		for num in range(4):
			csv.writer(file, delimiter=",").writerow(status[num])
			

#	APPLICATION FUNCTIONAL CODE
	
	
class Repairs(object):
	"""Different types of repairs are given an index indicating at which column their
	count is found in the log.csv file, and an exit message which is displayed when
	one is removed from the count in log.csv.
	"""
	def __init__(self, index, exitmessage):
			self.index = index
			self.exitmessage = exitmessage
			
	def add(self):
		"""Adds a new repair to the log, returns the quoted estimated time.
		
		Retrieves the current status and number of Geniuses doing repairs, 
		then adds 1 to the queue for repair type given by self.index.
		Writes the new values to the log file. Then runs the quoting functions, 
		passing in integers for arguments representing the current status.
		"""
		current_status = getcurrentstatus()
		genius = readgenius()	
		current_status[self.index] += 1
		writestatus(current_status)
		if self.index == 0:
			return quote_battery(current_status[0], current_status[1], genius)
		elif self.index == 1:
			return quote_display(current_status[0], current_status[1], \
				   current_status[2], current_status[3], genius)
		elif self.index == 3:
			hourlylog = log.gethourlylog()
			hourlylog[self.index] += 1
			log.writehourlylog(hourlylog)
			return "Display failed."

	def remove(self):
		"""Removes a completed repair from the log, or removes it from one repair type
		in order for it to be added to another.
		
		Retrieves the current status and number of Geniuses doing repairs, 
		then subtracts 1 from the queue for repair type given by self.index.
		Writes the new values to the log file, as in the add(self) function above.
		"""
		current_status = getcurrentstatus()
		if current_status[self.index] > 0:
			current_status[self.index] -= 1
		else:
			return "\nError!"

        # Reduce fail count on successful calib remove
		if self.index == 2:
				if current_status[3] > 0:
					current_status[3] -= 1
			
		writestatus(current_status)
		# Writes to the hourly log for battery, calibration (display rfp), and failures
		if self.index != 1:
			hourlylog = log.gethourlylog()
			hourlylog[self.index] += 1
			log.writehourlylog(hourlylog)
		return self.exitmessage
			
# Instantiation of all repair/movement types
battery = Repairs(0, "\nBattery complete.")
display = Repairs(1, "\nDisplay awaiting calibration.")
calib = Repairs(2, "\nDisplay complete.")
fail = Repairs(3, None) # Failure counts get removed invisibly, thus no self.exitmessage

def quote_battery(bq, dq, genius):
	"""Takes the current repair queues in arguments, returns a turnaround time."""
	num = float((bq + dq)/genius * 0.25 + 0.5)
	# Checks if the repair can be completed same-day.
	if check_sameday(num):
		return "\nQuote %s" % round_tat(num)
	else:
		return "\nNEXT DAY"
	
def quote_display(bq, dq, dc, df, genius):
	"""As with quote_battery, but includes display-related status integers."""
	num = float((bq + dq + dc + df)/ genius * 0.25 + 0.80)
	if check_sameday(num):
		return "\nQuote %s" % round_tat(num)
	else:
		return "\nNEXT DAY"

def check_sameday(num):
	"""Returns False if the estimated repair completion 
	time is after the store's closing hours.
	"""
	num_minutes = int(num%1*60)
	now = dt.datetime.now()
	carry_the_hour = ((now.minute + num_minutes) / 60)
	# Adds the repair time to the current time to estimate a completion time
	try:
	    endtime = dt.time((now.hour + int(num) + carry_the_hour), (now.minute + num_minutes)%60)
	    with open("message.txt", "w") as file:
			file.write("Ready and waiting.")
	except ValueError:
		with open("message.txt", "w") as file:
			file.write("That's a lot of phones...")
		return False

	if now.weekday() == 6:
		if endtime > dt.time(17, 50):
			return False
		else:
			return True
	else:
		if endtime > dt.time(19, 50):
			return False
		else:
			return True

def readlogfile():
	"""Opens the log file, returns a list where each line of the csv is a list."""
	with open("log.csv", "rb") as file:
		return [row for row in csv.reader(file)]  # List comprehension

def readgenius():
	"""Reads the cell of log.csv where the current number of Geniuses is stored."""
	return int(readlogfile()[0][1])

def getcurrentstatus():
	"""Converts the 2nd line of the status file into integers, returns as a list."""
	return [int(numbers) for numbers in readlogfile()[2]]

def writestatus(values):
	"""Takes the current status file, changes the values line, writes it back."""
	status = readlogfile()
	status[2] = values
	with open("log.csv", "wb") as file:
		for num in range(4):
			csv.writer(file, delimiter=",").writerow(status[num])


def round_tat(num):
	"""Changes the turnaround time from a float into natural language hours + minutes."""
	remain = num%1
	if num.is_integer():
		if int(num) == 1:
			return str(int(num)) + " hour."
		else:
			return str(int(num)) + " hours."
	else:
		num = round_num(num)
		remain = num%1
		if num < 1:
			return str(int(remain*60)) + " minutes."
		elif num-remain==1:
			return str(int(num-remain)) + " hour and " + \
				str(int(remain*60)) + " minutes."
		else:
			return str(int(num-remain)) + " hours and " + \
	    		str(int(remain*60)) + " minutes."

def round_num(num):
    return math.ceil(num/0.25)*0.25

#	TKINTER UI FUNCTIONAL CODE which calls from functional code above

def refresh():
	beforeeachaction()
	eachactionupdate()

# Used to refresh the status message
def get_status():
	current_status = getcurrentstatus()
	hourlylog = log.gethourlylog()
	return "\n%d displays, %d batteries/other awaiting repair." \
		"\nThere are %d phones in or awaiting calibration/testing.\n" \
		"%d repairs completed so far this hour." % \
		(current_status[1], current_status[0], current_status[2], \
		(hourlylog[0] + hourlylog[2]))

def get_next_times():
    current_status = getcurrentstatus()
    genius = readgenius()
    disp = quote_display(current_status[0], current_status[1], \
				   current_status[2], current_status[3], genius).replace("\n", "").replace("Quote", "")
    batt = quote_battery(current_status[0], current_status[1], genius).replace("\n", "").replace("Quote ", "")

    return "\nNext display will be %s Next battery will be %s" % (disp, batt)
    

def displaymessage():
	with open("message.txt", "r") as file:
		message = file.readline()
		to_print.set("\n" + message)

	
def beforeeachaction():
#	hourly_in()
	setgenius(readgenius())

countdownnum = 2

def eachactionupdate():
#	hourly_log()
	statusvar.set(get_status())
	try:
	    nexttimevar.set(get_next_times())
	except NameError:
	    pass
	if __name__ == "__main__":
		global countdownnum
		if countdownnum == 2:
			countdown()
		else:
			pass
			
def countdown():
	global root
	global countdownnum
	countervar.set("Wait " + str(countdownnum) + " more seconds.")
	if countdownnum > 0:
		countdownnum -= 1
		root.after(1000, countdown)
	else:
		displaymessage()		
		countdownnum = 2
		countervar.set("")
	
# BUTTON RESPONSE FUNCTIONS

def run_b():
	beforeeachaction()
	to_print.set(battery.add())
	eachactionupdate()
def run_nb():
	beforeeachaction()
#	if getcurrentstatus()[0]>=1:
#		hour_b += 1
	to_print.set(battery.remove())
	eachactionupdate()
def run_d():
	beforeeachaction()
	to_print.set(display.add())
	eachactionupdate()
def run_dc():
	beforeeachaction()
	to_print.set(display.remove()) 
	if to_print.get() == "\nError!":
		pass
	else:
		calib.add()
	eachactionupdate()
def run_df():
	beforeeachaction()
#	global hour_f
#	if getcurrentstatus()[2]>=1:
#		hour_f += 1
	fail.add()
	to_print.set("\nDisplay failed, attempt again.")
	eachactionupdate()
def run_nd():
	beforeeachaction()
#	global hour_d
#	if getcurrentstatus()[2]>=1:
#		hour_d += 1		
	to_print.set(calib.remove())
	if getcurrentstatus()[3] > 0:
		fail.remove()
	eachactionupdate()

def setmessage():
	with open("message.txt", "w") as file:
		file.write(setmessagevar.get())
	refresh()
def defaultmessage():
	with open("message.txt", "w") as file:
		file.write("Ready and waiting.")
	refresh()
	
def send_report(message):
#	to_print.set("\nGenerating report...")
	sendemail("Modular Report for %s" % str(dt.date.today()), \
		message)
#	to_print.set("\nClosing report submitted.")
def sendfeedback():	
	sendemail("RataTAT Feedback", 	\
		"\n %s" % feedbackvar.get())
	feedbackvar.set("Feedback submitted. Thanks!")
	root.after(2000, lambda: feedbackvar.set(""))

def setgenius(genius):
	status = readlogfile()
	status[0][1] = genius
	with open("log.csv", "wb") as file:
		for number in range(4):
			csv.writer(file, delimiter=",").writerow(status[number])
	declaregenius(genius)
	
def declaregenius(genius):	
	if genius == 1:
		geniusvar.set(str(genius) + " Genius currently.")
	else:
		geniusvar.set(str(genius) + " Geniuses currently.")

def newsession():
    # DEPRECATED!!!!!!!!!!
	# &&& TO FIX: LIST INDEX ISSUE
	#Sets up all variables to blank, creates new log files.
	create_log()
	create_csv()
	with open("hourly_log.txt", "w") as log:
		log.write("%s\nCleared" % 1)
	global hour_d
	global hour_b
	global hour_f
	hour_b = 0
	hour_d = 0
	hour_f = 0
	refresh()
	defaultmessage()


### TKINTER UI APPEARANCE CODE 		#&&& TO DO: add in comments for all these classes

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
		global geniusvar
		geniuses = tk.Label(self, textvariable = geniusvar).pack()
		
# Buttons and interactivity
class UpperButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
		spacer1 = tk.Label(self, text="             ").pack()
		displaycalib = tk.Button(self, text = "Awaiting Calibration", command = run_dc)\
			.pack()
		displayfail = tk.Button(self, text = "Display Failed", command = run_df).pack()		
		spacer2 = tk.Label(self, text="  ")
		spacer2.pack()
		
class MiddleButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
		displaycomplete = tk.Button(self, text = "Display RFP", command = run_nd)
		displaycomplete.grid(row=3, column=1)	
		batterycomplete = tk.Button(self, text = "Battery/Other RFP", \
			command = run_nb)
		batterycomplete.grid(row=3, column=3)

# Console output frame
class ConsoleFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global to_print
		global statusvar
		console = tk.Label(self, textvariable=to_print, font = ("Heiti TC", 24)).pack()
		countdown = tk.Label(self, textvariable=countervar, font = ("Heiti TC", 12)).pack()
		status = tk.Label(self, textvariable=statusvar, font = ("Heiti TC", 15)).pack()
		refreshbutton = tk.Button(self, text = "Refresh Status", \
			command = refresh).pack()
		spacer1 = tk.Label(self, text = "").pack()
		
class LowerButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
	
		spacer1 = tk.Label(self, text="             \n\n")
		#spacer1.grid(row=0, column=1)
		displayquote = tk.Button(self, text = "Add Display", command = run_d)
		displayquote.grid(row=0, column=0)
		batteryquote = tk.Button(self, text = "Add Battery/Other", command = run_b)
		batteryquote.grid(row=0, column=1)

	
#### REMOVE THESE TWO CLASSES	
class SetMessageFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		spacer = tk.Label(self, text = "").pack()
		global setmessagevar
		messageinput = tk.Entry(self, width=30, textvariable = setmessagevar).pack()
		setmessagebutton = tk.Button(self, text = "Set Emergency Message", \
			 command = setmessage).pack()
		defaultmessagebutton = tk.Button(self, text = "Return to Default Message", \
			command = defaultmessage).pack()
		spacer1 = tk.Label(self, text = "").pack()

class DayFrame(App):
    ## DEPRECATED!!!
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
		newsessionbutton = tk.Button(self, text = "Start Day", \
		command=newsession).grid(row=0, column=0)
		reportbutton = tk.Button(self, text = "End Day", command=report)\
			.grid(row=0, column=1)
########################

class FeedbackFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global feedbackvar
		#spacer = tk.Label(self, text = "").pack()
		copyrightlabel = tk.Label(self, text = "\n\nDesigned by Jason in London\n", \
			font = ("Heiti TC", 10)).pack()
		feedbackinput = tk.Entry(self, width=50, textvariable = feedbackvar).pack()
		feedbackbutton = tk.Button(self, text = "Submit Feedback", \
			 command = sendfeedback).pack()

class NextTimeFrame(App):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        status = tk.Label(self, textvariable=nexttimevar, font = ("Heiti TC", 12)).pack()


def for_import():
	global statusvar
	statusvar = tk.StringVar()
	global to_print
	to_print = tk.StringVar()
	global feedbackvar
	feedbackvar = tk.StringVar()
	global namevar
	namevar = tk.StringVar()
	global geniusvar
	geniusvar = tk.StringVar()
	global setmessagevar
	setmessagevar = tk.StringVar()
	

def main(title):
	global root
	root = tk.Tk()
	root.wm_title(title)
	root.geometry("600x600")

	global statusvar
	statusvar = tk.StringVar()
	global to_print
	to_print = tk.StringVar()
	global feedbackvar
	feedbackvar = tk.StringVar()
	global namevar
	namevar = tk.StringVar()
	global setmessagevar
	setmessagevar = tk.StringVar()
	global countervar
	countervar = tk.StringVar()
	global geniusvar
	geniusvar = tk.StringVar()
	global nexttimevar
	nexttimevar = tk.StringVar()

	displaymessage()
		
	NameFrame(root).pack()
	UpperButtonFrame(root).pack()
	MiddleButtonFrame(root).pack()
	ConsoleFrame(root).pack()
	LowerButtonFrame(root).pack()
	FeedbackFrame(root).pack()
	NextTimeFrame(root).pack()

	refresh()		
	root.mainloop()

if __name__ == "__main__":
	main(apptitle)	
