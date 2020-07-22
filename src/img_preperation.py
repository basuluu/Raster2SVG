from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2
from app_exception import *


def read_img(img_path):
    return cv2.imread(img_path)

#https://www.pyimagesearch.com/2014/07/07/color-quantization-opencv-using-k-means-clustering/
def img_quantize(img, n_colors):

    if img.size < n_colors:
        raise QuantizeError('img.size < n_colors', 'ValueError')

    h, w = img.shape[:2]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    img = img.reshape((img.shape[0] * img.shape[1], 3))

    clt = MiniBatchKMeans(n_clusters=n_colors, random_state=1)
    labels = clt.fit_predict(img)
    quant = clt.cluster_centers_.astype("uint8")[labels]

    # reshape the feature vectors to images
    quant = quant.reshape((h, w, 3))
    return cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)

def img_blur(img):
    return cv2.bilateralFilter(img, 11, 17, 17)
