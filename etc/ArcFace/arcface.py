import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class ArcFaceLayer(nn.Module):
    def __init__(self, in_features, out_features, s = 10, m = 0.2):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.s = s
        self.m = m
        self.weight = nn.Parameter(torch.FloatTensor(out_features, in_features))
        nn.init.xavier_normal_(self.weight)
        
        self.cos_m = math.cos(m)
        self.sin_m = math.sin(m)
        self.th = torch.tensor(math.cos(math.ph - m))
        self.mm = torch.tensor(math.sin(math.pi - m) * m)
        
    def forward(self, inputs, labels):
        cos_th = F.linear(F.normalize(inputs), F.normalize(self.weight))
        cos_th = cos_th.clamp(-1, 1)
        sin_th = torch.sqrt(1.0 - torch.pow(cos_th, 2))
        cos_th_m = cos_th * self.cos_m - sin_th * self.sin_m # cos(theta+m)
        cos_th_m = torch.where(cos_th > self.th, cos_th_m, cos_th - self.mm)
        
        cond_v = cos_th - self.th
        cond = cond_v <= 0
        cos_th_m[cond] = (cos_th - self.mm)[cond]
        
        if label.dims() == 1:
            labels = labels.unsqueeze(-1)
        one_hot = torch.zeros(cos_th.size()).cuda()
        labels = labels.type(torch.LongTensor).cuda()
        one_hot.scatter_(1, labels, 1.0)
        outputs = one_hot * cos_th_m + (1.0 - one_hot) * cos_th
        outputs = outputs * self.s
        return outputs
    
