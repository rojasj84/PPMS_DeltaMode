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

# Class to check if the file was edited                       
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')
        # Add your update logic here
        #print("File Was Changed")
        
        observer.pause()

        #Update the data file to get new values
        print("Observer Paused")

        #data_plots.update_graphs()
        time.sleep(0.5)
        
        observer.resume()
        print("Observer Resumed")

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

#function will read the last line of the datafile
def get_last_row(filename):
    with open(filename, 'rb') as file:
        file.seek(-2, 2)  # Go to the second to last byte
        while file.read(1) != b'\n':
            file.seek(-2, 1)  # Step back by 2 bytes
        last_row = file.readline().decode()
        return last_row

if __name__ == "__main__":

    window = tk.Tk()
    window.title("PPMS Data Gathering")
    window.geometry("1000x400")

    file_path = 'data/example.dat'
    complete_file_path = os.path.abspath(file_path)

    QD_DataFile = DataFile(complete_file_path)

    print(QD_DataFile.time_data_array)

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