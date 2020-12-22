# -*- coding: utf-8 -*-
"""Autoencoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/187qi7PgWQVFmHUDGh64jtmlhiGNdQPY8

dharamvir yadav(MT19CPS012)
autoencoder
"""

import os
import torch 
import torchvision
import torch.nn as nn
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn.functional as F
 
from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision.utils import save_image

NUM_EPOCHS = 100
LEARNING_RATE = 1e-3
BATCH_SIZE = 128
# image transformations
transform = transforms.Compose([
    transforms.ToTensor(),
])

image, label = datasets.MNIST[0]
print('image.shape:', image.shape)
plt.imshow(image.permute(1, 2, 0), cmap='gray')
print('Label:', label)

trainset = datasets.MNIST(
    root='./data',
    train=True, 
    download=True,
    transform=transform
)
testset = datasets.MNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)
trainloader = DataLoader(
    trainset, 
    batch_size=BATCH_SIZE,
    shuffle=True
)
testloader = DataLoader(
    testset, 
    batch_size=BATCH_SIZE, 
    shuffle=True
)

def get_device():
    if torch.cuda.is_available():
        device = 'cuda:0'
    else:
        device = 'cpu'
    return device
def make_dir():
    image_dir = 'MNIST_Images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
def save_decoded_image(img, epoch):
    img = img.view(img.size(0), 1, 28, 28)
    save_image(img, './MNIST_Images/linear_ae_image{}.png'.format(epoch))



class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        # encoder
        self.enc1 = nn.Linear(in_features=784, out_features=256)
        self.enc2 = nn.Linear(in_features=256, out_features=128)
        self.enc3 = nn.Linear(in_features=128, out_features=64)
        
        # decoder 
        
        self.dec3 = nn.Linear(in_features=64, out_features=128)
        self.dec4 = nn.Linear(in_features=128, out_features=256)
        self.dec5 = nn.Linear(in_features=256, out_features=784)
    def forward(self, x):
        x = F.relu(self.enc1(x))
        x = F.relu(self.enc2(x))
        x = F.relu(self.enc3(x))
        print(x)
        
        x = F.relu(self.dec3(x))
        x = F.relu(self.dec4(x))
        x = self.dec5(x)
        return x
net = Autoencoder()
print(net)

criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=1e-5)

train_loss = []
test_loss = []

def train(net, trainloader,testloader, NUM_EPOCHS):
    
    for epoch in range(NUM_EPOCHS):
        running_loss = 0.0
        for data in trainloader:
            
            img, _ = data
            img = img.to(device)
            img = img.view(img.size(0), -1)
            
            optimizer.zero_grad()
            outputs = net(img)
            loss = criterion(outputs, img)

            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        loss = running_loss / len(trainloader)
        train_loss.append(loss)
        
        running_loss1 = 0.0
        for data in testloader:
            
            img, _ = data
            img = img.to(device)
            img = img.view(img.size(0), -1)
            
            optimizer.zero_grad()
            outputs = net(img)
            loss1 = criterion(outputs, img)
            loss1.backward()
            optimizer.step()
            running_loss1 += loss1.item()
        
        loss1 = running_loss1 / len(trainloader)
        test_loss.append(loss1)
        print('Epoch {} of {}, Train Loss: {:.3f}, Test Loss: {:.3f}'.format(
            epoch+1, NUM_EPOCHS, loss, loss1))
        if epoch % 1 == 0:
            save_decoded_image(outputs.cpu().data, epoch)
    return train_loss, test_loss
    
            
def test_image_reconstruction(net, testloader):
     for batch in testloader:
        img, _ = batch
        img = img.to(device)
        img = img.view(img.size(0), -1)
        outputs = net(img)
        outputs = outputs.view(outputs.size(0), 1, 28, 28).cpu().data
        save_image(outputs, 'mnist_reconstruction.png')
        break

import numpy as np

# get the computation device
device = get_device()
print(device)
# load the neural network onto the device
net.to(device)
make_dir()
# train the network
train_loss, test_loss = train(net, trainloader,testloader, NUM_EPOCHS)

plt.figure()
#plt.plot(train_loss)
x = np.arange(len(train_loss))
plt.plot(x, train_loss,'r-')
plt.plot(x, test_loss,'b-')
plt.title('Train Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.savefig('deep_ae_fashionmnist_loss.png')

for data in testloader:

            
    img, _ = data
    #img = img.to(device)
    img = img.view(img.size(0), -1)

x = img

enc1 = nn.Linear(in_features=784, out_features=256)
enc2 = nn.Linear(in_features=256, out_features=128)
enc3 = nn.Linear(in_features=128, out_features=64)
        
        
    
x = F.relu(enc1(x))
x = F.relu(enc2(x))
x = F.relu(enc3(x))
print(x.shape)

