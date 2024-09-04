import os
from os.path import join
import cv2
import numpy as np
f = "/media/HDD2/VITON/StableVITON_git/StableVITON/test/test_pairs.txt"
images_root = "/media/HDD2/VITON/StableVITON_git/StableVITON/test/test"
f = open(f, "r+")
for line in f.readlines():
    l = line.split()
    person = l[0]
    cloth = l[1]
    result = person.split(".")[0]+"_"+cloth.split(".")[0]+".jpg"
    print(person, result)
    img1 = cv2.imread(join(images_root,"image", person))
    arr = cv2.imread(join(images_root,"agnostic-v3.2", person))
    indices_to_replace = np.where(np.all(arr == (128,128,128), axis=-1))
    print(indices_to_replace)
    out_image = cv2.imread(join("/media/HDD2/VITON/StableVITON_git/StableVITON/samples/unpair", result))
    out_image = cv2.resize(out_image, (768,1024), interpolation = cv2.INTER_NEAREST)
    img1[indices_to_replace] = out_image[indices_to_replace]
    cv2.imwrite(result, img1)

