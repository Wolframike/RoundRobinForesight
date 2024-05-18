from simulation import simulation
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
	root = tk.Tk()
	root.title("RoundRobinForesight")
	root.geometry("1600x1200+500+200")  # Set initial size and position
	root.resizable(False, False)  # Make the window size unchangeable

	def on_closing():
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()
	
	root.protocol("WM_DELETE_WINDOW", on_closing)

	simulation(root)

	root.mainloop()