keithley_6112_address = "GPIB0::12::INSTR"   #replace the 7 with your scope's GPIB address!
import pyvisa
import time
#from pymeasure.instruments.keithley import Keithley6221
#import pymeasure.instruments.keithley as pym

gpib_comm = pyvisa.ResourceManager()
keithley_6112 = gpib_comm.open_resource(keithley_6112_address)
'''print(keithley_6112.write('SOUR:DELT:ARM'))
time.sleep(1)
print(keithley_6112.write('INIT:IMM'))'''

'''print(keithley_6112.write('*RST'))
time.sleep(.5)
print(keithley_6112.write('SOUR:DELT:HIGH 1e-3')) #Sets high source value to 1mA.
time.sleep(.5)
print(keithley_6112.write('SOUR:DELT:DELay 100e-3')) # Sets Delta delay to 100ms.
time.sleep(.5)
print(keithley_6112.write('SOUR:DELT:COUN INF')) # Sets Delta count to infinite.
time.sleep(.5)
print(keithley_6112.write('SOUR:DELT:CAB ON')) # Enables Compliance Abort.
time.sleep(.5)
print(keithley_6112.write('TRAC:POIN 10')) # Sets buffer to 1000 points. A
time.sleep(.5)
print(keithley_6112.write('SOUR:DELT:ARM')) # Arms Delta.
time.sleep(2)
print(keithley_6112.write('INIT:IMM'))
time.sleep(1)
print(keithley_6112.write('UNIT OHMS'))'''


#time.sleep(5)
#print(keithley_6112.write('SENS:DATA:LAT?'))
#print(keithley_6112.write('SOUR:SWE:ABOR'))
#print(keithley_6112.write('FETC:Delt?'))
#keithley_6112.write('TRAC:CLE')
#keithley_6112.write('SOUR:DELT:COUN INF')
#keithley_6112.write('INIT:IMM')
#time.sleep(.25)
for i in range (100):
    data_string = keithley_6112.query('SENS:DATA:FResh?')

    #Parse the data string into a list of floating-point numbers
    data_list = [float(x) for x in data_string.strip().split(',')]

    print(data_list)
    time.sleep(0.1)