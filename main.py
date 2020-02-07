'''
This code will be used as the main code to run all classes
'''

# Imports
import torch
from Adjustable_LeNet import AdjLeNet
from MNIST_Setup import MNIST_Data
from Gym import Gym
from One_Step_Spectral_Attack import OSSA
import torchvision.transforms.functional as F
import matplotlib.pyplot as plt
import operator

'''
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "5"
'''

# Initialize
net = AdjLeNet(num_classes = 10,
               num_kernels_layer1 = 6, 
               num_kernels_layer2 = 16, 
               num_kernels_layer3 = 120,
               num_nodes_fc_layer = 84)
data = MNIST_Data()
detministic_model = Gym(net = net, data = data)

# Fit Model
accuracy = detministic_model.train(n_epochs = 10)
print("Deterministic Model Accuracy: ", accuracy)

# Generate an Attack using OSSA
image, label, show_image = data.get_single_image()
print("Image Label: ", label.item())

attack = OSSA(net, image, label)

# Test Attack
prediction = detministic_model.get_single_prediction(image)
print("Deterministic Model Prediction: ", prediction.item())

attack_prediction = detministic_model.get_single_prediction(image - attack.attack_perturbation)
print("Deterministic Model Attack Prediction: ", attack_prediction.item())

'''
# Display
rows = 1
cols = 3
figsize = [8, 4]
fig= plt.figure(figsize=figsize)
fig.suptitle('OSSA Attack Summary', fontsize=16)

ax1 = fig.add_subplot(rows, cols, 1)
ax1.imshow(show_image)
ax1.set_title("Orginal Image")

ax2 = fig.add_subplot(rows, cols, 2)
ax2.imshow(-attack.attack_perturbation)
ax2.set_title("Attack Perturbation")

ax3 = fig.add_subplot(rows, cols, 3)
ax3.imshow(show_image - attack.attack_perturbation)
ax3.set_title("Attack")

plt.show()
'''