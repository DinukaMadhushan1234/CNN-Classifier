import numpy as np
import torch
import torch.nn as nn
from torchvision import datasets
from torchvision import transforms
from torch.utils.data.sampler import SubsetRandomSampler

import os

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# #Old Dataloaders
# def get_train_valid_loader(data_dir,
#                                batch_size,
#                                augment,
#                                random_seed,
#                                valid_size=0.1,
#                                shuffle=True):
#     normalize = transforms.Normalize(
#         mean=[0.4914, 0.4822, 0.4465],
#         std=[0.2023, 0.1994, 0.2010],
#     )

#     # define transforms
#     valid_transform = transforms.Compose([
#             transforms.Resize((227,227)),
#             transforms.ToTensor(),
#             normalize,
#     ])
#     if augment:
#         train_transform = transforms.Compose([
#             transforms.RandomCrop(32, padding=4),
#             transforms.RandomHorizontalFlip(),
#             transforms.ToTensor(),
#             normalize,
#         ])
#     else:
#         train_transform = transforms.Compose([
#             transforms.Resize((227,227)),
#             transforms.ToTensor(),
#             normalize,
#             ])

#         # load the dataset
#         train_dataset = datasets.CIFAR10(
#             root=data_dir, train=True,
#             download=True, transform=train_transform,
#         )

#         valid_dataset = datasets.CIFAR10(
#             root=data_dir, train=True,
#             download=True, transform=valid_transform,
#         )

#         num_train = len(train_dataset)
#         indices = list(range(num_train))
#         split = int(np.floor(valid_size * num_train))

#     if shuffle:
#         np.random.seed(random_seed)
#         np.random.shuffle(indices)

#     train_idx, valid_idx = indices[split:], indices[:split]
#     train_sampler = SubsetRandomSampler(train_idx)
#     valid_sampler = SubsetRandomSampler(valid_idx)

#     train_loader = torch.utils.data.DataLoader(
#     train_dataset, batch_size=batch_size, sampler=train_sampler)

#     valid_loader = torch.utils.data.DataLoader(
#     valid_dataset, batch_size=batch_size, sampler=valid_sampler)

#     return (train_loader, valid_loader)

# def get_test_loader(data_dir,
#                         batch_size,
#                         shuffle=True):
#     normalize = transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225],
#     )

#     # define transform
#     transform = transforms.Compose([
#         transforms.Resize((227,227)),
#         transforms.ToTensor(),
#         normalize,
#     ])

#     dataset = datasets.CIFAR10(
#         root=data_dir, train=False,
#         download=True, transform=transform,
#     )

#     data_loader = torch.utils.data.DataLoader(
#         dataset, batch_size=batch_size, shuffle=shuffle
#         )

#     return data_loader

#     # CIFAR10 dataset 
#     # CIFAR10 dataset 

# train_loader, valid_loader = get_train_valid_loader(
#         data_dir='./data',
#         batch_size=64,
#         augment=False,
#         random_seed=1
#     )
# print(train_loader)
# print(valid_loader)

# test_loader = get_test_loader(
#         data_dir='./data',
#         batch_size=64
#     )

#New Dataloaders
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}
#Hi
data_dir = "/workspace/pattern/main/data/Jute_Pest_Dataset"
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                             shuffle=True, num_workers=4)
              for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

train_loader = dataloaders['train']
valid_loader = dataloaders['val']




# class AlexNet(nn.Module):
#         def __init__(self, num_classes=17):
#             super(AlexNet, self).__init__()
#             self.layer1 = nn.Sequential(
#                 nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=0),
#                 nn.BatchNorm2d(96),
#                 nn.ReLU(),
#                 nn.MaxPool2d(kernel_size = 3, stride = 2))
#             self.layer2 = nn.Sequential(
#                 nn.Conv2d(96, 256, kernel_size=5, stride=1, padding=2),
#                 nn.BatchNorm2d(256),
#                 nn.ReLU(),
#                 nn.MaxPool2d(kernel_size = 3, stride = 2))
#             self.layer3 = nn.Sequential(
#                 nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=1),
#                 nn.BatchNorm2d(384),
#                 nn.ReLU())
#             self.layer4 = nn.Sequential(
#                 nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1),
#                 nn.BatchNorm2d(384),
#                 nn.ReLU())
#             self.layer5 = nn.Sequential(
#                 nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
#                 nn.BatchNorm2d(256),
#                 nn.ReLU(),
#                 nn.MaxPool2d(kernel_size = 3, stride = 2))
#             self.fc = nn.Sequential(
#                 nn.Dropout(0.5),
#                 #nn.Linear(9216, 4096),
#                 nn.Linear(6400, 4096),
#                 nn.ReLU())
#             self.fc1 = nn.Sequential(
#                 nn.Dropout(0.5),
#                 nn.Linear(4096, 4096),
#                 nn.ReLU())
#             self.fc2= nn.Sequential(
#                 nn.Linear(4096, num_classes))

#         def forward(self, x):
#             out = self.layer1(x)
#             out = self.layer2(out)
#             out = self.layer3(out)
#             out = self.layer4(out)
#             out = self.layer5(out)
#             #print("After Conv shape:", out.shape)
#             out = out.reshape(out.size(0), -1)
#             #out = torch.flatten(out, start_dim=1)
#             #print("After layer2 shape:", out.shape)
#             out = self.fc(out)
#             out = self.fc1(out)
#             out = self.fc2(out)
#             return out

class AlexNet(nn.Module):
        def __init__(self, num_classes=17):
            super(AlexNet, self).__init__()
            self.layer1 = nn.Sequential(
                nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=0),
                nn.BatchNorm2d(96),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size = 3, stride = 2))
            self.layer2 = nn.Sequential(
                nn.Conv2d(96, 256, kernel_size=5, stride=1, padding=2),
                nn.BatchNorm2d(256),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size = 3, stride = 2))
            # self.layer3 = nn.Sequential(
            #     nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=1),
            #     nn.BatchNorm2d(384),
            #     nn.ReLU())
            # self.layer4 = nn.Sequential(
            #     nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1),
            #     nn.BatchNorm2d(384),
            #     nn.ReLU())
            # self.layer5 = nn.Sequential(
            #     nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            #     nn.BatchNorm2d(256),
            #     nn.ReLU(),
            #     nn.MaxPool2d(kernel_size = 3, stride = 2))
            self.fc = nn.Sequential(
                #nn.Dropout(0.5),
                #nn.Linear(9216, 4096),
                nn.Linear(6400, 4096),
                nn.ReLU())
            self.fc1 = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(4096, num_classes),
                nn.Softmax())
            # self.fc2= nn.Sequential(
            #     nn.Linear(4096, num_classes))

        def forward(self, x):
            out = self.layer1(x)
            out = self.layer2(out)
            print("After Conv shape:", out.shape)
            #out = self.layer3(out)
           #out = self.layer4(out)
            #out = self.layer5(out)
            print("After Conv shape:", out.shape)
            out = out.reshape(out.size(0), -1)
            #print("After layer2 shape:", out.shape)
            out = self.fc(out)
            out = self.fc1(out)
            #out = self.fc2(out)
            return out
        


num_classes = 17
num_epochs = 20
batch_size = 64
learning_rate = 0.005

model = AlexNet(num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, weight_decay=0.005, momentum=0.9)  



# Train the model
total_step = len(train_loader)




if __name__ == '__main__':
    for epoch in range(num_epochs):
       # print("Shit is trainging")
        for i, (images, labels) in enumerate(train_loader):  
            # Move tensors to the configured device
            images = images.to(device)
            labels = labels.to(device)
            #print(labels)
            #print("Data loded")
            
            # Forward pass
            outputs = model(images)
            #print(outputs)
            loss = criterion(outputs, labels)
            #print("Forward Pass")
        
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
        
        # Validation
        with torch.no_grad():
            correct = 0
            total = 0
            for images, labels in valid_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                del images, labels, outputs
        
        print('Accuracy of the network on the {} validation images: {} %'.format(5000, 100 * correct / total))

if __name__ == '__main__':
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in valid_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            del images, labels, outputs

        print('Accuracy of the network on the {} test images: {} %'.format(10000, 100 * correct / total))