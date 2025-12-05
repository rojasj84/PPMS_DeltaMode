import csv
import os
import time
import pyvisa

import tkinter as tk
import numpy as np
from tkinter import filedialog


# Class opens the data file and stores the relevant data
class DataFile:
    def __init__(self, filepath):

        self.filepath = filepath
        with open(filepath, newline='') as csvfile:
        
            # Read in and ignore the first 19 rows that are part of the file header
            csv_reader = csv.reader(csvfile, delimiter = ',')
            for i in range(19):
                qd_datfile_file_header = next(csv_reader)  # Reads the first row as the header
                #print("Header rows:", qd_datfile_file_header)       

            # Read in the column header for the data fields
            self.qd_datfile_data_field_names = next(csv_reader)  # Reads the first row as the header
            #print("Data field names:", qd_datfile_data_field_names)       


        #Obtainthe rest of the data from the csv file
        total_data_array = np.genfromtxt(filepath, delimiter=",", skip_header=20)

        #Create sub arrays for easy access to time and temperature
        self.time_data_array = total_data_array[:,1]
        self.temperature_data_array = total_data_array[:,3]         

        #function will read the last line of the datafile
    def get_last_row(self):
        with open(self.filepath, 'rb') as file:
            file.seek(-2, 2)  # Go to the second to last byte
            while file.read(1) != b'\n':
                file.seek(-2, 1)  # Step back by 2 bytes
            
            last_row = file.readline().decode()
            
            # Parse the data row with the , as the delimieter
            law_row_parsed = last_row.split(",")

            # Write down the time stamp and the temperature for that given time
            self.time_data_array = np.append(self.time_data_array, law_row_parsed[1])
            self.temperature_data_array = np.append(self.temperature_data_array, law_row_parsed[3])

            print(self.time_data_array)
            print(self.temperature_data_array)

class KeithleyConnect:
    def __init__(self, address):
        keithley_6112_address = "GPIB0::" + address + "::INSTR"
        
        #Initial connection to keithley and set up method of data gathering
        gpib_comm = pyvisa.ResourceManager()
        self.keithley_6112 = gpib_comm.open_resource(keithley_6112_address)
        self.keithley_6112.write('*RST')
        time.sleep(.5)
        self.keithley_6112.write('SOUR:DELT:HIGH 1e-3') #Sets high source value to 1mA.
        time.sleep(.5)
        self.keithley_6112.write('SOUR:DELT:DELay 100e-3') # Sets Delta delay to 100ms.
        time.sleep(.5)
        self.keithley_6112.write('SOUR:DELT:COUN INF') # Sets Delta count to infinite.
        time.sleep(.5)
        self.keithley_6112.write('SOUR:DELT:CAB ON') # Enables Compliance Abort.
        time.sleep(.5)
        self.keithley_6112.write('TRAC:POIN 10') # Sets buffer to 10 points. A
        time.sleep(.5)
        self.keithley_6112.write('SOUR:DELT:ARM') # Arms Delta.
        time.sleep(2)
        self.keithley_6112.write('INIT:IMM')
        time.sleep(1)
        self.keithley_6112.write('UNIT OHMS')
    
    def obtain_current_data(self):
        
        #Obtain latest data from Keithley 
        data_string = self.keithley_6112.query('SENS:DATA:FResh?')
        #Parse the data string into a list of floating-point numbers
        data_list = [float(x) for x in data_string.strip().split(',')]

        print(data_list)
        time.sleep(0.1)

def UpdateNumbers():
    global file_path
    global last_modified    
    
    current_modified = os.path.getmtime(file_path)
    if current_modified != last_modified:
        print(f"File modified at: {time.ctime(current_modified)}")
        QD_DataFile.get_last_row()
        print("File was changed...")
        
        last_modified = current_modified
    #time.sleep(.1)  # Check every second    
    window.after(100, UpdateNumbers)

def quit():
    window.destroy()

if __name__ == "__main__":

    window = tk.Tk()
    window.title("PPMS Data Gathering")
    window.geometry("400x400")


    button_close_program = tk.Button(window, text="EXIT", command = quit)
    button_close_program.place(x = 125, y = 10, width= 150, height= 30)

    #log.askopenfilename())
    file_path = "data/short_example.dat"
    
    # Load object to connect to Keithley via GPIB, address is 12
    Keithley6221 = KeithleyConnect("12")

    # Open dialog window that looks for the data file
    complete_file_path = os.path.abspath(file_path)
    QD_DataFile = DataFile(complete_file_path)

    #print(QD_DataFile.time_data_array)
    
    last_modified = os.path.getmtime(file_path)

    window.after(100, UpdateNumbers)
    window.mainloop()