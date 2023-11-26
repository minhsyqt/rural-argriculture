import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
from PIL import Image

# Define a custom dataset class that extracts labels from filenames
class PlantDiseaseDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = os.listdir(root_dir)

    def __len__(self):
        return sum([len(files) for r, d, files in os.walk(self.root_dir)])

    def __getitem__(self, idx):
        for i, cls in enumerate(self.classes):
            class_path = os.path.join(self.root_dir, cls)
            for file in os.listdir(class_path):
                if idx == 0:
                    image_path = os.path.join(class_path, file)
                    image = Image.open(image_path).convert('RGB')
                    if self.transform:
                        image = self.transform(image)
                    return image, i  # Map label based on class index
                else:
                    idx -= 1