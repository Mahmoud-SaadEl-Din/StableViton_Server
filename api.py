import os
from flask import Flask, render_template, jsonify
import shutil
from os.path import join
import time
import pandas as pd
import os
import argparse
from inference import run
from DB_manager_pandas import DB


app = Flask(__name__)


app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # for many images


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')
      
def save_tryon_in_DB(working_dir):
    root_ = join("/media/HDD2/VITON/StableVITON_git/StableVITON/test",working_dir)
    for image_name in os.listdir(join(root_,"TryOn")):
        shutil.copy(join(root_,"TryOn",image_name), join("/media/HDD2/VITON/CIHP_PGN/images_DB", "TryOn", image_name))

def build_args(operating_dir):
    operating_path = join("/media/HDD2/VITON/StableVITON_git/StableVITON/test", operating_dir)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="configs/VITON512.yaml")
    parser.add_argument("--model_load_path", type=str, default="VITONHD.ckpt")
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--data_root_dir", type=str, default=operating_path)
    parser.add_argument("--repaint", action="store_true")
    parser.add_argument("--unpair", action="store_true", default=True)
    parser.add_argument("--save_dir", type=str, default=join(operating_path,"TryOn"))

    parser.add_argument("--denoise_steps", type=int, default=1)
    parser.add_argument("--img_H", type=int, default=512)
    parser.add_argument("--img_W", type=int, default=384)
    parser.add_argument("--eta", type=float, default=0.0)
    args = parser.parse_args()
    return args


def prepare_samples(root):
    final_images = []
    final_clothes = []

    root_ = join("/media/HDD2/VITON/StableVITON_git/StableVITON/test",root)
    images = os.listdir(join(root_,"image"))
    clothes = os.listdir(join(root_,"cloth"))
    # random.shuffle(clothes)
    for image in images:
        for cloth in clothes:
            final_images.append(image)
            final_clothes.append(cloth)


    df = pd.DataFrame({"image": final_images, "clothes": final_clothes})
    df.to_csv(join(root_,"test_pairs.txt"), index=False, header=False, sep=" ")

@app.route('/run_SV/<string:working_dir>')
def run_SV(working_dir):
    
    db = DB()
    # Fetch data for button 1 (replace this with your logic)
    start = time.time()
    arg = build_args(working_dir)
    prepare_samples(working_dir)
    run(args=arg)
    save_tryon_in_DB(working_dir=working_dir)
    
    end= time.time()
    data = {
        "text": f"processed in {round((end-start),2)} seconds",
    }
    print(data)
    shutil.rmtree(join("/media/HDD2/VITON/StableVITON_git/StableVITON/test", working_dir))
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5901)
