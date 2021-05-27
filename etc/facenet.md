![img](https://github.com/HwangToeMat/HwangToeMat.github.io/blob/master/Paper-Review/image/FaceNet/img6.jpg?raw=true)

FaceNet은 각각의 얼굴 이미지를 128차원으로 임베딩하여 유클리드 공간에서 이미지간의 거리를 통해 분류하는 모델이다.

얼굴 사진에서 그 사람에 대한 특징 값(feature)를 구해주는 모델로, 그 값을 활용하여 값들 간의 거리를 통해 이미지에 대한 Identification, verification, clustering을 할 수 있게 된다. 

![img](https://github.com/HwangToeMat/HwangToeMat.github.io/blob/master/Paper-Review/image/FaceNet/img7.jpg?raw=true)

이 때, triplet loss를 사용한 Metric Learning으로 모델을 학습했다. 아래에서 자세히 다루도록 하겠다.

추가적으로 기존의 모델들이 2D나 3D로 aligned된 얼굴 이미지를 필요로했던 것에 비해 FaceNet은 그러한 과정 없이 높은 성능이 나왔다. (물론 얼굴 크기에 맞게 잘라주는 과정은 필요하다)

## Triplet Loss를 사용한 Metric Learning

![img](https://github.com/HwangToeMat/HwangToeMat.github.io/blob/master/Paper-Review/image/FaceNet/img1.jpg?raw=true)

FaceNet 학습 과정에서 Metric learning을 하기 위해 Triplet Loss를 사용했다. 학습시 미니배치 안에서 어떠한 사람(Anchor)에 대해 같은 사람(Positive)와 다른 사람(Negative)를 지정해놓는다. 그리고 임베딩된 값들의 유클리드 거리를 구해 그림과 같이 Anchor와 Positive의 거리는 가까워지고 Negative와의 거리는 멀어지도록 학습시켰다. 

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7183b29c-5302-4859-8ed1-021108e50d31/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7183b29c-5302-4859-8ed1-021108e50d31/Untitled.png)

$\alpha$는 하이퍼파라미터로, 마진을 의미한다. 따라서 Loss를 최소화한다는 것의 의미는 Positive의 거리는 가까워지도록 하고 Negative의 거리는 멀어지도록 하는 것이다.

여기서 잠깐 모델의 성능을 높이기 위해 Hard Positive(같은 사람이지만 다르게 보이는 사람)과 Hard Negative(다른 사람이지만 닮은 사람)와 같이 학습을 방해하는 요소를 제어하기위해 아래와 같은 식을 사용하였다. 

![img](https://github.com/HwangToeMat/HwangToeMat.github.io/blob/master/Paper-Review/image/FaceNet/img2.jpg?raw=true)

Hard Positive는 위의 첫번째 식과 같고, Hard Negative는 아래 식과 같이 나타낼 수 있다. 이 모델에서는 Hard Positive는 전부 학습을 진행했지만 Hard Negative는 세번째 식을 만족할 경우에만 학습을 진행하였다. 

> 참고

- [https://hwangtoemat.github.io/paper-review/2020-04-02-FaceNet-내용/](https://hwangtoemat.github.io/paper-review/2020-04-02-FaceNet-%EB%82%B4%EC%9A%A9/)