import sys
import torch
import sys
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
from torchvision import transforms, datasets
import time
import numpy as np

sys.path.append('../')
sys.path.append('./disease_model')


from dataset import PlantDiseaseDataset
import model
from model import tiny_cnn
import mongoAPI

if __name__ == '__main__':
    try:
        mongoAPI.connect("World", "Plant_Images")
        documents = mongoAPI.getNewImages()

        network = tiny_cnn()

        weights = torch.load('./disease_model/tinycnn.pth')

        # Load the state_dict into the model
        network.load_state_dict(weights)

        network.eval()

        for doc in documents:
            start_time = time.time()
            image = doc['image_data']
            image = np.array(image)

            # Reshape the NumPy array to the desired shape
            image = torch.tensor(image).view(1, 3, 224, 224).float()

            # Perform inference on the sample batch and measure the time
            with torch.no_grad():
                output = network(image)
                end_time = time.time()

                inference_time = end_time - start_time
                print(inference_time)

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        mongoAPI.disconnect()