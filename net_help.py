import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import shutil
import cv2
from os.path import join
import time
import numpy as np
from PIL import Image
# Set sample
import numpy as np
import pandas as pd
import os
from os.path import join
import random
import argparse, requests

def send_to_diffusion1(image_path,image_name, type):
    # URL of the GPU server where you'll upload the image
    gpu_server_url = 'http://62.67.51.24:5903/server_2_call'  # Replace with your GPU server's URL

    try:
        with open(image_path, 'rb') as image_file:
            files = {
                'image': image_file,
            }
            data = {
                'path': image_name,
                'type': type
            }

            response = requests.post(gpu_server_url, files=files, data=data)

            if response.status_code == 200:
                print("Files successfully uploaded to GPU server")
                return response.text  # Return the response if required
            else:
                print("Failed to upload files to GPU server")
                return None
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        return None
    
r= "/media/HDD2/VITON/pose_classification/poses_data/train/pose"
for image_path in os.listdir(r):
    send_to_diffusion1(join(r, image_path), image_path, "image")