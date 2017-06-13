'''
Created on May 28, 2017

@author: luciachen
'''
import urllib.request
import json
from tkinter import Tk, Frame, Label, Entry, Text, Button, TOP, BOTTOM, END
from tkinter.messagebox import showinfo

class Tour:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def distance(self, mode = "driving"):
        self.mode = mode
        self.url = 'http://maps.googleapis.com/maps/api/distancematrix/json'
        self.value = {'origins': '{}'.format(self.origin), 'destinations': '{}'.format(self.destination), 'mode': '{}'.format(self.mode), 'sensor': 'false'}
        self.user_agent = 'Mozilla/5.0'
        self.headers = {'User-Agent': self.user_agent}
        self.data = urllib.parse.urlencode(self.value)
        self.url = self.url + '?' + self.data
        self.req = urllib.request.Request(self.url, None, self.headers)
        self.response = urllib.request.urlopen(self.req)
        self.jsonresponse = json.loads(self.response.read())
        try:
            self.value = self.jsonresponse['rows'][0]['elements'][0]['distance']['value']
        except KeyError:
            self.value = ""
        return(self.value)

class TourGui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.userinput = Frame(self)
        self.originLabel = Label(self.userinput, text = 'Origin')
        self.originEnt = Entry(self.userinput)
        self.destinationLabel = Label(self.userinput, text = 'Destination')
        self.destinationEnt = Entry(self.userinput)
        self.modeLabel = Label(self.userinput, text = 'Mode')
        self.modeEnt = Entry(self.userinput)
        self.userinput.pack(side = TOP)
        self.originLabel.pack()
        self.originEnt.pack()
        self.destinationLabel.pack()
        self.destinationEnt.pack()
        self.modeLabel.pack()
        self.modeEnt.pack()
        self.result = Frame(self)
        self.distanceLabel = Label(self.result, text = 'Distance (m)')
        self.distanceText = Text(self.result, height = 1, width = 25)
        self.distanceButton = Button(self.result, text = 'Get Distance', command = self.onClick)
        self.result.pack(side = BOTTOM)
        self.distanceLabel.pack()
        self.distanceText.pack()
        self.distanceButton.pack()
    
    def onClick(self):
        self.origin = self.originEnt.get()
        self.destination = self.destinationEnt.get()
        self.mode = self.modeEnt.get().lower()
        self.value = Tour(self.origin, self.destination)
        if self.mode == "driving" or self.mode == "walking" or self.mode == "bicycling":
            self.display = self.value.distance(self.mode)
            if self.display != "":
                self.distanceText.delete(0.0, END)
                self.distanceText.insert(0.0, self.display)
            else:
                showinfo(message = "Distance between {} and {} not found".format(self.origin, self.destination))
        elif self.mode == "":
            self.display = self.value.distance()
            if self.display != "":
                self.distanceText.delete(0.0, END)
                self.distanceText.insert(0.0, self.display)
            else:
                showinfo(message = "Distance between {} and {} not found".format(self.origin, self.destination))
        else:
            self.display = ""
            showinfo(message = "Invalid mode. Valid modes are 'driving', 'bicycling', and 'walking'.")

def main(): 
    root = Tk()
    gui = TourGui(root)
    gui.mainloop()
    
if __name__ == '__main__': main()
        

        
        