#!python3
import time
import irsdk
ir = irsdk.IRSDK()
while True:
    if(ir.startup()) :
        print("Startup successful")
        while True:
            #print(ir['Speed'])
            print(ir['Throttle'])
    else:
        print("Startup failed")
        print("waiting...")
        time.sleep(5)