
# Pyspark 여러가지 함수들

## 0. 데이터 프레임 안의 내용 보기

### (1) 상위 N개만 출력 - `show()`

```python
# 상위 20개만 출력
df.show()

# 상위 n개 출력
df.show(n)
```

### (2) 전체 데이터 출력 - `collect()`

```python
df.collect()
```


## 1. 특정 칼럼 선택해 출력하기 - `select()`

```python
import pyspark.sql.functions as F

# 특정 칼럼만 보기
df.select(F.col('col1'), F.col('col2'), F.col('col3')).show()
```

## 2. 정렬 - `orderBy()`

```python
df.orderBy('칼럼명', ascending=True) # default : True, 오름차순
```

## 3. 상위 n개만 커트

```python
df = df.limit(1000) # 상위 1000개 데이터로 갱신
```

## 4. 칼럼을 기준으로 그룹핑 하기 - `groupBy()`

```python
# 하나의 칼럼으로 그룹핑
df.groupBy('col1') # col1 자리에 칼럼명 입력

# 2개 이상의 칼럼으로 그룹핑
df.groupBy(['col1', 'col2'])
```

일반적으로 `sum()`, `max()`, `avg()` 등의 함수들과 같이 사용

```python
# sum
df.groupBy('col1').sum('col2')

# avg
df.groupBy('col1').avg('col2')
```

groupby 연산 후 여러가지의 연산을 한 칼럼을 리턴하고 싶다면 `agg()`화 함께 아래와 같이 사용

```python
import pyspark.sql.functions as F

df.groupBy(['col1', 'col2']).agg(
    F.sum('col3').alias('sum_of_col3'),
    F.avg('col4').alias('avg_of_col4')
)
```

groupby 연산의 결과들을 리스트 / set으로 바꾸고 싶을때에는  `collect_list()`, `collect_set()`

```python
improt pyspark.sql.functions as F
df.groupBy(['col1', 'col2']).agg(
    F.collect_list('col3').alias('list_of_col3'), # ArrayType 칼럼
    F.collect_set('col4').alias('set_of_col4') # ArrayType이나 중복 제거된 리스트
)
```


## 5. 칼럼끼리의 연산을 통해 새 칼럼 만들기 - `withColumn()`

```python
import pyspark.sql.functions as F

# 두 칼럼 더하기
df = df.withColumn('col3', F.col('col1') + F.col('col2'))

# 세 칼럼 곱하기
df = df.withColumn('col4', F.col('col1') * F.col('col2') * F.col('col3'))
```


## 6. 사용자 정의 함수 사용 - `udf()`

여러가지 칼럼을 사용해서 새로운 칼럼을 만들고 싶을때 udf와 `withColumn()` 함수와 같이 사용.

아래는 문자열 타입에서 스페이스바를 없애는 사용자 정의 함수

```python
import pyspark.sql.functions as F
from pyspark.sql.functions import udf, StringType

# 방법 1 : annotation으로 udf 명시
@udf(returnType=StringType())
def remove_whitespace_udf(s):
    return s.replace(' ', '')

# 방법 2 : 따로 함수를 udf로 선언 
def remove_whitespace(s):
    return s.replace(' ', '')

remove_whitespace_udf = F.udf(remove_whitespace, StringType())

# udf 적용 방법 - withColumn과 함께 사용
df = df.withColumn('col2', remove_whitespace(F.col('s')))
```

하나의 udf에 여러가지 칼럼을 리턴하고 싶다면 스키마와 함께 사용

```python
import pyspark.sql.functions as F
from pyspark.sql.types import *

def get_mul_add(col1, col2):
    return col1 * col2, col1 + col2

schema = StructType([
    StructField('mul', FloatType(), True),
    StructField('add', FloatType(), True)
])

get_mul_add_udf = F.udf(get_mul_add, schema)

df = df.withColumn('output', get_mul_add_udf(F.col('col1'), F.col('col2')))\
        .select(F.col('output.*'), F.col('col1'), F.col('col2')) 
```