import numpy as np
import cv2 as cv
from skimage import io
from skimage.filters import (
    threshold_multiotsu, threshold_niblack, threshold_sauvola, threshold_otsu)
from skimage.util import (img_as_float, img_as_ubyte)
import math


def path(path):
    return ".{path}"


def read(img):
    image_path = path(img)
    image = cv.imread(image_path)
    return image


im = read("image")


class Binarization:

    @staticmethod
    def default(image, thresh=127, kernel=None, c=None, k=None):
        pass

    @staticmethod
    def globalFixed(image, thresh=127, kernel=None, c=None, k=None):
        return cv.threshold(image, thresh, 255, cv.THRESH_BINARY)

    @staticmethod
    def otsu(image, thresh, kernel, c, k):
        return cv.threshold(
            image, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

    @staticmethod
    def multi(image, thresh, kernel, c, k):
        thresholds = threshold_multiotsu(image)
        im = image.copy()
        a, b = thresholds
        im[image < a] = 0
        im[image >= a] = 255
        im[image > b] = 0
        return thresholds, im

    @staticmethod
    def mean(image, thresh=None, kernel=199, c=5, k=None):
        return None, cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                          cv.THRESH_BINARY, kernel, c)

    @staticmethod
    def gaussian(image, thresh=None, kernel=199, c=5, k=None):
        return thresh, cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv.THRESH_BINARY, kernel, c)

    @staticmethod
    def sauvola(image, thresh=None, kernel=199, c=5, k=None):
        thresh = threshold_sauvola(image, window_size=kernel, k=k)
        return thresh, img_as_ubyte(image > thresh)

    @staticmethod
    def niblack(image, thresh=None, kernel=199, c=5, k=None):
        thresh = threshold_niblack(image, window_size=kernel, k=k)
        return thresh, img_as_ubyte(image > thresh)


class Filter:

    @staticmethod
    def sobel(image, thresh=None, kernel=199, c=5, k=None):
        sobel_x = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3)
        sobel_y = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=3)
        sobel_x = np.uint8(np.absolute(sobel_x))
        sobel_y = np.uint8(np.absolute(sobel_y))
        return thresh, cv.bitwise_or(sobel_x, sobel_y)

    @staticmethod
    def canny(image, thresh=None, kernel=5, c=5, k=None):
        return thresh, cv.Canny(image, 80, 100)

    @staticmethod
    def laplacian(image, thresh=None, kernel=5, c=5, k=None):
        blur = cv.GaussianBlur(image, (kernel, kernel), 0)
        lap = cv.Laplacian(blur, cv.CV_64F, ksize=kernel)
        return thresh, np.uint8(np.absolute(lap))

    @staticmethod
    def median(image, thresh=None, kernel=5, c=5, k=None):
        return thresh, cv.medianBlur(image, kernel)

    @staticmethod
    def gaussian(image, thresh=None, kernel=5, c=5, k=None):
        return thresh, cv.GaussianBlur(image, (kernel, kernel), 0)


class Morphology:

    @staticmethod
    def dilation(image, thresh=None, kernel=5, c=5, k=None):
        kernel = np.ones((kernel, kernel), np.uint8)
        return thresh, cv.dilate(image, kernel, iterations=1)

    @staticmethod
    def erosion(image, thresh=None, kernel=5, c=5, k=None):
        kernel = np.ones((kernel, kernel), np.uint8)
        return thresh, cv.erode(image, kernel, iterations=1)


class Processing:

    def __init__(self, image, lyr1=None, lyr2=None, lyr3=None, thresh=127, kernel=5, c=5, k=0.2):
        self.image = image
        self.grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        self.lyr1 = lyr1
        self.lyr2 = lyr2
        self.lyr3 = lyr3
        self.thresh = thresh
        self.kernel = kernel
        self.c = c
        self.k = k

    def result(self):
        if (self.lyr1 is not None):
            thr, self.result = self.lyr1(
                self.grayImage, self.thresh, self.kernel, self.c, self.k)
        else:
            self.result = self.grayImage
        if (self.lyr2 is not None):
            thr, self.result = self.lyr2(
                self.result, self.thresh, self.kernel, self.c, self.k)
        if (self.lyr3 is not None):
            thr, self.result = self.lyr3(
                self.result, self.thresh, self.kernel, self.c, self.k)
        return self.result
