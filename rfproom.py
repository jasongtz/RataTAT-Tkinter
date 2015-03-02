# Bar version

### TO FIX:

import Tkinter as tk
import modularui as m
import time


# Button actions

num = 2

def countdown():
	global num
	countervar.set("Wait " + str(num) + " more seconds.")
	num -= 1
	if num >= 0:
		root.after(1000, countdown)
	else:
		num = 2
		set_label()
		countervar.set("")
		
def set_label():
	m.displaymessage()

def quote_b():
	global b
	m.to_print.set(m.quote_battery(m.current_status[0], m.current_status[1]))
	b.pack()
	b.buildconfirm()

def quote_d():
	global d
	m.to_print.set(m.quote_display(m.current_status[0], m.current_status[1], \
				m.current_status[2], m.current_status[3]))
	d.pack()
	d.buildconfirm()


def refresh():
	getnames()
	m.refresh()
	if num == 2:
		set_label()
	else:
		m.to_print.set("\nWait!")


### &&& FIX THIS
def getnames():
	m.beforeeachaction()
	m.declaregenius()
			
			
# TKINTER APPEARANCE

class App(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()

# Title and names
class NameFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		titlelabel = tk.Label(self, text = "\n" + m.apptitle + ": Bar", \
			font = ("Heiti TC", 32)).pack()
		whosrepairinglabel = tk.Label(self, textvariable = m.geniusvar, \
			 font = ("Heiti TC", 12)).pack()
		spacerhead = tk.Label(self, text = "").pack()
	
# Buttons and interactivity
class ButtonFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		
		batteryquote = tk.Button(self, text = "Quote Battery/Other", command = quote_b)
		batteryquote.pack(side=tk.LEFT)
		spacer1 = tk.Label(self, text="             \n\n")
		spacer1.pack(side=tk.LEFT)
		displayquote = tk.Button(self, text = "Quote Display", command = quote_d)
		displayquote.pack(side=tk.LEFT)
		spacer2 = tk.Label(self, text = "").pack()
	
class ConfirmFrame(App):
	def __init__(self, parent, repair):
		tk.Frame.__init__(self, parent)
		self.repair = repair
		self.parent = parent
		self.confirmbutton = tk.Button(parent, text = "CONFIRM BOOK-IN", \
			command = self.confirm)
		self.cancelbutton = tk.Button(parent, text = "Cancel Estimate", \
			command = self.cancel)
	
	def buildconfirm(self):
		self.cancelbutton.pack()
		self.confirmbutton.pack()
	def clearconfirm(self):
		self.confirmbutton.pack_forget()
		self.cancelbutton.pack_forget()
	
	def confirm(self):
		if self.repair == "b":
			m.run_b()
		elif self.repair == "d":
			m.run_d()
		self.clearconfirm()
		refresh()
	def cancel(self):
		self.clearconfirm()
		refresh()

# Console output frame
class UpperConsoleFrame(App):
	def __init__(self, parent):
		self.parent = parent
		tk.Frame.__init__(self, parent)
		console = tk.Label(self, textvariable=m.to_print, font = ("Heiti TC", 24)).pack()		
		counter = tk.Label(self, textvariable=countervar, font = ("Heiti TC", 12)).pack()


class LowerConsoleFrame(App):
	def __init__(self, parent):
		self.parent = parent
		tk.Frame.__init__(self, parent)
		status = tk.Label(self, textvariable=m.statusvar, font = ("Heiti TC", 15)).pack()
		refreshbutton = tk.Button(self, text = "Refresh Status", \
			command = refresh).pack()
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
	
	root.wm_title(m.apptitle + ": Bar")
	root.geometry("600x600")

	global countervar
	countervar = tk.StringVar()
	global namesvar
	namesvar = tk.StringVar()
		
	m.for_import()
	refresh()

	NameFrame(root).pack()
	ButtonFrame(root).pack()
	u = UpperConsoleFrame(root)
	u.pack()
	LowerConsoleFrame(root).pack()
	FeedbackFrame(root).pack()

	global b
	global d
	
	b = ConfirmFrame(u, "b")
	d = ConfirmFrame(u, "d")
	root.mainloop()

if __name__ == "__main__":
	main()	


