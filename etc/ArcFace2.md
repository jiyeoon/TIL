
논문 링크 : [https://arxiv.org/abs/1801.07698](https://arxiv.org/abs/1801.07698)

[

ArcFace: Additive Angular Margin Loss for Deep Face Recognition

One of the main challenges in feature learning using Deep Convolutional Neural Networks (DCNNs) for large-scale face recognition is the design of appropriate loss functions that enhance discriminative power. Centre loss penalises the distance between the d

arxiv.org



](https://arxiv.org/abs/1801.07698)

1500회 넘게 인용된 아주 인기있는 논문 ArcFace! Kaggle의 상위 솔루션들에서는 꼬박꼬박 등장하는 개념이기도 한데요, 제가 생각하기에 최근 가장 인기있는 loss 함수가 아닐까 싶습니다. 2018년에 처음 나왔던 논문으로 "각도"라는 개념을 적용시켜 손실함수를 만들었다는 점에서 꽤나 인상깊은 내용이 많이 있는 것 같습니다.

ArcFace를 상위 솔루션들에서 많이 사용한다고 하긴 했는데, 어쨌든 이 클래스와 저 클래스를 구분시켜주는 minimum인 margin이 가장 중요한 포인트입니다. 잘못 margin을 설정하게 되면 오히려 triplet loss나 softmax보다 성능이 떨어지기 때문에 margin값을 서서히 증가시키는 방식을 많이 사용하는 것 같더라구요. ArcFace와 함께 얼굴인식(FR, Face Recognition)에서 많이 사용되는 손실 함수인 [triplet loss도 이전에 포스팅](https://butter-shower.tistory.com/233)을 해두었으니 한번 읽어보시는 것을 추천합니다! ㅎㅎ

---

> 시작하기에 앞서...

ArcFace라는 이름에서 **Arc**는 $arccos$에서 나왔는데요, 아크코사인이라고 부르는 이것은 **역삼각함수**입니다.

보통 가장 오른쪽 항의 모습이 가장 익숙하실 것 같습니다 ㅎㅎ

$$ y = arccos(x) = cos^{-1}(x) $$

역삼각함수를 수식으로 나타내면 아래와 같아요.

$$ x = cos(y) $$

"**역**"이라는 이름에서 알 수 있듯이 원래의 수식에서 x<->y를 서로 바꿔주는것이죠. ㅎㅎ 간단한 리마인드!! 


---

### 1. Keypoint : "각도"의 도입

기존 FR에서 DCNN(Deep Convolution Neural Network)를 학습시키는 방법은 크게 두가지였습니다. 두 방법 모두 FR에서 좋은 성능을 보였지만 나름의 단점이 있었죠.

1. Softmax 같이 다중 클래스 분류기를 훈련
   - 선형 변환 행렬의 크기가 Identities의 수에 따라 선형적으로 증가
   - 학습된 피처는 폐쇄형(Closed-set) 분류 문제의 경우에서는 분류할 수 있지만, 개방형(Open-set) 얼굴인식 문제일 경우에는 약함.
2. Triplet Loss같이 임베딩을 직접 학습
   - 대규모 데이터셋의 경우 얼굴 Triplet 갯수의 결합이 엄청나게 늘어나고, 상당한 반복 단계의 횟수 증가.

![img](https://norman3.github.io/papers/images/arcface/f02.png)

그래서 새롭게 도입한 방법이 바로 **ArcFace**인데요, 요약하자면 클래스간 *각도*를 통해 *margin*을 주어 서로 다른 클래스간에는 더 큰 격차를 벌이는 것을 말합니다. 

ArcFace는 로짓을 살짝 변형하는데요, $W^T_j x_i = ||W_j|| \cdot ||x_i|| \cos{\theta_j}$로 변경합니다. 여기서 $\cos{\theta_j}$는 weight $W_j$와 피처 $x_i$ 사이의 각도를 말합니다. 개별 가중치 $W_j$는 L2 normalization에 의해 고정되고 임베딩 피처 $x_i$도 마찬가지로 L2 normalization 연산을 해주고 re-scale연산 한 결과를 $s$라고 합니다. weight와 feature에 정규화를 하여 **예측이 가중치 사이의 각도에만 의존**하도록 해주어 학습된 임베딩 피처들은 반경이 $s$인 하이퍼스피어에 분산되도록 해줍니다. 즉, 원의 호 부분에만 모여있게 해주는 것이죠. 마지막으로 $x_i$와 $W_{y_i}$사이의 추가 각도 마진 패널티 $m$이 추가해줘 일치하지 않는 클래스는 더욱 멀어지도록 해줍니다. 


![img](https://norman3.github.io/papers/images/arcface/f03.png)

위의 왼쪽 그림은 softmax고 오른쪽은 arcface인데요, 8개의 클래스별로 색을 칠한 모습닙니다. softmax은 서로 다른 두 클래스 사이의 경계값이 모호한 반면 arcface에서는 각도 기반으로 margin을 주어 서로 다른 두 클래스 사이에 경계를 분명히 했습니다. 

이렇듯 직접적으로 margin을 두어 마진값을 최적화하는 것으로, 구현이 매우 쉽고 성능이 좋은 것다는 것이 이 논문에서 하고싶은 말입니다. ㅎㅎ 여기서 $\theta$는 역삼각함수 $arccos$를 통해 구할 수 있겠죠? 이 $\theta$를 학습시키는 것이 arcface에서는 관건입니다.


### 2. 수식

$$ L=-\frac{1}{N}\sum_{i=1}^N \log \left(\frac{e^{s(\cos{(\theta_{y_i}+m)})}}{e^{s(\cos{(\theta_{y_i}+m)})} + \sum_{j=1, j \neq y+i}^n e^{s\cos{(\theta_j)}} }\right) $$

### 3. 구현 방법

#### (1) 슈도 코드

![img](https://norman3.github.io/papers/images/arcface/a01.png)

#### (2) Pytorch

```python
class ArcFace(Layer):
    """
    Implementation of ArcFace layer. Reference: https://arxiv.org/abs/1801.07698
    
    Arguments:
      num_classes: number of classes to classify
      s: scale factor
      m: margin
      regularizer: weights regularizer
    """
    def __init__(self,
                 num_classes,
                 s=30.0,
                 m=0.5,
                 regularizer=None,
                 name='arcface',
                 **kwargs):
        
        super().__init__(name=name, **kwargs)
        self._n_classes = num_classes
        self._s = float(s)
        self._m = float(m)
        self._regularizer = regularizer

    def build(self, input_shape):
        embedding_shape, label_shape = input_shape
        self._w = self.add_weight(shape=(embedding_shape[-1], self._n_classes),
                                  initializer='glorot_uniform',
                                  trainable=True,
                                  regularizer=self._regularizer,
                                  name='cosine_weights')

    def call(self, inputs, training=None):
        """
        During training, requires 2 inputs: embedding (after backbone+pool+dense),
        and ground truth labels. The labels should be sparse (and use
        sparse_categorical_crossentropy as loss).
        """
        embedding, label = inputs

        # Squeezing is necessary for Keras. It expands the dimension to (n, 1)
        label = tf.reshape(label, [-1], name='label_shape_correction')

        # Normalize features and weights and compute dot product
        x = tf.nn.l2_normalize(embedding, axis=1, name='normalize_prelogits')
        w = tf.nn.l2_normalize(self._w, axis=0, name='normalize_weights')
        cosine_sim = tf.matmul(x, w, name='cosine_similarity')

        training = resolve_training_flag(self, training)
        if not training:
            # We don't have labels if we're not in training mode
            return self._s * cosine_sim
        else:
            one_hot_labels = tf.one_hot(label,
                                        depth=self._n_classes,
                                        name='one_hot_labels')
            theta = tf.math.acos(K.clip(
                    cosine_sim, -1.0 + K.epsilon(), 1.0 - K.epsilon()))
            selected_labels = tf.where(tf.greater(theta, math.pi - self._m),
                                       tf.zeros_like(one_hot_labels),
                                       one_hot_labels,
                                       name='selected_labels')
            final_theta = tf.where(tf.cast(selected_labels, dtype=tf.bool),
                                   theta + self._m,
                                   theta,
                                   name='final_theta')
            output = tf.math.cos(final_theta, name='cosine_sim_with_margin')
            return self._s * output
```


### 4. ArcFace의 장점

1.  Engaging
    -   정규화된 hypersphere에서 호(Arc)와 각도(Angle) 사이의 정확한 일치성 때문에 직접 거리 마진을 최적화함.
2.  Effective
    -   ArcFace는 대규모 이미지와 비디오 Dataset을 포함하는 10개의 얼굴인식 benchmark에서도 최첨단 성능을 달성함.
3.  Easy
    -   구현이 쉬움.  
        [##_Image|kage@bXCvXm/btq6gees46G/HFKbJ2nArQtRKpKnSlszH1/img.png|alignCenter|data-origin-width="899" data-origin-height="276" data-ke-mobilestyle="widthOrigin"|||_##]
    -   SphereFace, Large-margin softmax loss for CNN 연구들과는 대조적으로 ArcFace는 안정적인 성능을 가지기 위해 다른 손실함수들과 결합해 사용할 필요가 없으며, 어떤 훈련 데이터셋에서도 쉽게 수렴(Converge)할 수 있음.
4.  Efficient
    -   훈련동안 무시할 수 있는 계산 복잡도만 추가함.

---

논문에서 가장 많이 언급되는 비율에 관한 그래프인데요, Triplet Loss가 압도적이고 ArcFace도 점차 늘어나는 추세인 것 같습니다. 잘 알아두면 좋을 것 같은 ArcFace... ^^... 높은 성능의 face recognition 혹은 multi-class classification을 할 때 사용하면 좋을 것 같네요.

내마음대로 논문리뷰 제목처럼 너무 제마음대로 리뷰였지만,,, ㅎㅎ 이만 마치도록 하겠습니다~!

---

> Reference

- <https://www.kaggle.com/chankhavu/keras-layers-arcface-cosface-adacos>
- <>