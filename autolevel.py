# -*- coding: utf-8 -*-
import numpy as np
import cv2


def ComputeMinLevel(hist, pnum):
    index = np.add.accumulate(hist)
    return np.argwhere(index>pnum * 8.3 * 0.01)[0][0]


def ComputeMaxLevel(hist, pnum):
    hist_0 = hist[::-1]
    Iter_sum = np.add.accumulate(hist_0)
    index = np.argwhere(Iter_sum > (pnum * 2.2 * 0.01))[0][0]
    return 255-index


def LinearMap(minlevel, maxlevel):
    if (minlevel >= maxlevel):
        return []
    else:
        index = np.array(list(range(256)))
        screenNum = np.where(index<minlevel,0,index)
        screenNum = np.where(screenNum> maxlevel,255,screenNum)
        for i in range(len(screenNum)):
            if screenNum[i]> 0 and screenNum[i] < 255:
                screenNum[i] = (i - minlevel) / (maxlevel - minlevel) * 255
        return screenNum


def CreateNewImg(img):
    h, w, d = img.shape
    newimg = np.zeros([h, w, d])
    for i in range(d):
        imghist = np.bincount(img[:, :, i].reshape(1, -1)[0])
        minlevel = ComputeMinLevel(imghist,  h * w)
        maxlevel = ComputeMaxLevel(imghist, h * w)
        screenNum = LinearMap(minlevel, maxlevel)
        if (screenNum.size == 0):
            continue
        for j in range(h):
            newimg[j, :, i] = screenNum[img[j, :, i]]
    return newimg

#曝光调整函数    
def gamma_trans(img,gamma):#gamma函数处理
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)]#建立映射表
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)#颜色值为整数
    return cv2.LUT(img,gamma_table)#图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。
    
def contrast_bright(img, c, b):
    h, w, ch = img.shape
    blank = np.zeros([h, w, ch], img.dtype)
    dst = cv2.addWeighted(img, c, blank, 1-c, b)
    return dst

if __name__ == '__main__':
    
    img = cv2.imread('./37.jpg')
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #cl1 = clahe.apply(img)
 
    #cv2.imshow('img',img)
    #cv2.imshow('cl1',cl1)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #newimg = CreateNewImg(img)
    #newimg=gamma_trans(img,0.5) #1为不调整，大于1，降低曝光，小于1，增强曝光，指数变化
    newimg=contrast_bright(img, 0.8, -20) #, 1为不变，0为亮度不变
    cv2.imshow('original_img', img)
    cv2.imshow('new_img', newimg / 255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
