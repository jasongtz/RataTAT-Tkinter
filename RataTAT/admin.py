# CONTROL PANEL
import Tkinter as tk
import modularui as m

def setgenius(x):
	m.setgenius(x)
	admingeniusvar.set(m.geniusvar.get())

def refresh():
	m.refresh()


class App(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()

class NameFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		titlelabel = tk.Label(self, text = "\n" + \
			m.apptitle + ": ADMIN CONTROLS", font = ("Heiti TC", 32)).pack()
		global geniusvar
		geniuses = tk.Label(self, textvariable = admingeniusvar).pack()
	
class GeniusFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		global geniusvar
			#spacerg = tk.Label(self, text = "                    ").pack(side=tk.LEFT)
		onegeniusbutton = tk.Button(self, text = "One", command = lambda: setgenius(1))
		onegeniusbutton.grid(row=0, column=0)
		twogeniusbutton = tk.Button(self, text = "Two", command = lambda: setgenius(2))
		twogeniusbutton.grid(row=0, column=1)
		threegeniusbutton = tk.Button(self, text = "Three", command = lambda: setgenius(3))
		threegeniusbutton.grid(row=0, column=2)
		#spacerhead = tk.Label(self, text = "\n").pack()
		
class SetMessageFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		spacer = tk.Label(self, text = "").pack()
		global setmessagevar
		messageinput = tk.Entry(self, width=30, textvariable = m.setmessagevar).pack()
		setmessagebutton = tk.Button(self, text = "Set Emergency Message", \
			 command = m.setmessage).pack()
		defaultmessagebutton = tk.Button(self, text = "Return to Default Message", \
			command = m.defaultmessage).pack()
		spacer1 = tk.Label(self, text = "").pack()

class DayFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)	
		newsessionbutton = tk.Button(self, text = "Start Day", \
		command=m.newsession).grid(row=0, column=0)
		reportbutton = tk.Button(self, text = "End Day", command=m.report)\
			.grid(row=0, column=1)

class FeedbackFrame(App):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		spacer1 = tk.Label(self, text = "\n").pack()
		copyrightlabel = tk.Label(self, text = "\n\nDesigned by Jason in London\n", \
			font = ("Heiti TC", 10)).pack()
	
		global feedbackvar
		feedbackinput = tk.Entry(self, width=30, textvariable = m.feedbackvar).pack()
		feedbackbutton = tk.Button(self, text = "Submit Feedback", \
			 command = m.sendfeedback).pack()



def main():
	global root
	root = tk.Tk()
	
	root.wm_title(m.apptitle + ": ADMIN CONTROLS")
	root.geometry("600x500")

	global admingeniusvar
	admingeniusvar = tk.StringVar()
	
	m.for_import()
	m.refresh()
	
	admingeniusvar.set(m.geniusvar.get())
		
	NameFrame(root).pack()
	GeniusFrame(root).pack()
	SetMessageFrame(root).pack()
#	DayFrame(root).pack()
	FeedbackFrame(root).pack()

	root.mainloop()

if __name__ == "__main__":
	main()	
