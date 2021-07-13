import timm
import os
import torch
import numpy as np
from PIL import Image


class Img2Vec():
    def __init__(self, cuda=False):
        self.device = torch.device('cuda' if cuda else 'cpu')
        self.model = self._get_model()
        self.config = self.model.default_cfg
        self.img_size = self.config['test_input_size'][-1] if 'test_input_size' in config else config['input_size'][-1]
        self.transform = self._get_transform()
    
    
    def get_vec(self, img): # img : PIL type
        input_tensor = self.transform(img).unsqueeze(0)
        #input_numpy = input_tensor.numpy()
        with torch.no_grad():
            output_vec = self.model(input_tensor)
            output_vec_np = output_vec.numpy()
        return output_vec_np
    
    
    def get_vec_bulk(self, img_list): # img_list : PIL image list
        input_tensor_list = [self.transform(img).unsqueeze(0) for img in img_list]
        #input_numpy_list = [input_tensor.numpy() for input_tensor in input_tensor_list]
        output_vec_list = []
        for input_tensor in input_tensor_list:
            with torch.no_grad():
                output_vec = self.model(input_tensor)
                output_vec_np = output_vec.numpy()
                output_vec_list.append(output_vec_np)
        return output_vec_list
    
    
    def _get_model(self):
        return timm.create_model('eca_nfnet_l0', pretrained=True).to(self.device)


    def _get_transform(self):
        return timm.data.transforms_factory.transforms_imagenet_eval(
            img_size = self.img_size,
            interpolation = self.config['interpolation'],
            mean = self.config['mean'],
            std = self.config['std'],
            crop_pct = self.config['crop_pct']
        )
        


'''
사용법
from PIL import Image

img_path = 'IMG_PATH'
img = Image.open(img_path)

img2vec = Img2Vec()
output_vector = img2vec.get_vec(img)
'''