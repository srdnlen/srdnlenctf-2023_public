# srdnlenctf 2023

## Improvise Adapt Overcome (X solves)

In this challenge you need to implement and adaptive attack against two ML models (a MNIST classifier and a detector).

### Solution

We have a classifier trained to recognize digits from MNIST dataset. Then we also have a detector to check if the submitted sample contains a perturbation to evade the classifier. In order to solve the challenge you have to submit an adversarial sample but to not raise an alert in the adversarial detector.

In the following the exploitation code.

### Exploit

```python
#!/bin/env python3

# Credits to rmura498 for the exploit code

import base64
import urllib.parse
import io
from io import BytesIO
from PIL import Image
import json
import torch
from torchvision.transforms import transforms
from torchvision.utils import save_image
import cv2


def image_base64_to_tensor(base64_image):
    image_bytes = base64.b64decode(base64_image)
    image_stream = BytesIO(image_bytes)
    image = Image.open(image_stream)
    image.save("output.png", "PNG")
    # transform to tensor
    transform = transforms.Compose([
        transforms.Resize((28, 28)),  # Resize the image to 28x28
        transforms.ToTensor()  # Convert the PIL Image to a PyTorch tensor
    ])

    image_tensor = transform(image)

    return image_tensor


def base64_to_tensor(input):
    bytes = base64.b64decode(input)
    tensor = torch.tensor(json.loads(bytes.decode()))
    return tensor


def tensor_to_base64(image_tensor):
    # Ensure that the tensor is on the CPU and in the correct data type
    image_tensor = image_tensor.cpu().detach()

    # Convert the tensor to a PIL Image
    image_pil = transforms.ToPILImage()(image_tensor)

    # Convert the PIL Image to bytes
    with io.BytesIO() as images:
        image_pil.save(images, format="PNG")
        image_bytes = images.getvalue()

    base64_encoded = base64.b64encode(image_bytes).decode()
    return base64_encoded


def get_sample_image():
    url = 'https://adapt.challs.srdnlen.it/sample_image'
    headers = {
        'accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response content
            return response.text
        else:
            # Print an error message if the request was not successful
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Request failed with error: {e}")


import requests


def post_request(url):
    headers = {
        'accept': 'application/json',
    }

    data = ''  # Leave this empty if there's no data to send in the request body

    try:
        response = requests.post(url, headers=headers, data=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response content
            return response.text
        else:
            # Print an error message if the request was not successful
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Request failed with error: {e}")


# retrieve the image
response_data = get_sample_image()
response_data = json.loads(response_data)
base64_image = response_data["image"]
image_tensor = image_base64_to_tensor(base64_image)

sample, label = image_tensor, 5
target_label = torch.LongTensor([0])
print(f'Original label: {label}')
iterations = 100
eps = 0.3
loss = torch.nn.CrossEntropyLoss()
step_size = 0.05

x_adv = sample.clone()

for i in range(iterations):
    print(i)

    base64_adv = tensor_to_base64(x_adv)
    url_encoded_string = urllib.parse.quote_plus(base64_adv)

    url = f'https://adapt.challs.srdnlen.it/grad_classifier?perturbation={url_encoded_string}'
    response_data = post_request(url)
    response_data = json.loads(response_data)
    scores = base64_to_tensor(response_data["scores"])
    gradient = base64_to_tensor(response_data["gradient"])

    url = f'https://adapt.challs.srdnlen.it/grad_detector?perturbation={url_encoded_string}'
    response_data = post_request(url)
    response_data = json.loads(response_data)
    det_scores = base64_to_tensor(response_data["scores"])
    det_gradient = base64_to_tensor(response_data["gradient"])

    adv_grad = gradient + det_gradient
    adv_grad = adv_grad.sign()

    x_adv.data = x_adv.data + step_size * adv_grad
    x_adv.data = torch.clamp(x_adv, 0, 1)

    if torch.norm(x_adv - sample, p=torch.inf) > eps:
        delta = x_adv - sample
        delta = delta.clamp(-eps, eps)
        x_adv = sample.data + eps*delta.data


print(f'Adv label: {scores.argmax(dim=-1)}')
print(f'Adv label: {det_scores.argmax(dim=-1)}')
delta = x_adv - sample
print(delta.abs().max())
save_image(delta, 'del.png')
image = cv2.imread('del.png', cv2.IMREAD_GRAYSCALE)
cv2.imwrite('del.png', image)

img_file = open('del.png', 'rb').read()
url_encoded_string = urllib.parse.quote_plus(base64.b64encode(img_file).decode())

url = f'https://adapt.challs.srdnlen.it/query?perturbation={url_encoded_string}'
response_data = post_request(url)
print(response_data)


```
