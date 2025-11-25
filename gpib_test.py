keithley_6112_address = "GPIB0::12::INSTR"   #replace the 7 with your scope's GPIB address!
import pyvisa

gpib_comm = pyvisa.ResourceManager()
keithley_6112 = gpib_comm.open_resource(keithley_6112_address)
#print(keithley_6112.write('SOUR:DELT:ARM'))

print(keithley_6112.write('SENS:DATA:LATest?'))

