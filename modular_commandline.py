#! /usr/bin/python

# Modulars

#### COMMAND LINE FUNCTIONS ONLY
# Mostly removed from this file, all in the other file now.

#### TRACKER
# Future Planning:
# Consider writing the TATS function into a class.
	# instead of if/else, each "command" would be a function.
	# ie run tats.b(), tats.log()
	# all variables, instead of global x, be tats.x


man = """Remember the commands.
b = quote for a battery, +1 battery to the queue.
d = quote for a display, +1 display to repair queue.
dc = repaired a display, awaiting calibration/testing.

-b = completed a battery, marked RFP.
-d = display completed calibration & testing, marked RFP.

genius = Change the number of Geniuses currently performing repairs.

To repeat this manual any time, type \"man\".
Go ahead, when ready.
"""

import time
import datetime
import csv




	



# These two functions below are used if running this application from
# command line, for testing or debugging purposes. This was how the application
# was first developed, before the GUI was implemented.

def input():
	# Looping main interaction
	while True:
		x = raw_input("> ")
		print tats(x)
		
		#prints the status - no longer needed
		print "%d phones on shelf." % rep_q
		
		# appends the status file - no longer needed
		
		with open("status.txt", "a") as status:
			status.write(time.strftime("%H:%M:%S") + "\n" + tats("write") + "\n\n")
	
		# Calls the function above which updates the hourly_log.txt file
		log()

if __name__ == "__main__":
	genius = 1

	# SETUP	
	print "Hi. Welcome to Modulars!\nHow many Geniuses on modulars? "
	genius = int(raw_input("> "))

	print "Please type your names."
	names = [raw_input("> ") for i in range(genius)]

	print "Okay, %s. Press RETURN to continue." % names
	raw_input("")
	create_csv()
	
	# initialises the status file = no longer needed
	with open("status.txt", "w") as blank:
		blank.write("%s doing repairs. \n\n" % names)
	#END SETUP
	
	# Runs the looping input() above.
	input()


