# Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting

## 0. Abstract

1. **여러 시점을 예측**하는 Multi-horizon forecasting 시계열 데이터는 여러 유형의 입력이 있을 수 있음.
2. Input유형을 크게 아래와 같이 분류
    1. **시간에 따라 변하지 않는 변수** (static covariates)
    2. **시간에 따라 변하는 관측 가능한 변수** (Time varying Observable input)
    3. 타겟과 어떤 상호작용을 하는지 사전 정보가 없는 **외인성 변수** (Exogenous variable)
3. 현재까지 여러 딥러닝 모델들이 제안되었지만 대부분 Black box 모델들이어서 설명가능하지 못했음.
4. 따라서 이 논문에서는 **Attention 기반 구조와 설명 가능한 (explainable) 모델 TFT(Temporal Fusion Transformer)**를 제안

## 1. Introduction
# Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting

## 0. Abstract

1. **여러 시점을 예측**하는 Multi-horizon forecasting 시계열 데이터는 여러 유형의 입력이 있을 수 있음.
2. Input유형을 크게 아래와 같이 분류
    1. **시간에 따라 변하지 않는 변수** (static covariates)
    2. **시간에 따라 변하는 관측 가능한 변수** (Time varying Observable input)
    3. 타겟과 어떤 상호작용을 하는지 사전 정보가 없는 **외인성 변수** (Exogenous variable)
3. 현재까지 여러 딥러닝 모델들이 제안되었지만 대부분 Black box 모델들이어서 설명가능하지 못했음.
4. 따라서 이 논문에서는 **Attention 기반 구조와 설명 가능한 (explainable) 모델 TFT(Temporal Fusion Transformer)**를 제안

## 1. Introduction

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/58c50f3b-dde2-49fe-90d5-0a930573cfb5/Untitled.png)

- 미래의 여러 Time step에 대해서 예측을 진행하는 Multi-Horizion Forecasting은 시계열 예측 분야에서 중요한 문제
    - Mulit-Horizon은 전체 시계열 데이터에 대한 접근을 가능하게 하고 미래의 다양한 스텝들에 대한 예측 결과를 통해 활용할 수 있는 범위를 넓히기가 가능.
- Multi-horizon Forecasting을 위해 필요한 데이터 input
    - 현재는 관측을 통해 그 값을 알 수 있지만 미래의 값은 알 수 없는 Observed Input
    - 시간에 따라 달라지지만 현재에도 그 값을 알 수 있으며 미래에도 그 값을 알 수 있는 Time Vary Known Input (ex. week, weekend, holiday 등)
    - 시간에 관계없이 변하지 않는 정적 공변량 static covariates
- 과거에는 Autoregressive Model이 사용되었음.
    - 모든 Exogenous input들을 미래에도 알 수 있다는 가정을 하고 있고,
    - 대부분 time-dependent features들과 단순하게 결합하는 방식으로 multi-horizon의 다양한 종류의 입력을 고려하지 못했음.
    - 또한 대부분의 모델들이 Black Box
- Attention 기반의 모델들
    - sequence 데이터에 대한 해석력이 뛰어남.
    - time series 데이터에 적용했을 때에는 중요한 time step을 발견할 수는 있지만 feature간의 관계에서 어떤 feature가 중요하게 고려되고 있는지 각 feature들의 중요성을 알기 어렵다는 한계가 있었음
- Attention 기반의 DNN 구조인 TFT
    - Attention score를 통해 time step에서의 중요성을 해석할 수 있게 하고, static variable, encoder variable, decoder variable에 대해 해석력을 제공할 수 있음.

## 2. Related Work

## 3. Multi-horizon Forecasting

- TFT는 **Quantile Regression**로 예측을 진행
- 각 quantile 예측은 아래와 같은 형태를 보임.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3d446498-8168-4747-b947-f58e484d221a/Untitled.png)
    
    - $y$ : $q$번째 sample quantile에 대하셔 $t$ 시점에서 $τ$ 번째 뒤에 해당하는 예측에 해당.
    - $f$ : 예측 모델
    - $k$ : look-back window
    - $x$ : Known Input (미래에도 알 수있는 time varying 값, ex. weekend)
    - $z$ : obesrved input (이전에 관측된 값)
    - $s$ : static covariate 집합
    - $i$ : 시계열 데이터셋에 대한 한 instance
- 시작하는 지점인 $t$로부터 $k$개 이전까지의 값을 이용

## 4. Model Architechture

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9de415a8-e3fa-44e0-9b9e-7e4598abcc4a/Untitled.png)

### 4.1 Gating Mechanisms

- Exogenous Input과 Target 사이의 관계는 종종 미리 알수가 없어 어떤 변수들이 연관되어 있는지 예측하기가 어려움.
- TFT에서는 필요할때만 비선형 처리를 해 모델의 유연성을 높이고자 **GRN(Gated Residual Network)**를 제안
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2b0df580-7862-47ae-a7a1-199465604e84/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a9a1bb81-e239-437e-8c2f-152fe5160a80/Untitled.png)
    
- **ELU** : **Expoential Linear Unit Activation Function** 을 의미
    - 입력이 0보다 크면 Identify Function으로 동작하고 0보다 작을때에는 일정한 출력을 냄.
- **GLU(Gated Linear Unit)**을 사용해 주어진 데이터 셋에서 필요하지 않은 부분을 제거
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7d891617-3d0d-4d24-ada9-6eccb7cd7587/Untitled.png)
    
    - 시그모이드 함수를 활성화 함수로 사용.
- GLU는 TFT에서 Input a의 비선형 기여도를 바꿈.
    - 예를 들어 GLU의 출력이 모두 0이라면 비선형 기여도를 suppress 하기 위해 layer를 skip하는 것으로 취급함.

### 4.2 Variable Selection Networks

- **Instance-wise한 변수 선택**을 통해 예측에 필요한 feature 선택 + 불필요한 noisy 입력을 줄이기
- 대부분의 시계열 데이터에서는 예측과 관련 없는 값들이 많으므로 variable selection을 통해 성능 개선이 가능함.
- **Categorical Variable**에서는 **Entity Embedding**, **Continuous Variables**에 대해서는 **Linear Transformation**을 진행
- 모든 static covariates, past & future input들에 대해서는 분리된 변수 선택 네트워크 사용함.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8aa3b4bd-8541-4438-a791-ecc44c6284a4/Untitled.png)

- $ξ$을 **각 시점에서의 입력**이라 하고, Ξ를 **모든 이전 시점 t에 대한 입력들의 flatten 벡터**라 하면, 수식은 아래와 같다.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4c9bd173-b90b-4f8e-98aa-f87a48b36e6d/Untitled.png)
    
    - $*v_{χt}*$가 **Variable Selection Weight의 Vector**
    - $*c_s*$는 Static Covariate Encoder를 통해 얻은 context vector
- 매 시점마다, GRN을 통해 $ξt(j)$를 feeding하면서 비선형 처리를 위한 추가적인 Layer를 거침
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4c2d203c-36ee-4b2a-8437-2e0f127fbf14/Untitled.png)
    
    - $*ξt(j)*$는 **variable j에 전처리된 Feature Vector**
    - 각각의 GRN에 $*ξt(j)*$를 넣어줌을 통해 가중치를 모든 시점 *t*에 대해서 공유하는 가중합이 최종 Output으로 나오게 됨.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/63b50e2f-5005-49b6-9860-068c97938cec/Untitled.png)
    
    - 위의 식에서 $*v_{χt}^{(j)}*$는 **Vector *vχt*의 j번째 element**

### 4.3 Static Covariate Encoder

- TFT는 정적인 메타데이터의 정보를 통합하기 위해서 설계됨.
- 개벌적은 GRN인코더를 이용해 4개의 서로 다른 Context Vector인 $c_s$, $c_e$, $c_c$, $c_h$를 만듦
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1df99296-3462-4a06-8a35-50a270d4acfe/Untitled.png)
    
    - $c_s$ : context for temporal variable selection
    - $c_c$, $c_h$ : local processing of temporal features
    - $c_e$ : enriching of temporal features with static information
- 여기에 다들 은근슬쩍 끼고 있음

### 4.4 Interpretable Multi-Head Attention

- TFT는 Self-Attention Mechanism을 통해 다른 시점에 대한 Long-term relation을 파악함
- 구체적으로는 transformer 기반의 multi-head attention을 통해 해석력을 강화함.

### 4.5 Temporal Fusion Decoder

Temporal Fusion Decoder는 데이터셋에 존재하는 시간간의 관계에 대해서 학습함

1. **Locality Enhancement with seq2seq layer**
    1. Local Context를 끌어올리기 위한 작업.
    2. LSTM기반의 Encoder/Decoder를 사용.
    3. 이와 같은 인코더/디코더를 사용하면 시간 순서에 대한 적절한 inductive bias를 제공해주기 때문에 positional encoding을 대신하는 효과가 있음.
    4. 추가적으로 static meta data를 활용하기 위해 $c_c$ 와 $c_h$ 와 같은 context vector를 사용하는데 이는 cell state와 hidden state의 초기값
2. **Static Enrichment Layer**
    1. static 데이터에 시간 feature를 강화하는 요인!
3. **Temporal Self-Attention Layer**
    1. static enriched된 시계열 feature들을 하나의 matrix로 그룹화
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4d07f967-266c-48f3-b3a1-54ce88c2dcfc/Untitled.png)
        
    2. 이후에 **Interpretable Multi-Head Attention**을 예측하고자 하는 time step에 적용.
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/448a568b-264c-4bcc-bc9b-77c077bc5618/Untitled.png)
        
        1. multi-head attention : 셀프어텐션을 동시에 여러번 수행하는 것
    3. Decoder Masking이 Multi-Head Attention에 적용되는데, 각각의 temporal dimension이 그에 해당하는 feature에 상응할 수 있도록 하기 위함.
    4. self-attention layer는 tft가 rnn으로는 잡아내기 힘든 long-range dependency에 대하여 잡아낼 수 있도록 함은 물론, 추가적인 gating layer를 통해 학습을 촉진시킨다
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3a24d7b9-6b15-432c-bac3-5c0c06cf61f9/Untitled.png)
        
4. **Position-Wise feed-foreward Layer**
    1. self-attention layer에 추가적인 비선형 처리.
    2. Static Enrichment Layer와 유사하게 아래와 같이 GRN을 사용

### 4.6 Quantile Outputs

- 예측하고자 하는 time step에 대한 다양한 quantile 범위의 output 제공

## 5. Loss Function

- Quantile Loss 를 최소화하는 방향으로 학습을 진행

## 6. Performance Evaluation

## Conclusion

- *Attention-based deep learning model for interpretable high performance multi-horizon forecasting*
- 아래를 포함
    - seq2seq & attention-based temporal processing
    - static covariate encoder
    - gating components
    - variable selection
    - quantile prediction
- forecasting prediction에서 SOTA를 달성한 알고리즘.
![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/58c50f3b-dde2-49fe-90d5-0a930573cfb5/Untitled.png)

## 2. Related Work

## 3. Multi-horizon Forecasting

## 4. Model Architechture

### 4.1 Gating Mechanisms

- Exogenous Input과 Target 사이의 관계는 종종 미리 알수가 없어 어떤 변수들이 연관되어 있는지 예측하기가 어려움.
- TFT에서는 필요할때만 비선형 처리를 해 모델의 유연성을 높이고자 **GRN(Gated Residual Network)**를 제안
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2b0df580-7862-47ae-a7a1-199465604e84/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a9a1bb81-e239-437e-8c2f-152fe5160a80/Untitled.png)
    
- **ELU** : **Expoential Linear Unit Activation Function** 을 의미
    - 입력이 0보다 크면 Identify Function으로 동작하고 0보다 작을때에는 일정한 출력을 냄.
- **GLU(Gated Linear Unit)**을 사용해 주어진 데이터 셋에서 필요하지 않은 부분을 제거
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7d891617-3d0d-4d24-ada9-6eccb7cd7587/Untitled.png)
    
    - 시그모이드 함수를 활성화 함수로 사용.
- GLU는 TFT에서 Input a의 비선형 기여도를 바꿈.
    - 예를 들어 GLU의 출력이 모두 0이라면 비선형 기여도를 suppress 하기 위해 layer를 skip하는 것으로 취급함.

### 4.2 Variable Selection Networks

- **Instance-wise한 변수 선택**을 통해 예측에 필요한 feature 선택 + 불필요한 noisy 입력을 줄이기
- 대부분의 시계열 데이터에서는 예측과 관련 없는 값들이 많으므로 variable selection을 통해 성능 개선이 가능함.
- **Categorical Variable**에서는 **Entity Embedding**, **Continuous Variables**에 대해서는 **Linear Transformation**을 진행
- 모든 static covariates, past & future input들에 대해서는 분리된 변수 선택 네트워크 사용함.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8aa3b4bd-8541-4438-a791-ecc44c6284a4/Untitled.png)

- $ξ$을 **각 시점에서의 입력**이라 하고, Ξ를 **모든 이전 시점 t에 대한 입력들의 flatten 벡터**라 하면, 수식은 아래와 같습니다.
    
    $$
    ⁍
    $$
    
    - $*v_{χt}*$가 **Variable Selection Weight의 Vector**이며, $*c*$는 Static Covariate Encoder를 통해 얻을 수 있습니다. Static Variable에 대해서 Context Vector *c*는 Static Information을 담고 있다고 볼 수 있습니다.
    - grn : gating mechanism 을 통해 나온애.
- 매 시점마다, GRN을 통해 $ξt(j)$를 feeding하면서 비선형 처리를 위한 추가적인 Layer를 거치게 됩니다.
    
    $$
    ξt(j)=GRNξ(j)(ξt(j))
    $$
    
    - $*ξt(j)*$는 **Variable j에 대해 전처리된 Feature Vector**이며, 우리는 각자의 GRN에 $*ξt(j)*$를 넣어줌을 통해 가중치를 모든 시점 *t*에 대해서 공유하는 가중합을 구할 수 있으며 그 식은 아래와 같습니다.
        
        $$
        ξt=∑_{j=1}^{mχ}vχt(j)ξt(j)
        $$
        
- 위의 식에서 $*v_{χt}(j)*$는 **Vector *vχt*의 *j*번째 element**입니다.

### 4.3 Static Covariate Encoder

- TFT는 정적인 메타데이터의 정보를 통합하기 위해서 설계됨.
- 개벌적은 GRN인코더를 이용해 4개의 서로 다른 Context Vector인 $c_s$, $c_e$, $c_c$, $c_h$를 만듦
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/52890168-f64f-47c8-8115-0724b2e87f2c/Untitled.png)
    
    - $c_s$ : context for temporal variable selection
    - $c_c$, $c_h$ : local processing of temporal features
    - $c_e$ : enriching of temporal features with static information
- 여기에 다들 은근슬쩍 끼고 있음

### 4.4 Interpretable Multi-Head Attention

- TFT는 Self-Attention Mechanism을 통해 다른 시점에 대한 Long-term relation을 파악함
- 구체적으로는 transformer 기반의 multi-head attention을 통해 해석력을 강화함.

### 4.5 Temporal Fusion Decoder

Temporal Fusion Decoder는 데이터셋에 존재하는 시간간의 관계에 대해서 학습함

1. **Locality Enhancement with seq2seq layer**
    1. Local Context를 끌어올리기 위한 작업.
    2. LSTM기반의 Encoder/Decoder를 사용.
    3. 이와 같은 인코더/디코더를 사용하면 시간 순서에 대한 적절한 inductive bias를 제공해주기 때문에 positional encoding을 대신하는 효과가 있음.
    4. 추가적으로 static meta data를 활용하기 위해 $c_c$ 와 $c_h$ 와 같은 context vector를 사용하는데 이는 cell state와 hidden state의 초기값
2. **Static Enrichment Layer**
    1. static 데이터에 시간 feature를 강화함.
3. **Temporal Self-Attention Layer**
4. **Position-Wise feed-foreward Layer**
5. **Quantile Outputs**
    1. 예측하고자 하는 time step에 대한 다양한 **percentage 범위의 output을 제공**

## 5. Loss Function

- Quantile Loss 를 최소화하는 방향으로 학습을 진행

## 6. Performance Evaluation

## Conclusion

- *Attention-based deep learning model for interpretable high performance multi-horizon forecasting*
- 아래를 포함
    - seq2seq & attention-based temporal processing
    - static covariate encoder
    - gating components
    - variable selection
    - quantile prediction
- forecasting prediction에서 SOTA를 달성한 알고리즘.