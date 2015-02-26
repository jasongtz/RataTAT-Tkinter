## Can't I do this as an import??


import Tkinter as tk
from modularui import Repairs
from modularui import hourly_in
from modularui import eachactionupdate

root = tk.Tk()
apptitle = "RataTAT v0.1.1\n"

root.wm_title(apptitle)
root.geometry("600x400")



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










battery = Repairs(0, "\nBattery complete.")
display = Repairs(1, "\nDisplay awaiting calibration.")

to_print = tk.StringVar()
statusvar = tk.StringVar()


# Title
titleframe = tk.Frame(root)
titlelabel = tk.Label(titleframe, text = "\n" + apptitle, font = ("Heiti TC", 32))
titlelabel.pack()
titleframe.pack()



def run_b():
	hourly_in()
	to_print.set(battery.add())
	eachactionupdate()
def run_d():
	hourly_in()
	to_print.set(display.add())
	eachactionupdate()




buttonframe = tk.Frame(root)

batteryquote = tk.Button(buttonframe, pady = 2, padx= 9, \
	 text = "Quote Battery/Other", command = run_b)
batteryquote.grid(row=0, column=0)

displayquote = tk.Button(buttonframe, text = "Quote Display", command = run_d)
displayquote.grid(row=0, column=1)

buttonframe.pack()

consoleframe = tk.Frame(root)
console = tk.Label(consoleframe, textvariable=to_print, font = ("Heiti TC", 24))
console.pack()
status = tk.Label(consoleframe, textvariable=statusvar, font = ("Heiti TC", 15))
status.pack()
consoleframe.pack()


if __name__ == "__main__":
	root.mainloop()

