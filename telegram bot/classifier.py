# -*- coding: utf-8 -*-
"""
Created on Mon Nov 01 16:10:02 2019

@author: vkovalev
"""
import torch
import torchvision
from PIL import Image


def classify_image(image_name):
    # Load the best saved model.
    device = torch.device("cpu")
    with open('top_model.mdl', 'rb') as f:
        model = torch.load(f, map_location = torch.device('cpu'))
    model.eval()
    idx_to_class = {0 : 'Impressionism', 1 : 'Realism', \
                2 : 'Romanticism', 3 : 'Expressionism', \
                4: 'Post-Impressionism'}
    test_image = Image.open('tmp\\'+image_name)
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(size=256),
        torchvision.transforms.CenterCrop(size=224),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    
    image_tensor = transform(test_image)
    image_tensor = image_tensor.view(1, 3, 224, 224)
     
    with torch.no_grad():
        model.eval()
        out = model(image_tensor)
        print('out:', out)
        ps = torch.softmax(out, dim = 1)
        print('ps:', ps)
        print(torch.sum(ps, dim = 1))
        #res = {'Impressionism' : ps[0][0].numpy(),
        #        'Realism' : ps[0][1].numpy(),
        #        'Romanticism' : ps[0][2].numpy(),
        #        'Expressionism' : ps[0][3].numpy(),
        #        'Post-Impressionism' : ps[0][4].numpy()}
        topk, topclass = ps.topk(1, dim=1)
        #print(res)
        print('topclass', topclass)
        print("Output class :  ", idx_to_class[topclass.cpu().numpy()[0][0]])
    return idx_to_class[topclass.cpu().numpy()[0][0]]