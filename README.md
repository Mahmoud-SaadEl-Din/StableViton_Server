# StableViton_Server
This repo for production. Making Microservice of [StableVITON](https://arxiv.org/abs/2312.01725) to use it in different applications


## Environments
```bash
git clone https://github.com/rlawjdghek/StableVITON
cd StableVITON

conda create --name StableVITON python=3.10 -y
conda activate StableVITON

# install packages
pip install torch==2.0.0+cu117 torchvision==0.15.1+cu117 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu117
pip install pytorch-lightning==1.5.0
pip install einops
pip install opencv-python==4.7.0.72
pip install matplotlib
pip install omegaconf
pip install transformers==4.33.2
pip install xformers==0.0.19
pip install triton==2.0.0
pip install open-clip-torch==2.19.0
pip install diffusers==0.20.2
pip install scipy==1.10.1
pip install clean-fid # this line is missing from original repo. we added it
conda install -c anaconda ipython -y
```

## Model weights
Original model of StableViton can be download from here. It's called [VITONHD](https://kaistackr-my.sharepoint.com/personal/rlawjdghek_kaist_ac_kr/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Frlawjdghek%5Fkaist%5Fac%5Fkr%2FDocuments%2FStableVITON&ga=1). It's around 6.9G. 

download from sharepoint is not easy throught terminal (for server). so I will provide link for GoogleDrive to download soon.


prepare the test data in the following structure.
```
test
|-- image
|-- image-densepose
|-- agnostic
|-- agnostic-mask
|-- cloth
|-- test_pairs.csv
```

## Inference
```bash
# paired setting
python inference.py --config_path ./configs/VITON512.yaml --batch_size 4 --model_load_path <model weight path> --save_dir <save directory>

# unpaired setting
python inference.py --config_path ./configs/VITON512.yaml --batch_size 4 --model_load_path <model weight path> --unpair --save_dir <save directory>
```

You can also preserve the unmasked region by '--repaint' option. 


**Acknowledgements** Sunghyun Park is the corresponding author.

## License
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
