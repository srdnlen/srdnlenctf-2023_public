from typing import Union
from fastapi import FastAPI

import base64

# ML imports
from torch import nn
import torch
from torchvision import datasets, transforms
from PIL import Image
from io import BytesIO

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = torch.relu(torch.max_pool2d(self.conv1(x), 2))
        x = torch.relu(torch.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
    
class DetectorNet(nn.Module):

    def __init__(self):
        super(DetectorNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 2)

    def forward(self, x):
        x = torch.relu(torch.max_pool2d(self.conv1(x), 2))
        x = torch.relu(torch.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

net = Net()    
detector_net = DetectorNet()

net.load_state_dict(torch.load('model.pth'))
detector_net.load_state_dict(torch.load('detector.pth'))

net.eval()
detector_net.eval()

transform = transforms.ToTensor()
mnist = datasets.MNIST(root='.', download=True, train=True)
sample_raw = mnist[0]
mnist = datasets.MNIST(root='.', download=True, train=True, transform=transform)
sample, label = mnist[0]
x = sample
label = torch.tensor(label).unsqueeze(0)

app = FastAPI()

@app.get("/")
def index():
    return {"Description": "This is an ML Security Challenge"}

@app.get("/sample_image")
def sample_image():
    """
    Get the sample image to use for your attack
    """
    buffered = BytesIO()
    sample_raw[0].save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())
    return {"image": img_str.decode()}

@app.post("/query")
def query_model(perturbation: Union[str, None] = None):
    """
    Send your adversarial sample (ONLY the perturbation delta as a base64 encoded image).
    Your goal is to craft an adversarial sample that is misclassified by the model and not detected as an adversarial sample.
    """
    submitted = base64.b64decode(perturbation)
    submitted_im = Image.open(BytesIO(submitted))
    convert_tensor = transforms.ToTensor()
    delta = convert_tensor(submitted_im)
    if (not (delta.abs().max() <= 0.3)):
        return {"Error":"Delta should be less than 0.3"}
    if (delta.min() < 0 or delta.max() > 1):
        return {"Error": "Delta should only contain pixels values between 0 and 1"}

    attack_detection = detector_net(x+delta).argmax(1)
    if attack_detection == 1:
        return {"Error":"Your sample was detected as an adversarial, try again!"}

    detection = net(x+delta).argmax(1)
    if detection == label:
        return {"Success":"Your sample was correctly classified as a 5"}
    else:
        return {"Flag": "srdnlen{adaptive_attacks_are_easy}"}
    
@app.post("/grad_classifier")
def query_gradient(perturbation: Union[str, None] = None):
    """
    Send your base64 encoded image (of the WHOLE adversarial sample) to get the gradient and scores of the classifier
    """
    loss = torch.nn.CrossEntropyLoss()
    submitted = base64.b64decode(perturbation)
    submitted_im = Image.open(BytesIO(submitted))
    convert_tensor = transforms.ToTensor()
    delta = convert_tensor(submitted_im)
    sample = delta
    sample = sample.clone()
    sample.requires_grad =True
    scores = [net(sample), detector_net(sample)]
    output = loss(scores[0], label) + 0.5 * loss(scores[1], torch.tensor(1).unsqueeze(0))
    output.backward()
    gradient = sample.grad
    return {"gradient":base64.b64encode(str(gradient.tolist()).encode()).decode(), "scores": base64.b64encode(str(scores[0].tolist()).encode()).decode()}

@app.post("/grad_detector")
def query_gradient(perturbation: Union[str, None] = None):
    """
    Send your base64 encoded image (of the WHOLE adversarial sample) to get the gradient and scores of the adversarial detector
    """
    loss = torch.nn.CrossEntropyLoss()
    submitted = base64.b64decode(perturbation)
    submitted_im = Image.open(BytesIO(submitted))
    convert_tensor = transforms.ToTensor()
    delta = convert_tensor(submitted_im)
    sample = delta
    sample = sample.clone()
    sample.requires_grad_()
    scores = [net(sample), detector_net(sample)]
    output = loss(scores[0], label) + 0.5 * loss(scores[1], torch.tensor(1).unsqueeze(0))
    output.backward()
    gradient = sample.grad
    gradient = gradient.sign()
    return {"gradient":base64.b64encode(str(gradient.tolist()).encode()).decode(), "scores": base64.b64encode(str(scores[1].tolist()).encode()).decode('utf-8')}


