"""
GUI for a Linux auto-clicker written in python. 
Uses Tkinter to get relevant info from the user to create an AutoClicker object.

Author: Julian Jocque
Date: 8/16/2014

Updated by: Carsten Ziegler
Date: 2/17/2018
"""

from autoClicker import AutoClicker
import tkinter as tk
from tkinter import messagebox

class AutoClickerGUI:

    def __init__(self, parent):
        self.initGUI(parent)
        self.clicker = AutoClicker()

    def initGUI(self, parent):
        """
        Initializes the GUI
        """
        self.parent = parent
        parent.wm_title("Felix Ziegler's AutoClicker")
        parent.protocol("WM_DELETE_WINDOW", self.cleanUp)
        self.panel = tk.Frame(parent)
        self.panel.grid()

        vcmd = (parent.register(self.validateInt), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.CPS =      tk.IntVar(parent, value=50)
        self.delay =    tk.IntVar(parent, value=20)
        self.keyToUse = tk.StringVar(parent, value="Caps_Lock")
        self.method =   tk.StringVar(parent, value="Hold")

        self.CPSText =      tk.Label(parent, text="Clicks Per Second").grid(row=0, sticky=tk.W)
        self.MSText =       tk.Label(parent, text="MS of random delay").grid(row=1, sticky=tk.W)
        self.keyToUseText = tk.Label(parent, text="Key to use (Caps_Lock, Shift_L, ...)").grid(row=2, stick=tk.W)
        self.methodText =   tk.Label(parent, text="Clicking Method").grid(row=3, stick=tk.W)

        self.CPSEntry =           tk.Entry(parent, validate = "key", validatecommand = vcmd, textvariable=self.CPS)
        self.MSEntry =            tk.Entry(parent, textvariable=self.delay)
        self.keyToUseEntry =      tk.Entry(parent, textvariable=self.keyToUse)
        self.methodEntry =        tk.OptionMenu(parent, self.method, "Hold", "Toggle")
        self.applyChangesButton = tk.Button(parent, text="Apply Changes", command=self.updateClicker)

        self.CPSEntry.grid(row=0, column=1)
        self.MSEntry.grid(row=1, column=1)
        self.keyToUseEntry.grid(row=2, column=1)
        self.methodEntry.grid(row=3, column=1)
        self.applyChangesButton.grid(row=4, columnspan=2)


    def cleanUp(self):
        """
        Stops the AutoClicker before closing
        """
        self.clicker.cleanUp()
        self.parent.destroy()

    def updateClicker(self):
        """
        Updates the autoclicker with the current information in the GUI.
        Returns True if it successfully updated, else returns False
        """
        try:
            CPS = self.CPS.get()
            delay = self.delay.get()
            keyToUse = self.keyToUse.get()
        except ValueError:
            self.showInputError()
            return False
        hold = False
        toggle = False
        if self.method.get() == "Hold":
            hold = True
        else:
            toggle = True
        self.clicker.cleanUp()
        try:
            self.clicker = AutoClicker(clicksPerSecond = CPS, randomizeRange = delay, toggleClick = toggle,
                                        holdClick = hold, keyToUse = keyToUse)
        except ValueError:
           self.showInputError()
           return False
        return True

    def showInputError(self):
        """
        Shows a message box alerting the user that there was errors with their input.
        """
        messagebox.showinfo("Error", "One or more of the values you inputted is invalid")

    def validateInt(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        """
        Validates that an Entry always contains only an int or is empty.
        """
        if value_if_allowed == "":
            return True
        if text in '0123456789':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

if __name__ == "__main__":
    window = tk.Tk()
    gui = AutoClickerGUI(window)
    window.mainloop()
