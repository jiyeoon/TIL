
# 스파크 튜닝하기

스파크는 여러층의 데이터 추상화 구조와 분산 아키텍쳐가 녹아있는 복잡한 프레임워키이기 때문에 job이 단지 실행되는 것을 넘어 더 효율적으로 처리될 필요가 있습니다. 

스파크 튜닝을 잘하면 더 효율적인 spark job을 만들 수 있습니다.

## 1. Spark 배경 지식

### Spark job 실행 흐름

- Spark와 YARN은 효율적인 클러스터 리소스 관리를 위해 여러개의 논리적인 단위로 spark job을 구성
- 구성 단위는 Application, Job, Task, Stage, Worker, Executor 등 다양함
- Executor는 실질적으로 연산을 하는 프로세스로, 이를 기준으로 메모리 계층을 구성하고 병렬성 크기를 결정
- spark는 물리적으로 보통 1개의 Master와 1개 이상의 Worker 노드로 구성
- 1개의 Worker 노드는 1개 이상의 Executor 프로세스를 동작함
- Spark Job은 DAG 스케줄러에 의해 1개 이상의 task로 쪼개짐
- 1개의 Executor는 1개 이상의 task를 순차적으로 혹은 병렬적으로 실행
- 1개의 Executor는 하나의 JVM(Java Virtual Machine)을 가짐
- 각각의 Executor는 똑같은 개수의 Core와 똑같은 크기의 Memory(heap)을 가짐
- 분산 능력이 없다면 Spark Job은 오직 하나의 Executor에서 실행
- 병렬성이 아예 없다면 하나의 Executor와 하나의 Core에서 실행


### Executor 메모리 계층 구성

Spark와 YARN은 다음과 같이 Executor 컨테이너 단위로 메모리 계층을 구성한다. 다양한 파라미터 중에서 오직 `spark.executor.memory` 한개만 실제로 Task를 실행할때 사용된다. Spark이 요청받은 리소스 정보는 YARN에게도 전달된다.
Spark 파라미터와 함께 YARN 파라미터도 있다.

![img](https://bygritmind.files.wordpress.com/2020/10/image-9.png)

- yarn.nodemanager.resource.memory-md : 1개의 노드에 있는 모든 Executor 컨테이너들이 사용하는 메모리 총합
- spark.yarn.executor.MemoryOverhead : 오버헤드를 위한 여유분 메모리 크기
- spark.executor.memory : 1개의 Executor가 사용하는 메모리 크기
- spark.memoryFraction : Task 실행, 셔플, 조인, 정렬, 집계를 위한 데이터 저장 비율
- spark.storage.memoryFraction : Cache, Broadcast, Accumulator를 위한 데이터 저장 비율

### RDD (Resilient Distributed Datasets)

Spark 아키텍쳐는 크게 RDD와 DAG로 2가지의 주요한 추상화(abstraction)을 가진다. RDD는 특히 Spark 프로그래밍 튜닝 기법에서 많이 다룬다.

- "Spark = RDD + Interface" 공식처럼 RDD는 분산 환경과 Spark에 맞는 특별한 자료구조다.
- RDD는 Spark 고유의 자료구조로 분산이 용이하게 여러개 파티션으로 구성되어 있다.
- Read-only와 Immutable의 특징으로 Fault-tolerance를 쉽게 극복할 수 있다.
- Spark job은 RDD를 가공해 새로운 RDD를 얻는 식의 반복으로 구성됨.
- RDD는 변환(transformation)과 액션(action)의 두 가지 operator가 있음.
- Lazy-execution으로 Operation 파이프라인 최적화시킴
- 변환 함수는 Narrow와 Wide로 구분되며 Wide는 네트워크를 통해 데이터 셔플이 발생하는 아주 비싼 operator임.

---

## 2. Spark 환경 설정

Spark는 분산환경에서 동작하고 **메모리를 주로 활용**하기 때문에 그만큼 리소스 할당이 중요하다. 데이터 크기, Spark API 함수 종류, 그리고 YARN 스케줄링 방식에 따라 적합한 리소스 할당 방법이 필요하다. Spark는 Spark property, Environment 변수, Logging 이라는 세가지 종류의 환경 변수가 있다. 이 글에서는 Spark property만 다룬다. (편의상 Spark property를 Spark 파라미터로 명명) 또한, Spark는 YARN과 함께 동작하기에 YARN 환경 변수도 함께 고려한다.

### 2.1 설정 방법

~ 회사 서버에서는 이미 설정되어있으므로 일단 패스~

---

## 3. Spark 프로그래밍

### 3.1 파티셔닝

분산 데이터 처리는 큰 데이터를 작은 데이터들로 분할해서 각개격파하는 Divide and Conquer 철학을 가진다. Spark에서는 작은 데이터를 지칭하는 논리적인 데이터 청크 단위인 **파티션**(partition)이 있다. 하나의 파티션에서 하나의 태스크가 실행된다. 이론적으로는 하나의 코어가 한개의 파티션을 점유하지만 실제론 2~3배의 파티션을 가져도 된다.

파티션 개수를 제어하는 파티셔닝 기법은 클러스터 성능에 큰 영향을 준다. 각 파티션이 일정 크기의 데이터(128MB ~ 1GB)를 가지는 것에 한해서 *파티션 개수를 최대화하여 병렬성을 높이는 것이 좋다.* 파티션이 매우 적은 크기의 데이터를 가진다면 작업 능률은 떨어진다. 파티셔닝은 개수를 제어하는 것 뿐만 아니라 파티션의 *데이터 분포를 균등하게 조절*하는 역할도 한다. 데이터가 한쪽 파티션에 쏠리게 되면 추측 실행(speculative execution)이 증가해 성능 저하를 유발하고 메모리 에러로 프로그램이 종료되기도 한다. 

데이터롤 로딩할 때 Spark는 데이터 크기에 맞게 자동으로 적절한 파티션 개수를 설정한다. 이후에 Narrow 변환 함수만 실행된다면 파티션 개수의 변함은 없다. Join, GroupBy와 같이 데이터 셔플을 유발하는 Wide 변환 함수가 실행되면 디폴트 200개로 재설정된다. 데이터 크기가 적당하고 심플한 API 함수로만 구성된다면 파티셔닝 기법은 크게 중요하지 않다. 하지만 데이터가 크고 API 함수 파이프라인으로 구성된다면 적재적소에 파티셔닝을 해줘야 한다.

파티셔닝 해야하는 한 가지 예를 들어보자. **Filter** 변환 함수를 실행하면 보통 데이터 분포가 균등하지 않고 **편향**(skewed) 된다.

![img](https://bygritmind.files.wordpress.com/2020/10/image-18.png)

이러한 경우 다음과 같은 파티셔닝 기법을 사용하여 고른 데이터 분포를 가지도록 한다. 주의할 점은 **파티션 함수가 고비용**이므로 적합한 상황에서만 사용해야 한다.

- `repartition()` : 파티션 개수를 줄이거나 늘릴 때 사용
- `coalesce()` : 파티션 개수를 줄일 때 사용 (데이터 셔플을 하지 않는 특별한 repartition 함수와 같다.)
- `partitionBy()` : Disk 파티셔닝


최적의 파티션 개수는 여러번의 실험을 통해 확인해야 한다. 기본적으로 클러스터 코어 수의 2배, 즉 모든 작업자 노드의 총 코어 수의 2배로 설정하는 것이지만 데이터의 종류와 크기, Operation 함수에 따라 크게 달라진다.

리파티션 계열의 함수는 *해쉬를 기반*으로 데이터를 분배한다. 데이터 샘플이 많을수록 비교적 정확히 균등하게 분배되지만 샘플이 작을수록 간혹 잘 못하는 경우도 있다. 이 경우는 기준이 되는 새로운 칼럼을 인위적으로 생성해 정확히 균등하게 분배하도록 한다. 이를 Salting 기법이라고 한다.

### 3.2 캐싱

RDD는 동일한 프로그램에서 액션 함수가 호출될 때 마다 데이터 로드부터 처음부터 다시 계산된다. RDD를 캐싱하면 이후에 실행되는 액션 함수는 재평가 없이 재사용할 수 있다. 같은 RDD 또는 Dataframe에 반복되는 액션함수를 실행시키려면 캐싱이 유용하다. RDD는 persist, DataFrame은 cache 함수로 캐싱할 수 있다. RDD로 접근하는 persist는 스토리지 레벨에 따라 캐싱할 수 있다는 장점이 있다.

- `RDD.persist()`
- `DataFrame.cache()`

한가지 예로, 다른 조건의 filter 함수를 여러번 실행할 때 캐싱을 한다.

```python
df = df.cache()
noun_df = df.filter(F.col('pos_type') == 'NOUN')
verb_df  = df.filter(F.col('pos_type') == 'VERB')
...
df.unpersist()
```

### 3.3 브로드 캐스팅

**브로드캐스트(broadcast) 변수는 모든 작업 노드들이 접근할 수 있는 공유 변수**이다. Driver 프로세스에 있는 데이터 혹은 함수를 클러스터 전역에서 사용하는 기능이 있지만 상황에 맞게 이러한 공유변수를 잘 활용한다면 성능 이점도 살릴 수 있다.

한가지 예를 들어보자. 작은 DataFrame과 큰 DataFrame을 조인하려고 한다. 그냥 하면 비싼 셔플 연산이 필요하다. 작은 DataFrame을 브로드캐스팅하면 셔플 연산이 필요없이 조인할 수 있다. 특히 큰 DataFrame과 조인할 때 매우 효율적이다.

```python
from pysaprk.sql.functions import broadcast

big_df.join(broadcast(small_df), big_df.id == small_df.id)
```

### 3.4 기타

Spark의 힘은 데이터를 여러 노드에 분산해서 처리하는 것이다. RDD.collect() 메소드를 호출하면 분산되어있던 모든 데이터를 마스터노드(driver 프로세스)로 보내진다. 이 경우 메모리 에러가 발생할 확률이 높고 분산의 힘을 전혀 사용하지 못한다. 만약 꼭 사용해야 한다면 `take` 또는 `takeSample` 메소드를 사용하거나 필터링하여 데이터의 일부만 가져오는 것이 좋다.


