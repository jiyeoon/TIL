# NFNet

안녕하세요? 이번에 리뷰할 논문은 NFNet입니다. Deepmind에서 올해(2021) 2월 발표한 따끈따끈한 논문이에요. 최근 가장 좋은 SOTA를 보이고 있는 모델로, 최근 캐글 상위 솔루션들을 보면 대부분 NFNet을 사용하고 있더라구요. 지금까지 EfficientNet이 속도와 성능 면에서 모두 강세를 보였었는데, 새로운 모델의 등장이라 한번 정리를 해보려고 합니다. MobileNet이나 EfficientNet을 한번도 정리하지도 않고 바로 정리하는 것 같긴 하지만...... 시작하겠습니다! 


## 시작하기에 앞서.. Batch Normalization에 대해서 (Abstract)

대부분의 네트워크들은 모두 batch normalization을 사용하고 있는데요, 배치정규화는 gradient vanishing/exploding의 문제를 해결하는데 아주 효과적이어서 지금까지의 SOTA 모델들에서 꼬박꼬박 등장하는 개념이었습니다. normalization은 원래 트레이닝 셋 전체에 대해 실시하는 것이 좋겠지만, 미니배치 방식을 사용하게 되면 파라미터의 업데이트가 배치 단위로 일어나기 때문에 미니배치 단위로 batch normalization을 해줍니다. 

배치 정규화는 워낙 많이 사용되고 필수적인 것 같지만, 동시에 단점이 존재합니다. 

- 연산이 많이 필요로 한다 -> 계산 복잡도가 증가한다
- Fine-tuning이 필요한 다른 하이퍼파라미터가 필요하다
- 배치 사이즈가 작을 경우 성능이 저하된다.
- 분산학습에서 구현 에러를 일으킨다


## Adaptive Gradient Clipping

Gradient Clipping은 NLP에서 안정화를 위해 많이 사용되는 것 중 하나로, 쉽게 말해 기울기(gradient)가 특정 임계값을 초과하지 않도록 하여 모델 학습을 안정화하는 방법입니다. 최근에는 gradeint descent에 비해 더 높은 learning rate에서도 더 빠른 수렴(covergence)를 보여주는 논문들이 등장했었습니다. 그래서 해당 논문에서는 이를 잘 활용하는 방안으로 **Adaptive Gradient Clipping(AGC)** 를 도입하게 됩니다. 






## 파이토치 구현 코드

<https://github.com/rwightman/pytorch-image-models/blob/master/timm/models/nfnet.py>



> References

- <https://wikidocs.net/61375>
- <https://github.com/deepmind/deepmind-research/tree/master/nfnets>
- - 