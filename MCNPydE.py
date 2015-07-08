
''' 
Copyright (c) 2015 Megat Harun Al Rashid bin Megat Ahmad
and Rafhayudi Jamro.

All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the Malaysian Nuclear Agency. The name of the
Malaysian Nuclear Agency may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
'''

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm

#-------------------------------------------------------------#

class dataExtract(object):
    
    '''This class allows the user to view the content and
    number of lines of MCNP output file. Unless specified,
    only the first 100 lines of the file ouput content will
    be displayed. It also allows the user to extract the
    block of data, process it and display it in 2D and 3D'''
    
    def __init__(self,fileName,searchStr='There are     20 grid points along the s-axis'):
    # Initialization
    
        self.fileName = fileName
        self.searchStr = searchStr
                
        fh = open(fileName,'r')
        self.fileExtract = fh.readlines()
        
        self.lineNum = len(self.fileExtract)
        
        self.listLineNum = []
        self.blockCount = 0
        
        # Extracting the the line number of the first
        # line of the block data and number of blocks
        with open(fileName,'r') as fh2:
            for num, line in enumerate(fh2, 1):
                if searchStr in line:
                    self.listLineNum = self.listLineNum + [num]
                    self.blockCount = self.blockCount+1
                
        fh.close()
        fh2.close()
        
        # Refering the position of batch of data block
        self.key = {1:1,2:3,3:5,4:7,5:9}
        
    '''*************************************************'''
        
    def lineNumber(self):
    # Display total number of lines
    
        print self.lineNum
    
    '''*************************************************'''
    
    def rawContent(self, minLine = 0, maxLine = 99):
    # Display the content of the file
    
        lineNum=0
    
        if maxLine == -1:
            maxLine = -2
                
        for item in self.fileExtract[minLine:maxLine+1]:
            lineNum=lineNum+minLine
            print lineNum,item.replace('\r\n','')
            
    
    def dataBlockContent(self, minLine = 'False',\
                         rangeLine = 25):
    # Display the content of any of the data block
        
        if minLine == 'False':
            minLine = self.listLineNum[0]
        
        line=minLine
        indPos=0
        
        print "Use the index position to select mapping energy when plotting\n"
        print "Line Number--->Energy Index--->Line Content\n\n"
        
        for item in self.fileExtract[minLine:minLine+rangeLine+1]:
            
            if indPos >=6:
                print line,"\t",indPos-5,"\t",item
            else:
                print line,"\t\t",item
            line = line+1
            indPos=indPos+1
            
    '''*************************************************'''
            
    def listLinenumber(self):
    # Display the list of line numbers that initiates
    # the block data
        
        print "The line number list that contain the passed \n",\
        "strings is:\n"
        print self.listLineNum
        
    '''*************************************************'''
        
    def allBlockData(self, axisPt=20, axisSeq=1, lowLim=3,\
                     upLim=23):
    # Extract data in blocks as list into self.nilaiAxis
    
        self.nilaiAxis = []
        for i in range(0,self.blockCount,1):
                self.nilaiAxis = self.nilaiAxis+\
                [self.fileExtract[self.listLineNum[i]+lowLim:\
                                  self.listLineNum[i]+upLim]]
                
        # Extract x,y axes values from the first twenty blocks       
        self.axisT = []
        for j in range(0,axisPt,1):

            satuLine = self.nilaiAxis[j][axisSeq].replace('\r\n','').split()
            satuLine = (float(satuLine[1])+float(satuLine[3]))/2.0
            self.axisT = self.axisT + [satuLine]
            
        # Assigning variables for plotting later on
        self.X = np.array(self.axisT)
        self.Y = self.X
        self.L = len(self.axisT)
        
        self.dataLength2 = (len(self.axisT))**2
        self.positNo = self.blockCount/self.dataLength2
        
        print "The number of blocks are",\
        len(self.nilaiAxis)
        print "There would be", self.positNo/2, "groups of data"
    
    '''*************************************************'''
        
    def plot2D(self,dataSeq=1,energy=3,intPol = 'nearest',\
              figName = 'defaultPlot', figRes = 100,\
              colorMap = cm.gist_rainbow):
    # Plot function in 2D
    
        if energy !=3:
            energy = energy+2
        
        array_2D_MeV = []
        bil = (self.key[dataSeq]-1)*self.dataLength2
        
        for k in range(bil,self.dataLength2+bil,1):

            fastN = self.nilaiAxis[k][energy].split()
            array_2D_MeV = array_2D_MeV + [float(fastN[1])]

        array_2D_MeV = np.array(array_2D_MeV)
        array_2D_MeV=array_2D_MeV.reshape(self.L,self.L)
        
        #--------------Plotting----------------
        
        plt.imshow(array_2D_MeV,\
                   extent=(self.X.min(), self.X.max(),\
                           self.Y.max(), self.Y.min()),\
                   interpolation=intPol, cmap=colorMap)
        
        plt.colorbar()
        
        if figName != 'defaultPlot':
            plt.savefig(figName,dpi = figRes)
        
        plt.show()
        print "Energy :", fastN[0], "MeV"
        
    '''*************************************************'''
        
    def plot3D(self,dataSeq=1,energy=3,angleT=45,angleD=20,\
              figName = 'defaultPlot',figRes = 100,\
              colorMap = cm.hsv, lineGrid = 0):
    # Plot function in 3D
    
        if energy !=3:
            energy = energy+2
        
        array_2D_MeV = []
        bil = (self.key[dataSeq]-1)*self.dataLength2
        
        for k in range(bil,self.dataLength2+bil,1):

            fastN = self.nilaiAxis[k][energy].split()
            array_2D_MeV = array_2D_MeV + [float(fastN[1])]

        array_2D_MeV = np.array(array_2D_MeV)
        array_2D_MeV=array_2D_MeV.reshape(self.L,self.L)
        
        dataX = np.ones(self.dataLength2).\
        reshape(self.L,self.L)*self.X
        
        dataY = dataX.T
        
        #--------------Plotting----------------
        
        from mpl_toolkits.mplot3d.axes3d import Axes3D
                
        fig = plt.figure(figsize=(6,4))
        #ax = fig.gca(projection='3d')
        ax = Axes3D(fig)
        
        surf = ax.plot_surface(dataX, dataY, array_2D_MeV, rstride=1,\
                               cstride=1, cmap=colorMap,\
                               linewidth=lineGrid, antialiased=True,\
                               alpha=0.5)

        fig.colorbar(surf, shrink=0.6, aspect=10)
        ax.view_init(angleT, angleD)            # Angles of viewing
        
        if figName != 'defaultPlot':
            plt.savefig(figName,dpi = figRes)
            
        plt.show()
        
        print "Energy :", fastN[0], "MeV"
           