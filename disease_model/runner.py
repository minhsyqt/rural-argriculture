import torch
import sys
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
from torchvision import transforms, datasets
import time

sys.path.append('./')

from dataset import PlantDiseaseDataset
import model
from model import tiny_cnn

NUM_CLASSES = 3
NUM_EPOCHS  = 5

# Define data transforms and load your dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

batch_size = 32
train_data = PlantDiseaseDataset('/Users/minhtruong/Documents/GitHub/rural-argriculture/data/plant_images', transform=transform)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# Initialize the model and set up loss and optimizer
network = tiny_cnn()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(network.parameters(), lr=0.001)

for epoch in range(NUM_EPOCHS):
    running_loss = 0.0
    correct = 0
    total = 0

    for i, data in enumerate(train_loader, 0):
        inputs, labels = data

        optimizer.zero_grad()

        outputs = network(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        if i % 10 == 9:  # Print and evaluate every 10 mini-batches
            train_accuracy = 100 * correct / total
            print(f'Epoch {epoch + 1}, Batch {i + 1}, Loss: {running_loss / 10:.4f}, Training Accuracy: {train_accuracy:.2f}%')
            running_loss = 0.0
            correct = 0
            total = 0

print("Training finished")

sample_data = torch.randn((batch_size, 3, 224, 224))

# Set the model to evaluation mode
network.eval()

# Perform inference on the sample batch and measure the time
with torch.no_grad():
    start_time = time.time()
    output = network(sample_data)
    end_time = time.time()

inference_time = end_time - start_time
print(f'Inference time for a batch of {batch_size} images: {inference_time:.4f} seconds')

# Save the trained network
torch.save(network.state_dict(), 'tinycnn.pth')
