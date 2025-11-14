import csv
import os
import time
import watchdog.observers
import contextlib

import tkinter as tk
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



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

            #print(self.temperature_data_array)


# Class to check if the file was edited                       
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')
        # Add your update logic here
        print("File Was Changed")

        # Call function to get the most recent row added to the fata file
        
        
        observer.pause()

        
        #print("Observer Paused")
        # Call the function to read the most recently written row to the data file.
        QD_DataFile.get_last_row()
        time.sleep(0.5)
        
        observer.resume()
        #print("Observer Resumed")

#Modificaiton to the observer class to be able to pause it.  Very useful.
class PausingObserver(watchdog.observers.Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(self.timeout)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextlib.contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()

if __name__ == "__main__":

    window = tk.Tk()
    window.title("PPMS Data Gathering")
    window.geometry("1000x400")

    file_path = 'data/example.dat'
    complete_file_path = os.path.abspath(file_path)

    QD_DataFile = DataFile(complete_file_path)

    #QD_DataFile.get_last_row()
    #print(QD_DataFile.time_data_array)

    event_handler = MyHandler()
    observer = PausingObserver()
    observer.schedule(event_handler, path=complete_file_path, recursive=False)
    observer.start()

    '''try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()'''

    window.mainloop()