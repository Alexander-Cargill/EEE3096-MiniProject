from PyQt5 import QtWidgets, QtSerialPort, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import serial
import csv

n = 50 #button offset value
serialPort = serial.Serial(port = "COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ""  # Used to hold data coming over UART
rownum = 0 #index for csv file
currentADC = "" 
rows = [] #csv contents

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Steezy UART gang")
        self.setStyleSheet("background-color: cyan;")
        
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Welcome to the coolest UART interface this side of the Zambezi!")
        self.label1.adjustSize()
        self.label1.move(50,50)
        self.label.move(50,80)
        self.label.setText("")

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.move(20+n,0)
        self.b1.setStyleSheet("background-color: yellow;")
        self.b1.setText("Receive Transmission!")
        self.b1.adjustSize()
        self.b1.clicked.connect(self.serialVibes)
        
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setStyleSheet("background-color: yellow;")
        self.b2.move(160+n,0)
        self.b2.setText("Clear Text")
        self.b2.adjustSize()
        self.b2.clicked.connect(self.clear)
        
        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setStyleSheet("background-color: yellow;")
        self.b3.move(255+n,0)
        self.b3.setText("Log to csv")
        self.b3.adjustSize()
        self.b3.clicked.connect(self.log)
        
        self.output_text = QtWidgets.QTextEdit(readOnly=True)
        

    def update(self):
        self.label.adjustSize()
        self.label1.adjustSize()

    def serialVibes(self):
        global currentADC
        currentADC = ""
        
        self.label1.setText("Press 'log to csv' to save the ADC reading")
        self.update()
        
        temp = ""
        for i in range(14):
            serialString = serialPort.readline()
            
            if i == 0: #save ADC value for logging
                firstLine = serialString.decode('Ascii')
                currentADC = firstLine[int(firstLine.find("g"))+2:len(serialString)-1:1]
                if rownum == 0:
                    data = ["0", currentADC]
                    rows.append(data)
                else:
                    data = [str(rownum-1), currentADC]
                    rows.append(data)
                    
                    
            temp = temp + serialString.decode('Ascii')
        self.label.setText(temp)
        self.update()

    def clear(self):
        self.label.setText("")
        self.label1.setText("Welcome to the coolest UART interface this side of the Zambezi!")
        self.update()
        global currentADC
        currentADC = ""
    
    def log(self):
        global rownum
        global currentADC
        with open('ADC_READINGS.csv', 'w', encoding='UTF8') as f:
            for i in range(rownum):
                writer = csv.writer(f)
                writer.writerow(rows[i]) # write the data
            rownum+=1


def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()