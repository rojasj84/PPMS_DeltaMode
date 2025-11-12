import csv
import os

import numpy as np




if __name__ == "__main__":

    file_path = 'data/example.dat'
    complete_file_path = os.path.abspath(file_path)

    with open(complete_file_path, newline='') as csvfile:
        
        # Read in and ignore the first 19 rows that are part of the file header
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for i in range(19):
            qd_datfile_file_header = next(csv_reader)  # Reads the first row as the header
            #print("Header rows:", qd_datfile_file_header)       

        # Read in the column header for the data fields
        qd_datfile_data_field_names = next(csv_reader)  # Reads the first row as the header
        #print("Data field names:", qd_datfile_data_field_names)       

        # Read in the file data into a numpy data structur
        qd_datafile_total_data = np.zeros((2), dtype= float)
        temp_data_array = np.zeros((2), dtype= float)
        #qd_datafile_temperature_data = []

        while True:
            try:
                qd_datfile_data_row = next(csv_reader)
                temp_data_array[0] = qd_datfile_data_row[1]
                try:
                    temp_data_array[1] = qd_datfile_data_row[3]
                except:
                    temp_data_array[1] = 0
                #qd_datafile_temperature_data[count] = qd_datfile_data_row[3]
                #print(qd_datafile_time_data)
                #print("Reached the end of the CSV file.")
            except FileNotFoundError:
                print("Error: The specified CSV file was not found.")
            except Exception as e:
                print(f"End of File Reached: {e}")
                break
        
        
        print(temp_data_array)

    
        
            
        
            


                    

