
# Addictive Angular Margin Loss (=ArcFace)

ArcFace는 얼굴 인식(FR, Face Recognition)에서 사용되는 손실함수입니다. 소프트맥스가 전통적으로 많이 사용되지만 소프트맥스의 손실함수는 클래스 내 샘플에 대해 더 높은 유사성을 적용하고 클래스 간 샘플에 대해 다양성을 강화하기위해 피처 임베딩을 명시적으로 최적화하지는 않습니다. 이로 인해 대규모 클래스 내 외모 변화에서 깊은 얼굴인식에 대한 성능 차이가 발생합니다.


ArcFace 손실함수는 로짓을 변경하는데 $W^T_j x_i = ||W_j|| \cdot ||x_i|| \cos{\theta_j}$이며 $\cos{\theta_j}$는 weight $W_j$와 피처 $x_i$ 사이의 각도이다. 개별 가중치 $||W_j||=1$은 L2 normalization에 의해 고정됩니다. 임베딩 피처 $||x_i||$는 L2 normalization에 의해 고정되고 $s$ 로 re-scale 됩니다. weight와 feature에 정규화를 하는 것은 예측이 가중치 사이의 각도에만 의존하도록 합니다. 따라서 학습된 임베딩 피처들은 반경이 $s$인 하이퍼스피어에 분산시킨다. 마지막으로 $x_i$와 $W_{y_i}$사이의 추가 각도 마진 패널티 m이 추가되어 클래스 내 간결함과 클래스간 불일치를 동시에 향상시킵니다. 제안된 추가 각도 여백 패널티는 정규화된 하이퍼 스피어의 여백 패널티와 같으므로 이 방법의 이름은 ArcFace입니다. (??)

$$ L_{3} = -\frac{1}{N}\sum^{N}_{i=1}\log\frac{e^{s\left(\cos\left(\theta_{y_{i}} + m\right)\right)}}{e^{s\left(\cos\left(\theta_{y_{i}} + m\right)\right)} + \sum^{n}_{j=1, j \neq y_{i}}e^{s\cos\theta_{j}}}
 $$

![img](https://paperswithcode.com/media/methods/Screen_Shot_2020-08-04_at_2.17.31_PM_bCJokL9.png)

위 사진은 2D피처를 가진 데이터를 각각 sofrmax와 arcface로 시각화한 모습닙니다. 그림이 보여주듯이, 소프트맥스 함수는 대략적으로 분리 가능한 기능 임베딩을 제공하지만 결정 경계에서 모호성을 보여주는 반면 ArcFace는 가장 가까운 클래스 사이에서도 확실한 margin이 있는 것을 확인할 수 있습니다.

## ArcFace 예시 코드

```python
class ArcMarginProduct(nn.Module):
    r"""Implement of large margin arc distance: :
        Args:
            in_features: size of each input sample
            out_features: size of each output sample
            s: norm of input feature
            m: margin
            cos(theta + m)
        """
    def __init__(self, in_features, out_features, s=30.0, m=0.50, easy_margin=False):
        super(ArcMarginProduct, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.s = s
        self.m = m
        self.weight = Parameter(torch.FloatTensor(out_features, in_features))
        nn.init.xavier_uniform_(self.weight)

        self.easy_margin = easy_margin
        self.cos_m = math.cos(m)
        self.sin_m = math.sin(m)
        self.th = math.cos(math.pi - m)
        self.mm = math.sin(math.pi - m) * m

    def forward(self, input, label):
        # --------------------------- cos(theta) & phi(theta) ---------------------------
        cosine = F.linear(F.normalize(input), F.normalize(self.weight))
        sine = torch.sqrt((1.0 - torch.pow(cosine, 2)).clamp(0, 1))
        phi = cosine * self.cos_m - sine * self.sin_m
        if self.easy_margin:
            phi = torch.where(cosine > 0, phi, cosine)
        else:
            phi = torch.where(cosine > self.th, phi, cosine - self.mm)
        # --------------------------- convert label to one-hot ---------------------------
        # one_hot = torch.zeros(cosine.size(), requires_grad=True, device='cuda')
        one_hot = torch.zeros(cosine.size(), device='cuda')
        one_hot.scatter_(1, label.view(-1, 1).long(), 1)
        # -------------torch.where(out_i = {x_i if condition_i else y_i) -------------
        output = (one_hot * phi) + ((1.0 - one_hot) * cosine)  # you can use torch.where if your torch.__version__ is 0.4
        output *= self.s
        # print(output)

        return output
```

