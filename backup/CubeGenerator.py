import numpy as np
from scipy import misc
from libtiff import TIFFfile
from libtiff import TIFF
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from math import *
import cv2
import sys
import os

class FileTIFFWorker(object):

    def __init__(self,dir_name_input):
        self.dir_name_input = dir_name_input
        self.dir_name_output = "./"
        
    def writeTIFF(self,filename,array):
        #tif = TIFF.open(filename,mode = 'w')       
        #for zInd in range(3):
        #tif.write_image(array[:,:,:],compression=compression, write_rgb=True)
        #tif.close()
        cv2.imwrite(filename,array)

    def readTIFF(self,filename):
        return cv2.imread(filename,-1)

    def readImages(self,filename):
        imgs = []
        with open(self.dir_name_input + filename) as f:
            for line in f:
                line = line.splitlines()[0]
                img = self.readTIFF(self.dir_name_input + line)
                rows, cols = img.shape
                imgs.append(img)
        
        return (imgs , rows , cols)

class CubeGenerator(object):

    def __init__(self,inputDirectory,fileInput,height_wavelength,binning_spectral):
        self.fileInput = fileInput
        self.height_wavelength = height_wavelength
        self.binning_spectral = binning_spectral
        self.inputDirectory = inputDirectory
        self.fileWorker = FileTIFFWorker(inputDirectory)
        self.init()
    
    def init(self):
        self.inputImgs , rows , cols = self.fileWorker.readImages(self.fileInput)      
        #set output parameters
        num_images_input = len(self.inputImgs)
        self.setOutputParameters(num_images_input,rows,cols)

    def setOutputParameters(self,num_images_input,rows,cols):
        self.num_images_out = rows/self.height_wavelength
        self.rows_output = num_images_input
        self.cols_output = cols

    def getRow(self,img,row_index):
        return img[row_index,0:] 

    def getImage(self,waveLengthIndex,scale = False):
        output = np.zeros((self.rows_output,self.cols_output),np.int16)        
        j = 0
        for inputImg in self.inputImgs:
            rowWaveLength = self.getRow(inputImg,waveLengthIndex)#se obtiene la fila k-esima de la i-esima imagen
            output[j] = rowWaveLength
            j+=1
        if scale :
            self.scaleData(output)
        return output

    def generateCube(self):
        for waveLengthIndex in range(self.num_images_out):
            result = self.getImage(waveLengthIndex)
            waveLength = 1.0*0.000014*waveLengthIndex*waveLengthIndex*self.binning_spectral + 0.5092*waveLengthIndex**self.binning_spectral + 399.1945;
            self.fileWorker.writeTIFF("longitud%.2f.tif"%(waveLength),result)

    def generateRGB(self, scale = True):
        k = 0
        bgr = range(3)
        for waveLengthIndex in [50,148,245]:
            result = self.getImage(waveLengthIndex,scale)
            bgr[k] = result
            k+=1
        bgr_img = cv2.merge(bgr)
        fileDirectory = self.inputDirectory + "output.tif"
        self.fileWorker.writeTIFF(fileDirectory,bgr_img)
        return bgr_img

    def getQImage(self,bgr_img):
        qimage = QImage(self.cols_output, self.rows_output, QImage.Format_RGB32);
        for i in range(0, self.rows_output):
            for j in range(0, self.cols_output):
                valueBGR =  bgr_img[i,j]
                value = qRgb(valueBGR[2], valueBGR[1], valueBGR[0])
                qimage.setPixel(j, i, value)
        return qimage

    def scaleData(self,img):
        rows , cols = img.shape
        maxVal = img.max()
        minVal = img.min()
        alpha = 255.0/(maxVal - minVal)
        beta = (-minVal * 255.0)/(maxVal - minVal)
        for i in range(0, rows):
            for j in range(0, cols):
                value =  img[i,j]
                value = floor(1.0*(alpha*value + beta))
                img[i,j] = value