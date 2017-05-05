# Random Sierpinski
#
# Written by Michael Kersting Jr.
import Tkinter as tk
import tkMessageBox as tkm
import random
import time

# Version string
version = "1.0"

#
#
#
#
#
# Main window class
class MainWindow():

    #
    #
    # Init method
    def __init__(self, root):
        # Create instance variables
        self.root = root
        self.cornerColor = "#0077FF"
        self.pointColor = "#FFFFFF"
        self.bgColor = "#757575"
        self.seedVar = tk.StringVar(self.root, value="12345")
        self.iterVar = tk.StringVar(self.root, value="1")
        self.clickCoords = (-1, -1)

        # Flags
        self.flag_stop = False

        # Create widgets
        self.canvas = tk.Canvas(self.root, bg=self.bgColor)
        self.seedLabel = tk.Label(self.root, text="Random # Generator Seed")
        self.seedEntry = tk.Entry(self.root, textvariable=self.seedVar)
        self.iterLabel = tk.Label(self.root, text="Iterations per second")
        self.iterEntry = tk.Entry(self.root, textvariable=self.iterVar)
        self.startButton = tk.Button(self.root, text="Start Simulation", command=self.startSimulation)
        self.aboutButton = tk.Button(self.root, text="About", command=self.showInfo)

        # Pack widgets
        self.canvas.pack()
        self.seedLabel.pack()
        self.seedEntry.pack()
        self.iterLabel.pack()
        self.iterEntry.pack()
        self.startButton.pack()
        self.aboutButton.pack()

        # Place widgets
        self.canvas.place(x=200, y=5, width=595, height=590)
        self.seedLabel.place(x=5, y=5)
        self.seedEntry.place(x=5, y=30, width=190)
        self.iterLabel.place(x=5, y=60)
        self.iterEntry.place(x=5, y=85, width=190)
        self.startButton.place(x=5, y=530, width=190)
        self.aboutButton.place(x=5, y=565, width=190)

        # Window configuration
        self.root.geometry("800x600")
        self.root.wm_title("RandomSierpinski v%s" % version)

        # Bind the mouse to the canvas
        self.canvas.bind("<Button-1>", self.__canvasClickCallback__)

    #
    #
    # Start simulation method
    def startSimulation(self):
        # Check the parameters from our entry boxes
        try:
            int(self.seedVar.get())
        except ValueError:
            tkm.showerror("Input Error", "The seed must be an integer")
            return
        try:
            int(self.iterVar.get())
        except ValueError:
            tkm.showerror("Input Error", "The iteration value must be an integer")
            return
        if int(self.iterVar.get()) < 1:
            tkm.showerror("Input Error", "Iteration value must be greater than 1")
            return
        
        # Disable parts of the UI and clear the canvas and old coordinates
        self.seedEntry.config(state=tk.DISABLED)
        self.iterEntry.config(state=tk.DISABLED)
        self.startButton.config(state=tk.DISABLED)
        self.canvas.delete("all")
        self.getCanvasClick()
        
        # Get the user to place the 3 points on the canvas
        text = self.canvas.create_text(10, 10, text="Click and place 3 points", anchor=tk.NW)
        corners = list()
        while len(corners) < 3:
            point = self.getCanvasClick()
            if point != None:
                corners.append(point)
                self.canvas.create_oval(point[0], point[1], point[0]+5, point[1]+5, fill=self.cornerColor)
                print "Point placed at " + str(point)
            self.root.update()
        self.canvas.delete(text)

        # Configure the button for stopping
        self.startButton.config(text="Stop Simulation", command=self.stopSimulation, state=tk.NORMAL)

        # Place points randomly halfway
        self.flag_stop = False
        delay = 1.0 / int(self.iterVar.get())
        random.seed(int(self.seedVar.get()))
        lastPoint = (100, 100)
        lastTime = time.time()
        while self.flag_stop == False:
            if (time.time() - lastTime >= delay):
                # Pick a random corner
                randomC = random.randint(0, 2)
            
                # Calculate the halfway point
                halfX = (lastPoint[0] + corners[randomC][0])/2
                halfY = (lastPoint[1] + corners[randomC][1])/2

                # Place the dot, save it as the last point, and reset the last time
                self.canvas.create_oval(halfX, halfY, halfX+1, halfY+1, fill=self.pointColor, width=0)
                lastPoint = (halfX, halfY)
                lastTime = time.time()

            # Update the root window
            self.root.update()

        # Re-enable the UI and change the start button back
        self.seedEntry.config(state=tk.NORMAL)
        self.iterEntry.config(state=tk.NORMAL)
        self.startButton.config(text="Start Simulation", command=self.startSimulation)

    #
    #
    # Stop simulation method
    def stopSimulation(self):
        self.flag_stop = True

    #
    #
    # Get canvas click method
    def getCanvasClick(self):
        if self.clickCoords != (-1, -1):
            data = self.clickCoords
            self.clickCoords = (-1, -1)
            return data
        else:
            return None

    #
    #
    # Canvas click callback
    def __canvasClickCallback__(self, event):
        self.clickCoords = (event.x, event.y)

    #
    #
    # Show info method
    def showInfo(self):
        message = "RandomSierpinski v%s\nWritten by Michael Kersting Jr.\n\nInspired by this Numberphile video:\nhttps://youtu.be/kbKtFN71Lfs" % version
        tkm.showinfo(title="About", message=message)
#
#
#
#
#
# Set up and run the program
root = tk.Tk()
window = MainWindow(root)
root.mainloop()
