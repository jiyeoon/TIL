import cv2
import timm
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from  .arcface import ArcFaceLayer

"""
eca_nf_net10 : https://huggingface.co/timm/eca_nfnet_l0
"""

class NFNetModel(nn.Module):
    def __init__(self, channel_size, out_features, dropout=0.5, backbone='resnet'):
        super(NFNetModel, self).__init__()
        self.base_model = timm.create_model("hf_hub:timm/eca_nfnet_10")
        self.channel_size = channel_size
        self.out_features = out_features
        self.in_features = self.base_model.classifier.in_features
        self.arcface = ArcFaceLayer(in_features=self.channel_size, out_features=self.out_features)
        self.bn1 = nn.BatchNorm2d(self.in_features)
        self.dropout = nn.Dropout2d(dropout, inplace=True)
        self.gap = nn.AvgPool2d(kernel_size=3)
        self.norm = nn.LayerNorm() # todo
        
    
    def forward(self, x, labels=None):
        model = nn.Sequential(
            self.base_model,
            self.gap,
            self.bn1,
            self.norm,
            self.margin
        )
        return model