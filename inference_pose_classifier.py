from torchvision import datasets, transforms
import os
import torchvision
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import models
import torch, torch.nn as nn
# Data augmentation and normalization for training
# Just normalization for validation
data_transforms = transforms.Compose([transforms.Resize((512,512)),
                                      transforms.ToTensor()])

data_dir = 'test/test/image'
class PoseDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.image_list = os.listdir(data_dir)

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        img_name = os.path.join(self.data_dir, self.image_list[idx])
        image = Image.open(img_name).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, os.path.basename(img_name)  # Assuming filenames are unique identifiers


def run_classifier():
# Iterate over data.
    pose_test_dataset = PoseDataset(data_dir=data_dir, transform=data_transforms)
    dataloaders = DataLoader(pose_test_dataset,batch_size=16, # best batch size here is 16
                                            shuffle=True, num_workers=8) # best num_workers here is 8

    model_path = "classifier_ckpt/best.pt"
    resnet = models.resnet18()
    num_ftrs = resnet.fc.in_features
    resnet.fc = nn.Linear(num_ftrs, 2)

    resnet.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))

    resnet.eval()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    resnet = resnet.to(device=device)
    for inputs, names in dataloaders:#tqdm(self.val_dataloader,desc="Validation loop"):
        inputs = inputs.to(device)

        outputs = resnet(inputs)
        _, preds = torch.max(outputs, 1)
        for i in range(inputs.size(0)):
            input_image = transforms.ToPILImage()(inputs[i].cpu())
            pred = preds[i].item()
            if pred == 1:
                save_path = os.path.join("test/test/classified_poses",names[i])
            else:
                save_path = os.path.join("test/test/classified_not_poses", names[i])
            input_image.save(save_path)