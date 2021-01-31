import os
import torch
from torchvision import transforms
from PIL import Image
import numpy as np 
from django.conf import settings

model_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),
    'py_templates/classifier.pth')
model=torch.load(model_path, map_location=lambda storage, loc: storage)

image_path=settings.MEDIA_URL

#transforms
transform=transforms.Compose([transforms.Resize(256),
                                  transforms.CenterCrop(224),
                                  transforms.ToTensor(),
                                  transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
#create a function that predict labels
def image_pred(url):
    try:
        new_url=image_path+url
    except TypeError:
        new_url=url

    img = Image.open(new_url)
    img=img.convert(mode='RGB')
    img = transform(img)
    img=img.unsqueeze(0).cpu() #add another dimension at 0
    model.eval()
    ps=torch.exp(model(img))
    top_p,top_class=ps.topk(1,dim=1)
    top_p=top_p.squeeze(0).detach().numpy().tolist()[0]
    top_class=top_class.squeeze(0).detach().numpy().tolist()[0]
    return top_p,top_class

