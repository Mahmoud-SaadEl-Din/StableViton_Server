import cv2
from os.path import join
import os
import numpy as np
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def resize_viton_input(root):
    l = ["agnostic-mask","agnostic-v3.2","cloth", "image", "image-densepose"]
    # l = ["image"]
    for dir in l:
        for image in os.listdir(join(root,dir)):
            resized_image = image_resize(cv2.imread(join(root,dir,image)),height= 1024)
            cv2.imwrite(join(root,dir, image), resized_image)
            print(resized_image.shape)



def crop_viton_input(root):
    for image in os.listdir(join(root,"agnostic-v3.2")):
        arr = cv2.imread(join(root,"agnostic-v3.2", image))
        indices_to_replace = np.where(np.all(arr == (128,128,128), axis=-1))
        y1,y2 = np.min(indices_to_replace[0]), np.max(indices_to_replace[0])
        x1,x2 = np.min(indices_to_replace[1]), np.max(indices_to_replace[1])
        # arr[indices_to_replace] = [0,255,0]
        # cv2.imwrite(join(root,"agnostic-v3.2", image+"temp.png"), arr)
        # print(len(indices_to_replace))
        # print(y1,y2, x1,x2)
        l = ["agnostic-v3.2","image", "image-densepose"]
        for dir in l:
            resized_image = cv2.imread(join(root,dir,image))[y1:y2, x1:x2]
            # resized_image =cv2.circle(resized_image, (x1,y1), radius=5, color=(0, 0, 255), thickness=-1)
            # resized_image =cv2.circle(resized_image, (x2,y2), radius=5, color=(0, 0, 255), thickness=-1)

            cv2.imwrite(join(root,dir, image), resized_image)
            # print(resized_image.shape)

crop_viton_input("/media/HDD2/VITON/StableVITON_git/StableVITON/test/test")