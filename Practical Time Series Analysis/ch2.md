
- [Ch2. 시계열 데이터의 발견 및 다루기](#ch2-시계열-데이터의-발견-및-다루기)
  - [사전관찰 (look ahead)](#사전관찰-look-ahead)
  - [시계열 데이터를 다루는 방법](#시계열-데이터를-다루는-방법)
  - [누락된 데이터 다루기](#누락된-데이터-다루기)
    - [1. 포워드 필(forward fill)](#1-포워드-필forward-fill)
    - [2. 이동편균 (moving average)](#2-이동편균-moving-average)
    - [3. 보간법 (interpolation)](#3-보간법-interpolation)
  - [업샘플링과 다운샘플링](#업샘플링과-다운샘플링)
  - [데이터 평활 (smoothing)](#데이터-평활-smoothing)

---

# Ch2. 시계열 데이터의 발견 및 다루기

## 사전관찰 (look ahead)

- 미래의 어떤 사실을 안다.
- 모델의 설계, 학습, 검증 단계에서는 알 수 없으나 데이터를 통해 실제로 알아야 하는 시점보다 더 일찍 미래에 대한 사실을 발견하는 방법.
- 모델의 초기 동작에 영향을 줌.


## 시계열 데이터를 다루는 방법

1. 해결하고자 하는 문제에 맞는 형태로 데이터의 간격을 교정
2. 사전 관찰을 피하기 위해 가용 데이터를 생산하는 타임 스탬프를 데이터에 사용하지 않는 방법을 이해
3. '아무 일도 일어나지 않았더라도' 관련된 모든 기간을 기록
4. 사전 관찰을 피하기 위해 아직 알아서는 안되는 정보를 생산하는 타임스탬프를 데이터에 사용하지 안흔ㄴ 방법을 이해


## 누락된 데이터 다루기

1. 대치법 (imputation)
   - 데이터 셋 전체의 관측에 기반하여 누락된 데이터를 채워 넣는 방법
2. 보간법 (interpolation)
   - 대치법의 한 형태로 인접한 데이터를 사용하여 누락된 데이터를 추정하는 방법
3. 영향을 받은 기간 삭제


### 1. 포워드 필(forward fill)

- 누락된 값의 직전값 삽입
- 계산이 복잡하지 않고 실시간 스트리밍 데이터에 쉽게 적용 가능. 


### 2. 이동편균 (moving average)

- 롤링 평균 또는 중앙값. 과거 데이터의 부분집합들의 평균 or 중앙값
- rolling window


### 3. 보간법 (interpolation)

- 전체 데이터를 기하학적인 행동에 제한하여 누락된 데이터 값을 결정하는 방법.
- 선형(linear) 보간법 : 누락된 데이터가 주변 데이터에 선형적인 일관성을 갖도록 제한.
- 스팔라인 보간법 : 다항식 보간법
- 선형적인 추세로 움직이지 않는 경우에는 부적절.


## 업샘플링과 다운샘플링

1. 다운샘플링
   - 데이터의 빈도를 줄이는 것. (예) 일단위 데이터 -> 주단위 데이터
   - 아래와 같은 경우에 사용
     - 원본 데이터의 시간 단위가 실용적이지 않은 경우
     - 계절 주기의 특정 부분에 집중하는 경우
     - 더 낮은 빈도의 데이터에 맞추는 경우
2. 업샘플링
   - 더 자주 측정하는 것.
   - 실제론 어려운 일. 더 많은 시간의 레이블이 추가되는 것은 맞지만 더 많은 정보 자체가 추가되는 것은 아님.
   - 아래와 같은 경우에 사용
     - 시계열이 불규칙적인 상황
     - 입력이 서로 다른 빈도로 샘플링 된 상황



## 데이터 평활 (smoothing)

- 평활의 목적
  - 측정의 오류, 높게 튀는 측정치 제거
  - 가공하지 않은 데이터가 부적합한 경우.
- 지수 평활 (exponential smoothing)
  - 스무딩할 때 모든 데이터를 똑같이 취급하고 싶지 않을때, 최근의 데이터일수록 유익한 것으로 살리고 싶을때 사용하는 방식.
  - 좀 더 최근 데이터일수록 가중치를 두어 시간의 특성을 더 잘 인식할 수 있도록 만들어진 방법.
  - $t$라는 특정 시간에 대해 평활된 값 : $S_t = d \times S_{t-1} + (1-d) \times x_t$
  - 아래와 같은 연쇄적 형태를 띔. 
    - $$ d^n \times x_{t-n} + d^{n-1} \times x_{t-(n-1)} + ... + d \times x_{t-1} $$
- 파이썬 판다스에서 `ewm()` 함수로 사용 가능.
  - `df['col1'].ewm(alpha=0.5).mean()`
  - 평활 요인 (smoothing factor)  `alpha` : 기존의 평균 정보를 유지하는 것에 비해 현재의 값을 얼마나 갱신하는지에 대한 영향. 현재 값에 가까울수록 더 빨리 갱신.

