# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:54:40 2020

@author: JEOL
"""
from PIL import Image
import numpy as np
import time
#from PIL import Image
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime
import sys
from PyQt4 import QtCore, QtGui, uic
#from PyJEM import TEM3
from PyJEM import TEM3


qtCreatorFile =  "Emission stab.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Emission Stab")
        count=self.COUNT.text()
        #print (count)
        interval_time =self.INTERVAL.text()
        #print(interval_time)
        self.START.clicked.connect(self.start)
        
        
    def start(self):
        count=int(self.COUNT.text())
        print ("counts:",count)
        interval_time =int(self.INTERVAL.text())
        print("interval_time:",interval_time)
        _gun_instance = TEM3.HT3()
        ht=int( _gun_instance.GetHtValue())
        print ('HT:',ht)
        FEG = TEM3.GUN3()
        
        """
        #CSV
        import csv
        with open('emission.csv', 'wb') as csvfile:
            fieldnames = ['DATE','TIME','-', 'emission']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writerow({'DATE': ht, 'TIME': count})
        """    
        
        
        
        
        
        
        
        file = open("log.txt", "w")
        x = []
        y = []
        value=15
        start=time.time()
        print ("start time=",start)
        value = FEG.GetEmissionCurrentValue()
        for i in range(count):
            # value for online
            value = FEG.GetEmissionCurrentValue()
            
            
            A1=FEG.GetAnode1CurrentValue()
            
            A1=round(A1,2)
            #print (round(value,2))
            
            #value for test offline:
            #value=value-0.1
            #from random import randint
            #value =randint(10,15)
            #####  end test offline
            
            A=datetime.datetime.today()
            C=str(A.strftime("%d_%m_%Y"))
            C=str(C)
            print(C)
            B=A.strftime(("%H:%M:%S "))
            print(B)
            
            #formating date and time
            H=B[0:2]
            print(H)
            M=B[3:5]
            print(M)
            S=B[6:9]
            print(S)
            H=float(H)*60
            M=float(M)
            S=float(S)/60
            B=S+M+H
            B=round(B,3)
            print("time in second: ",round(B,3))
            x.append(B)
            y.append(value)
            print("Emission: " + str(round(value,2)))
            
            HV=str(int(ht/1000))+"kv"
            date = datetime.datetime.today()
            write_data = date.strftime("%Y/%m/%d,%H:%M:%S ") + ",EmissionValue:, " + str(value) + "\n"
            file.write(write_data)
            time.sleep(interval_time)
        file.close()
        end=time.time()
        print("end time=",end)
        elapstime=round(end-start,1)
        print ("elapsed time=",elapstime)
        D="Emission Stability"+"\n"+str(date.strftime("%d/%m/%Y")) +"\n" +str(ht/1000)+"kv"+"  A1:"+str(A1)+"kv"
        print(D)
        # plotting graph of emission vs time
        #plt.plot(x, y, "b*-")
        #plt.plot(x,y,"b:",linestyle=":",marker="o",markersize=10,color='y',label='Emission')
        plt.plot(x,y,"b:",marker="o",markersize=10,color='y',label='Emission')
        plt.legend (loc='upper right', shadow=True)
        plt.xlabel("Plot time:"+str(elapstime)+"sec"+"           Time/mn")
        plt.ylabel("Emission Value"+"    (µA)")
        plt.title(D,fontsize=14,verticalalignment='center')
        plt.grid(True)
        plt.vlines(x,[0],y,colors='r', linestyles='dashdot')
        ymax=17
        ymin=2
        plt.ylim(ymin,ymax)
        #plt.show()
        img="Emission Stab "+C+" "+HV+".jpg"
        plt.savefig(img)
        plt.show()
        #plt.savefig(img)
        #item=C
        #plt.savefig(str(item) + '.jpg')
        
        """
        img = mpimg.imread(img)
        imgpil = Image.fromarray(img)
        img = np.array(imgpil)
        plt.imshow(img)
        """
        
            
        
        
#if __name__ == "__main__":
app = QtGui.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())