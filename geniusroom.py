from modularui import *

### TKINTER UI APPEARANCE CODE

root = tk.Tk()
apptitle = "RataTAT v0.1.1"
root.wm_title(apptitle)
root.geometry("600x700")

to_print = tk.StringVar()
namevar = tk.StringVar()
statusvar = tk.StringVar()
feedbackvar = tk.StringVar()

# initial message
to_print.set("\nEnter your names above.")		
statusvar.set("\nChoose Start or Import below.\n")


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
	 text = "Quote Battery/Other", command = run_b)
batteryquote.grid(row=0, column=0)
batterycomplete = tk.Button(buttonframe, text = "Battery/Other Complete", command = run_nb)
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

refreshbutton = tk.Button(consoleframe, text = "Refresh Status", \
	command = refresh)
refreshbutton.pack()
spacer1 = tk.Label(consoleframe, text = "")
spacer1.pack()
newsessionbutton = tk.Button(consoleframe, text = "Start New Session", command=newsession)
newsessionbutton.pack()
importstatusbutton = tk.Button(consoleframe, text = "Import Saved Status", \
	command = importstatus)
importstatusbutton.pack()
spacer2 = tk.Label(consoleframe, text = "")
spacer2.pack()
reportbutton = tk.Button(consoleframe, text = "Email EoD Report", command=report)
reportbutton.pack()

copyrightlabel = tk.Label(consoleframe, text = "\n\nDesigned by Jason in London\n", \
	font = ("Heiti TC", 10))
copyrightlabel.pack()
consoleframe.pack()

feedbackframe = tk.Frame(root)
#feedbacklabel = tk.Label(feedbackframe, text = "\nFeedback:", font = ("Heiti TC", 12))
#feedbacklabel.pack()
feedbackinput = tk.Entry(feedbackframe, width=30, textvariable = feedbackvar)
feedbackinput.pack()
feedbackbutton = tk.Button(feedbackframe, text = "Submit Feedback", \
	 command = sendfeedback)
feedbackbutton.pack()
feedbackframe.pack()



if __name__ == "__main__":
	root.mainloop()
