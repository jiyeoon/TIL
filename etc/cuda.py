import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np

class Img2Vec_CUDA():
    
    def __init__(self, cuda=False, model='resnet-18', layer='default', layer_output_size=512):
        """
        """
        self.device = torch.device('cuda' if cuda else 'cpu')
        self.layer_output_size = layer_output_size
        self.model_name = model
        
        self.model, self.extraction_layer = self._get_model_and_layer(model, layer)
        
        cudacnt = torch.cuda.device_count()
        
        """
        if cudacnt > 1:
            print("use", torch.cuda.device_count(), "GPUS!")
            self.model = nn.DataParallel(self.model)
        """
        
        self.model = self.model.to(self.device)
        
        self.model.eval()
        
        self.scaler = transforms.Scale((224, 224))
        self.normalize = transforms.Normalize(mean=[0.0485, 0.0456, 0.406],
                                              std=[0.229, 0.224, 0.225])
        self.to_tensor = transforms.ToTensor()
        
    def get_veclist_cuda(self, list, tensor=False):
        if self.model_name == 'alexnet':
            my_embedding = torch.zeros(len(list), self.layer_output_size)
        else:
            my_embedding = torch.zeros(len(list), self.layer_output_size, 1, 1)
        
        def copy_data(m, i, o):
            my_embedding.copy_(o.data)
        
        h = self.extraction_layer.register_forward_hook(copy_data)
        h_x = self.model(list)
        h.remove()
        
        if tensor:
            return my_embedding
        else:
            if self.model_name == 'alexnet':
                return my_embedding.numpy()[:, :]
            else:
                print(my_embedding.numpy()[:, :, 0, 0].shape)
                return my_embedding.numpy()[:, :, 0, 0]