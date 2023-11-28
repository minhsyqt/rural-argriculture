import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from collections import OrderedDict

class tiny_cnn(nn.Module):
    def __init__(self):
        super(tiny_cnn,self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3,
                               out_channels=6,
                               kernel_size=3,
                               stride=1,
                               padding=0,
                               bias=True)

        self.pool = nn.MaxPool2d(kernel_size=3,
                                 stride=3)

        self.conv2 = nn.Conv2d(in_channels=6,
                               out_channels=12,
                               kernel_size=6,
                               stride=3,
                               padding=0,
                               bias=True)

        self.fc1 = nn.Linear(in_features=588,
                             out_features=100)

        self.fc2 = nn.Linear(in_features=100,
                             out_features=50)

        self.fc3 = nn.Linear(in_features=50,
                             out_features=10)

        self.fc4 = nn.Linear(in_features=10,
                             out_features=3)

        self.sm = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.shape[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        x = self.sm(x)
        return x

def resnet18(transfer=True):
    model = torchvision.models.resnet18(pretrained=transfer)

    # Freeze the model if transfer learning
    if (transfer):
        for param in model.parameters():
            param.require_grad = False;

    # Remake the final layer
    fc = nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(in_features=512, out_features=100)),
        ('relu1', nn.ReLU()),
        ('fc2', nn.Linear(in_features=100, out_features=10)),
        ('relu2', nn.ReLU()),
        ('fc3', nn.Linear(in_features=10, out_features=3)),
        ('output', nn.Softmax(dim=1))
    ]))

    model.fc = fc
    return model

def mobilenet(transfer=True):
    model = torchvision.models.mobilenet_v2(pretrained=transfer)

    # Freeze the model if transfer learning
    if (transfer):
        for param in model.parameters():
            param.require_grad = False;

    # Remake the final layer
    fc = nn.Sequential(OrderedDict([
        ('do', nn.Dropout(p=0.2, inplace=False)),
        ('fc1', nn.Linear(in_features=1280, out_features=100)),
        ('relu1', nn.ReLU()),
        ('fc2', nn.Linear(in_features=100, out_features=10)),
        ('relu2', nn.ReLU()),
        ('fc3', nn.Linear(in_features=10, out_features=3)),
        ('output', nn.Softmax(dim=1))
    ]))

    model.classifier = fc
    return model