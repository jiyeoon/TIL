- [Metric Learning의 개념과 Deep Metric Learning](#metric-learning의-개념과-deep-metric-learning)
  - [1. 거리 함수 (Distance Function)](#1-거리-함수-distance-function)
  - [2. Deep Metric Learning](#2-deep-metric-learning)
  - [3. Constrative Embedding](#3-constrative-embedding)
  - [4. Triplet Embedding](#4-triplet-embedding)


#  Metric Learning의 개념과 Deep Metric Learning

## 1. 거리 함수 (Distance Function)

데이터간의 유사도를 수치화하기 위해 일반적으로 거리함수(metric function)을 사용한다. 가장 대표적인 거리 함수로는 유클리디안 거리가 있다. 두 데디터 $\textbf{x}_1 \in \mathbb{R}^{d}$과 $\textbf{x}_2 \in \mathbb{R}^d$에 대해 아래와 같이 정의한다.

$$ d_E(\textbf{x}_1, \textbf{x}_2) = \sqrt{\sum_{i=1}^{d} (\textbf{x}_{1, i} - \textbf{x}_{2, i})^2} \tag{1} $$

또 다른 대표적인 거리 함수로는 각 축의 방양으로의 분산까지 고려한 Mahalanobis 거리가 있으며, 두 점 사이의 거리는 아래와 같이 정의된다.

$$ d_M(\textbf{x}_1, \textbf{x}_2) = \sqrt{{(\textbf{x}_1 - \textbf{x}_2)}^T S^{-1} {(\textbf{x}_1 \textbf{x}_2)}} \tag{2} $$

식 $S$는 공분산 행렬이다. 이외에도 cosine similarity나 Wesserstein 거리와 같은 다양한 거리 함수가 있다.

데이터 마이닝 및 머신러닝의 대표적인 알고리즘인 k-평균 군집화, DBSCAN, 결정트리 등을 비롯하여 여러 샘플링 알고리즘 등이 이러한 거리 함수를 기반으로 동작하기 때문에 데이터에 적합한 거리 함수를 결정하는 것은 알고리즘의 정확도 측면에서 아주 중요하다. 실제로 어떠한 거리 함수를 이용하는가에 따라 예측 모델의 성능이 2배 이상 차이나는 경우도 있다.

그러나 미리 정의된 거리 함수 중에서 모든 데이터에 대해 적합한 거리 함수는 현실적으로 존재하지 않는다. 이러한 이유로 데이터에 적합한 거리 함수를 머신러닝 알고리즘으로 직접 만드는 metric learning이 활발하게 연구되고 있다.

## 2. Deep Metric Learning

데이터에 적합한 거리 함수라는 표현을 머신러닝의 관점에서 다시 말하면, 데이터의 각 목표 값에 대해 데이터를 구분하기 쉽게 만들어주는 거리 함수를 의미한다. 아래 그림은 이러한 관점에서 metric learning의 목적을 시각적으로 보여준다. 기존의 feature로는 분류가 쉽지 않았던 데이터에 대해 class label별로 잘 구분할 수 있게 만드는 metric을 학습함으로써 분류 모델을 만드는 문제가 매우 단순해졌다. 

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fdpuky0%2FbtqIjeVyxZo%2FSnmmbKkMGT6aD1JSWybngk%2Fimg.png)

Metric learning을 통해 학습된 새로운 거리 함수는 일반적으로 embedding 함수 $f: \mathbb{R}^r \rightarrow \mathbb{R}^m$를 통해 변환된 새로운 데이터 표현에 대한 유클리디언 거리로 정의된다. 예를 들어, metric learning을 통해 학습된 거리 함수를 $f(\textbf{x};\theta)$라고 할 때, 두 데이터 $\textbf{x}_1$과 $\textbf{x}_2$에 대한 새로운 거리 함수는 

$$ d_{\theta}(\textbf{x}_1, \textbf{x}_2) = ||f(\textbf{x}_1) - f(\textbf{x}_2) ||_2^2 \tag{3} $$

과 같이 정의된다. 따라서 metric learning 문제의 목적은 **데이터를 각 목표값에 따라 잘 구분되도록 변환하는 embedding 함수 $f$를 학습하는 것**이 된다. 이 때, f가 단순한 선형 변환이 아니라 deep neural network일 경우에 앞에 deep을 붙여 deep metric learning이라고 한다.

아래에서는 deep metric learning에 대한 대표적인 두가지 방법인 contrasive embedding과 triplet embedding을 살펴보도록 하자.

## 3. Constrative Embedding

**이진분류**(binary classification)에 이용될 수 있는 metric learning. 각각의 tuple $(\textbf{x}_i, \textbf{x}_j, y_{ij})$에 대해 contrastive loss는 아래와 같이 정의된다.

$$ L_{C} = \frac{1}{N}\sum_{i=1}^{N/2} \sum_{j=1}^{N/2} y_{ij}d(\textbf{x}_i, \textbf{x}_j) + (1 - y_{ij})\{\text{max}(0, \alpha - d(\textbf{x}_i, \textbf{x}_j))\} \tag{4} $$

위의 contrastive loss에서는 embedding network $f$에 대해 $d(\textbf{x}_i, \textbf{x}_j) = ||f(\textbf{x}_i) - f(\textbf{x}_j)||_2^2$로 정의된다.

- $y_{ij}$는 실제값으로, $\textbf{x}_i$와 $\textbf{x}_j$가 같은 클래스면 1이고 아니면 0이다.
- $\alpha$ : 하이퍼파라미터로, 두 데이터가 다른 클래스에 속할 경우 $\alpha$ 이상의 거리를 갖도록 제한하는 역할을 한다.

Contrastive embedding에서는 $L_C$를 최소화하도록 $f$의 모델 파라미터를 학습시킴으로써 데이터를 잘 구분할 수 있는 새로운 embedding을 만들어낸다.

## 4. Triplet Embedding

Triplet Embedding은 **다중분류**(multi-class classification)에서 이용되는 metric learning이다. Embedding을 위한 triplet losss는 주어진 데이터셋에서 선택된 데이터인 anchor, 그리고 anchor와 동일한 class label을 갖는 positive sample, 다른 class label을 갖는 negative sample로 아래 식과 같이 정의된다. 

$$ L_{T} = \frac{3}{2N} \sum_{i=1}^{M/3} \text{max}(0, d(\textbf{x}_i, \textbf{x}_{i,p}) - d(\textbf{x}_i, \textbf{x}_{i,n}) + \alpha) \tag{5} $$

이 식에서 $\textbf{x}_{i, p}$와 $\textbf{x}_{i, n}$은 각각 현재 선택된 anchor $\textbf{x}_i$의 positive sample과 negative sample이다. 식 (5)의 triplet loss를 $f$의 model parameter $\theta$에 대해 최소화함으로써 embedding space에서 achor와 positive sample의 거리는 가까워지고, negative sample과의 거리는 멀어진다.

아래 그림은 tiplet embedding의 개념을 보여준다. 일반적으로 triplet embedding에서 positive sample과 negative sample은 랜덤 샘플링을 기반으로 추출되며 이외에도 embedding의 성능을 향상시키기 위한 여러 샘플링 방법이 제안되었다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FFboxH%2FbtqIlvR6Xbd%2Fm7VKQ1VnNlrGwELyrSIve0%2Fimg.png)


> Reference
- <https://untitledtblog.tistory.com/164>
