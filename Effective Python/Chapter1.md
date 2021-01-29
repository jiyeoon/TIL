- [Effective Python](#effective-python)
  - [Better way 1. 사용중인 파이썬 버전을 알자](#better-way-1-사용중인-파이썬-버전을-알자)
    - [Better way 2. PEP 8 스타일 가이드를 따르자](#better-way-2-pep-8-스타일-가이드를-따르자)
  - [Better way 3. bytes, str, unicod의 차이점을 알자](#better-way-3-bytes-str-unicod의-차이점을-알자)

# Effective Python


## Better way 1. 사용중인 파이썬 버전을 알자

`python --version` 명령어로 확인 가능하다.

### Better way 2. PEP 8 스타일 가이드를 따르자

> 파이썬 개선 제안서 (Phython Enhancement Proposal) #8

파이썬 코드를 어떻게 구상할지에 대한 스타일 가이드.

자세한 내용은 블로그 글 참고!

## Better way 3. bytes, str, unicod의 차이점을 알자

- python 3 : `bytes`와 `str`
    - `bytes` : raw 8비트를 저장
    - `str` : 유니코드 문자를 저장.
- python 2 : `str`과 `unicode`
    - `str` : raw 8비트 값을 저장
    - `unicode` : 유니코드 문자 저장

유니코드 문자를 바이너리 데이터로 표현하는 방법은 많다. 가장 대표적인 인고징은 UTF-8!

여기서 중요한 것은 파이썬3의 `str` 인스턴스와 파이썬2의 `unicode` 인스턴스는 연관된 바이너리 인코딩이 없다는 점이다. 유니코드 문자를 바이너리 데이터로 변환하려면 `encode` 메서드를 사용해야 한다. 바이너리 데이터를 유니코드 문자로 변환하려면 `decode` 메소드를 써야한다.


파이썬 프로그래밍을 할 때 외부에 제공할 인터페이스에서는 유니코드를 인코드하고 디코드해야한다. 문자타입이 분리되어있는 탓에 파이썬 코드에서는 일반적으로 다음 두가지 상황에 부딪힌다.

- UTF-8로 인코드 된 문자인 raw 8비트 값을 처리하려는 상황
- 인코딩이 없는 유니코드 문자를 처리해야하는 상황

이 두 경우 사이에서 변환하고 먼저 코드에서 원하ㅡㄴ 타입과 입력값의 타입이 정확하게 일치하게 하려면 헬퍼함수가 두개가 필요하다.

1. `str`이나 `bytes`를 입력으로 받고 `str`을 반환하는 메서드

```python
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value
```

2. `str`이나 `bytes`를 받고 `bytes`로 반환하는 메소드

```python
def to_bytes(bytes_or_str):
    if isinstance(bytes_for_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value
```

파이썬2에서는 아래와 같다.

```python
# python 2
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value

def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value
```

파이썬에서 raw 8비트 값과 유니코드 문자를 처리할 때의 큰 이슈에는 두가지가 있다.

1. 파이썬2에서 `str`이 7비트 아스키 문자만 포함하고 있다면 `unicode`와 `str`은 같은 타입처럼 보인다.
    - 서로 + 연산자로 묶을 수 있다.

2. 파이썬3에서 내장함수 `open`이 반환하는 파일 핸들을 사용하는 연산은 기본적으로 UTF-8 인코딩을 한다. 
    - 예를 들어 아래의 코드는 파이썬 2에서는 잘 동작하지만 파이썬 3에서는 동작하지 않는다.
    ```python
    with open('/tmp/random.bin', 'w') as f:
        f.write(os.urandom(10))
    ```
    - 그 이유는 파이썬3의 `open`에 새 `encoding` 변수가 추가되었기 때문이다. 이 파라미터의 기본값은 `'utf-8'`이다. 따라서 파일 핸들을 사용하는 `read`나 `write`연산은 바이너리 데이터를 담은 `bytes`가 아닌 유니코드 문자를 담은 `str`인스턴스를 기대한다.
    - 위의 코드를 문제없이 동작하게 하려면 문자 쓰기 모드(`'w'`)가 ㅇ닌 바이너리 쓰기 모드(`'wb'`)로 오픈해야 한다.
    ```python
    with open('/tmp/random.bin', 'wb') as f:
        f.write(os.urandom(10))
    ```


    


