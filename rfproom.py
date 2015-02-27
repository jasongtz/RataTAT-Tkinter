# Bar version

import Tkinter as tk
import modularui as m
import time
# Button actions

num = 3

# &&& Bug if another button is clicked while countdown is running

def countdown():
	global num
	countervar.set("Wait " + str(num) + " more seconds.")
	num -= 1
	if num >= 0:
		root.after(1000, countdown)
	else:
		num = 3
		set_label()
		countervar.set("")
def set_label():
	m.to_print.set("\nFire when ready.")

def quote_b():
	global num
	if num == 3:
		m.run_b()
		countdown()
def quote_d():
	global num
	if num == 3:
		m.run_d()
		countdown()

class App(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()

# Title and names
class NameFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		titlelabel = tk.Label(self, text = "\n" + apptitle, \
			font = ("Heiti TC", 32)).pack()
		whosrepairinglabel = tk.Label(self, text = "\n" + m.namevar.get() + \
			" doing repairs.", font = ("Heiti TC", 12)).pack()
		spacerhead = tk.Label(self, text = "").pack()
	
# Buttons and interactivity
class ButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		
		batteryquote = tk.Button(self, text = "Quote Battery/Other", command = quote_b)
		batteryquote.grid(row=0, column=0)
		spacer1 = tk.Label(self, text="             \n\n")
		spacer1.grid(row=0, column=1)
		displayquote = tk.Button(self, text = "Quote Display", command = quote_d)
		displayquote.grid(row=0, column=2)

# Console output frame
class ConsoleFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		console = tk.Label(self, textvariable=m.to_print, font = ("Heiti TC", 24)).pack()		
		counter = tk.Label(self, textvariable=countervar, font = ("Heiti TC", 12)).pack()
		status = tk.Label(self, textvariable=m.statusvar, font = ("Heiti TC", 15)).pack()
		refreshbutton = tk.Button(self, text = "Refresh Status", \
			command = m.refresh).pack()
		spacer1 = tk.Label(self, text = "").pack()
		copyrightlabel = tk.Label(self, text = "\n\nDesigned by Jason in London\n", \
			font = ("Heiti TC", 10)).pack()

class FeedbackFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global feedbackvar
		feedbackinput = tk.Entry(self, width=30, textvariable = m.feedbackvar).pack()
		feedbackbutton = tk.Button(self, text = "Submit Feedback", \
			 command = m.sendfeedback).pack()




def main():
	global root
	root = tk.Tk()
	
	global apptitle
	apptitle = "RataTAT v0.1.1"
	root.wm_title(apptitle)
	root.geometry("600x500")
	
	global countervar
	countervar = tk.StringVar()
	m.for_import()
	set_label()
	m.eachactionupdate()
	
	NameFrame(root).pack()
	ButtonFrame(root).pack()
	ConsoleFrame(root).pack()
	FeedbackFrame(root).pack()

	root.mainloop()

if __name__ == "__main__":
	main()	
