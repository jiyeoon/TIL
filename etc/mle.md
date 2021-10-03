
# 최대우도법 (Maximum Likelihood Estimation, MLE)

> 어떤 평균값을 갖는 확률밀도로부터 이 샘플들이 추출되었을까?

## 정의

- **데이터 밀도 추정 방법**
- 파라미터 $\theta = ({\theta}_1, ..., {\theta}_m)$ 으로 구성된 어떤 확률밀도함수 $P(x|\theta)$에서 관측된 표본 데이터 집합을 $x = (x_1, x_2, ..., x_n)$이라고 할 때, 이 표본들에서 파라미터 $\theta = ({\theta}_1, ..., {\theta}_m)$을 추정하는 방법\

### 예시 

아래와 같은 5개의 데이터를 얻었다고 가정

$ x  = {1, 4, 5, 6, 9}$

아래 그림을 보았을 때 데이터 $x$는 주황색 곡선과 파란색 곡선 중 어떤 곡선으로부터 추출되었을 확률이 더 높을까?

![img](https://raw.githubusercontent.com/angeloyeo/angeloyeo.github.io/master/pics/2020-07-17-MLE/pic1.png)

주황색 곡선에서 이 데이터를 얻었을 가능성이 더 커 보임. 

따라서 데이터를 관찰함으로써 이 데이터가 추출되었을 것으로 생각되는 분포의 특성을 추정할 수 있다. 여기서 추출된 분포가 정규분포라 가정하고, 분포의 특성 중 평균을 추정하려고 했다. 


## Likelihood function

![img](https://raw.githubusercontent.com/angeloyeo/angeloyeo.github.io/master/pics/2020-07-17-MLE/pic2.png)

- 위 그림에서 주황색 후보 분포에 대해 각 데이터들의 likelihood 기여도를 점선의 높이로 나타난다
- likelihood란 **지금 얻은 데이터가 이 분포로부터 나왔을 가능도**를 말한다. 
- 수치적으로 이 가능도를 계산하기 위해서는 각 데이터 샘플에서 후보 분포에 대한 높이를 계산해서 다 곱한것을 이용할 수 있다.
  - 계산된 높이를 더해주지않고 곱해주는 것은 모든 데이터들의 추출이 독립적으로 연달아 일어나는 사건이기 때문
- 계산된 가능도를 생각해볼 수 있는 모든 후보군에 대해 계산하고 이것을 비교하면 지금 얻은 데이터를 가장 잘 설명할 수 있는 확률분포를 얻게된다.


지금까지 얘기한 likelihood를 수학적으로 설명하면 아래와 같다

- 전체 표본 집합의 결합 확률 밀도를 likelihood function이라 하고 아래와 같이 나타낼 수 있다
  - $$P(x|\theta) = \prod_{k=1}^{n}P(x_k|\theta)$$
- 위 식의 결과 값이 가장 커지는 $\theta$를 추정값 ${\hat{\theta}}$ 로 보는 것이 가장 그럴듯하다
- 위 식을 likelihood function이라고 하고 보통은 자연로그를 이용해 아래와 같이 log-likelihood function $L(\theta|x)$를 이용한다
  - $$ L(\theta|x) = \log{P(x|\theta)} = \sum_{i=1}^{n} \log{P(x_i|\theta)} $$


## Likelihood function의 최대값을 찾는 방법

- 결국 Maxium Likelihood Estimation은 Likelihood 함수의 최대값을 찾는 방법이라 할 수 있다
- log 함수는 단조증가 함수이기 때문에 likelihood function의 최대값을 찾으나 log-likelihood function의 최대값을 찾으나 두 경우 모두의 최대값을 갖게해주는 정의역의 함수 입력값은 동이랗다
- 따라서 보통은 계산의 편의를 위해 log-likelihood의 최대값을 찾는다
- 어떤 함수의 최대값을 찾는 방법 중 가장 보편적인 방법은 미분계수를 이용하는 것이다
- 즉, 찾고자하는 파라미터 $\theta$에 대하여 다음과 같이 편미분하고 그 값이 0이 도도록 하는 $\theta$를 찾는 과정을 통해 likelihood 함수를 최대화 시켜줄 수 있는 $\theta$를 찾을 수 있다

$$ \frac{\partial}{\partial \theta}L(\theta|x) = \frac{\partial}{\partial \theta}\log P(x|\theta) = \sum_{i=1}^{n}\frac{\partial}{\partial\theta}\log P(x_i|\theta) = 0 $$




