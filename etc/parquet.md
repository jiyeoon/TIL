# Parquet(파케이)란?

파케이(parquet)이란 **하둡에서** **칼럼방식**으로 저장하는 저장 포맷을 말합니다. 파케이는 프로그래밍 언어, 데이터 모델 혹은 데이터 처리 엔진과 독립적으로 엔진과 하둡 생태계에 속한 프로젝트에서 칼럼 방식으로 데이터를 효율적으로 저장하여 처리 성능을 비약적으로 향상시킬 수 있습니다.

열(Column)기반 압축을 하고있는데 이는 칼럼의 데이터가 연속된 구조로 저장되어 있다. Row 중심으로 저장되어있는 것과는 아래 사진을 보면 이해가 빠를 것 같습니다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FDQHdl%2FbtrlhCdJVC2%2FIGSg7C1kW0fg8FcEeI3PhK%2Fimg.png)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FJcDkF%2FbtrliMtDAH7%2FDfoTOoRnaFFWPiHrKgTDT1%2Fimg.png)

열을 기반으로 데이터를 처리하면 행 기반으로 압축했을때에 비해 **데이터의 압축률이 더 높고, 필요한 열의 데이터만 읽어서 처리하는 것이 가능하기 때문에 데이터 처리에 들어가는 지원을 절약**할 수 있습니다.

파케이는 하둡 에코시스템 안에서 언제든지 사용 가능한 데이터 저장 포맷으로, 스파크 SQL은 자동으로 **기존의 데이터 스키마를 유지**하는 parquet 파일의 읽기와 쓰기를 지원합니다. 유사한 파일 형식으로 ORC가 있는데요, ORC도 파케이와 마찬가지로 압축률이 높고 스키마를 가지고있으며 처리속도가 빠르지만 하이브에서만 사용할 수 있었습니다. (현재는 아님) 회사가 다르다보니 통합된 형태로 발전되지 못하고 있다가 트위터에서 Parquet을 발표하였습니다. ORC는 Hive에 최적화된 형식이고, Parquet은 스파크에 최적화된 형식이라고 보시면 좋을 것 같습니다. 

Parquet 파일을 쓸 때 모든 칼럼은 호환성을 위해 자동으로 null을 허용하도록 변경됩니다.

## 장점

-   높은 압축률. 칼럼 단위로 구성하면 데이터가 더 균일하므로 압축률이 높아진다.
-   데이터를 전체 칼럼중에서 일부 칼럼을 선택해서 가져오는 형식이므로 선택되지 않은 칼럼의 데이터에서는 I/O가 발생하지 않게된다.
-   칼럼에 동일한 데이터 타입이 저장되기 때문에 칼럼별로 적합한(데이터형에 유리한) 인코딩을 사용할 수 있다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcZbJwW%2FbtrlhDKwYTX%2FZrIE127ADLJc0FCqyqYz01%2Fimg.jpg)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcauuQF%2FbtrlbEqDJ0l%2FruUKAbKqzg4DgLq9VDaX00%2Fimg.jpg)

위는 파일 형식에 따른 IO시 메모리 사용량과 파일의 크기를 비교한 파이콘 발표 자료인데요, 비록 판다스를 기준으로 측정된 지표이긴 하나 파일을 저장할 때 CSV보다는 parquet, hdf5 등의 형식을 사용하면 시간과 메모리를 절약할 수 있습니다. 

<iframe src="https://www.youtube.com/embed/0Vm9Yi_ig58" width="860" height="484" frameborder="0" allowfullscreen="true"></iframe>

## Parquet 데이터 쓰기 & 불러오기

```python
PARQUET_FILEPATH = "sample.parquet"

# 데이터프레임의 스키마 정보를 유지하면서 parquet 파일로 저장
df.write.format('parquet').save(PARQUET_FILEPATH)
df.write.parquet(PARQUET_FILEPATH)

# parquet 데이터 불러오기
df = spark.read.parquet(PARQUET_FILEPATH)
df = spark.read.format('parquet').load(PARQUET_FILEPATH)
```

parquet 파일에는 스키마 정보가 포함되어 있습니다. 따라서 위에서 읽어온 스키마는 그대로 보존됩니다. 파케이 파일로 불러온 결과 역시 DataFrame이 됩니다.