- [Effective Python](#effective-python)
  - [Better way 1. 사용중인 파이썬 버전을 알자](#better-way-1-사용중인-파이썬-버전을-알자)
  - [Better way 2. PEP 8 스타일 가이드를 따르자](#better-way-2-pep-8-스타일-가이드를-따르자)
  - [Better way 3. bytes, str, unicod의 차이점을 알자](#better-way-3-bytes-str-unicod의-차이점을-알자)
  - [Better Way 4. 복잡한 표현식 대신 헬퍼 함수를 쓰자.](#better-way-4-복잡한-표현식-대신-헬퍼-함수를-쓰자)
  - [Better Way 5. 시퀀스를 슬라이스 하는 방법을 알자.](#better-way-5-시퀀스를-슬라이스-하는-방법을-알자)
  - [Better way 6. 한 슬라이스에 start, end, stride를 함께 쓰지 말자](#better-way-6-한-슬라이스에-start-end-stride를-함께-쓰지-말자)
  - [Better way 7. map과 filter 대신 리스트 컴프리헨션을 사용하자.](#better-way-7-map과-filter-대신-리스트-컴프리헨션을-사용하자)
  - [Better way 8. 리스트 컴프리헨션에서 표현식을 두개 넘게 쓰지 말자](#better-way-8-리스트-컴프리헨션에서-표현식을-두개-넘게-쓰지-말자)
  - [Better way 9. 컴프리헨션이 클 때는 제너레이터 표현식을 고려하자.](#better-way-9-컴프리헨션이-클-때는-제너레이터-표현식을-고려하자)
  - [Better way 10. range보다는 enumerate를 사용하자](#better-way-10-range보다는-enumerate를-사용하자)

# Effective Python


## Better way 1. 사용중인 파이썬 버전을 알자

`python --version` 명령어로 확인 가능하다.

## Better way 2. PEP 8 스타일 가이드를 따르자

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
    - 위의 코드를 문제없이 동작하게 하려면 문자 쓰기 모드(`'w'`)가 아닌 바이너리 쓰기 모드(`'wb'`)로 오픈해야 한다.
    ```python
    with open('/tmp/random.bin', 'wb') as f:
        f.write(os.urandom(10))
    ```
    - 데이터를 읽을때도 마찬가지다. 파일을 오픈할 때 `'r'`이 아닌 `'rb'`를 사용하여 오픈하자.


## Better Way 4. 복잡한 표현식 대신 헬퍼 함수를 쓰자.

파이썬의 간결한 문법을 이용하면 많은 로직을 표현식 한줄로 쉽게 작성할 수 있다.

```python
green = my_values.get('green', [''])
if green[0]:
    green = int(green[0])
else:
    green = 0
```

위 로직을 펼쳐서 보면 훨씬 복잡해보인다. 이런 로직을 반복해서 사용해야한다면 헬퍼 함수를 만드는 것이 좋다.

```python
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found
```

위의 핼퍼 함수를 쓰면 `or`를 사용한 복잡한 표현식이나 `if/else` 조건식을 사요한 두줄짜리 버전을 쓸 때 보다 호출 코드가 훨씬 더 명확해진다.

```python
green = get_first_int(my_values, 'green')
```

표현식이 복잡해지기 시작하면 최대한 빨리 해당 표현식을 작은 조각으로 분할하고 로직을 헬퍼 함수로 옮기는 방안을 고려해야 한다. ***무조건 짧은 코드를 만들기 보다는 가독성을 선택하는 편이 낫다.*** 이렇게 이해하기 어려운 복잡한 표현식에는 파이썬의 함축적인 문법을 사용하면 안된다. 

## Better Way 5. 시퀀스를 슬라이스 하는 방법을 알자.

파이썬은 시퀀스를 슬라이스해서 조각으로 만드는 문법을 제공한다. 이렇게 슬라이스하면 최소한의 노력으로 시퀀스 아이템의 부분 집합에 접근할 수 있다. 가장 간단한 슬라이싱 대상은 내장 타입인 `list`, `str`, `bytes`이다. `__getitem__`과 `__setitem__`이라는 특별한 메서드를 구현하는 파이썬 클래스에서도 슬라이싱을 적용할 수 있다. 

- 슬라이싱 문법의 기본 형태는 `somelist[start:end]`이며, 여기서 `start`인덱스는 포함되고 `end`인덱스는 제외된다.
- 슬라이싱은 `start`와 `end`인덱스가 리스트의 경계를 벗어나도 적절하게 처리를 한다. 덕분에 입력 시퀀스에 대응해 처리할 최대 길이를 코드로 쉽게 수정할 수 있다. 
- 슬라이싱의 결과는 완전히 새로운 리스트다. 
    ```python
    >>> a = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> b = a[4:]
    >>> b[1] = 99
    >>> print(a)
    ['a', 'b', 'c', 'd', 'e', 'f']
    >>> print(b)
    ['e', 99]
    ```
할당에 사용하면 슬라이스는 원본 리스트에서 지정한 범위를 대체한다. `a, b = c[:2]` 같은 튜플 할당과 달리 슬라이스 할당의 길이는 달라도 된다. 할당받은 슬라이스의 앞뒤 값은 유지된다. 리스트는 새로 들어온 값에 맞춰 늘어나거나 줄어든다.

```python
>>> print("Before ", a)
Before  ['a', 'b', 'c', 'd', 'e', 'f']
>>> a[2:7] = [99, 22, 17]
>>> print("After ", a)
After  ['a', 'b', 99, 22, 17]
```

시작의 끝 인덱스를 모두 생략하고 슬라이스하면 원본 리스트의 복사본을 얻는다.

```python
>>> b = a[:]
>>> b==a and b is not a
True
```

## Better way 6. 한 슬라이스에 start, end, stride를 함께 쓰지 말자

파이썬에는 기본 슬라이싱뿐만 아니라 `somelist[start:end:stride]`처럼 슬라이스의 스트라이드를 설정하는 특별한 문법도 있다. 이 문법을 사용하면 시퀀스를 슬라이스 할 때 n번째 아이템을 가져올 수 있다.

```python
>>> a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
>>> odds = a[::2]
>>> evens = a[1::2]
>>> print(odds)
['red', 'yellow', 'blue']
>>> print(evens)
['orange', 'green', 'purple']
```

문제는 `stride` 문법이 종종 예상치 못한 동작을 해서 버그를 만들어내기도 한다는 점이다. 예를 들어 파이썬에서 바이트 문자열을 역순으로 만드는 일반적인 방법은 스트라이드 -1로 문자열을 슬라이스 하는 것이다.

```python
>>> x = b'mongoose'
>>> y = x[::-1]
>>> print(y)
b'esoognom'
```

위 코드는 바이트 문자열이나 아스키 문자에서는 잘 동작하지만, utf-8 바이트 문자열로 된 유니코드 문자에는 원하는대로 동작하지 않는다.

```python
>>> w = '지연'
>>> x = w.endoce('utf-8')
>>> y = x[::-1]
>>> z = y.decode('utf-8')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb0 in position 0: invalid start byte
```

그리고 -1을 제외한 음수값으로 스트라이드를 지정하는 것은 매우 혼란스러울 수 있다. 대괄호 안에 숫자가 세개나 있으면 빽빽해서 읽기 어렵다. 그래서 `start`와 `end`인덱스가 `stride`와 연계되어 어떤 작용을 하는지 분명하지 않다. 특히 `stride`가 음수인 경우에는 더욱 그러하다.

이런 문제를 방지하려면 `stride`를 `start`, `end`인덱스와 함께 사용하지 말아야 한다. `stride`를 사용해야한다면 양수값을 사용하고 `start`와 `end` 인덱스를 생략하는 것이 좋다. 굳이 둘다 사용해야한다면 stride를 적용한 결과를 변수에 할당하고, 이 변수를 슬라이스 한 결과를 다른 변수에 할당해서 사용하자.

```python
b = a[::2]
c = b[1:-1]
```

슬라이싱부터 하고 스트라이딩을 하면 데이터의 얕은 복사본이 추가로 생긴다. 첫 번째 연산은 결과로 나오는 슬라이스의 크기를 최대한으로 줄여야 한다. 프로그램에서 두 과정에 필요한 시간과 메모리가 중분하지 않는다면 내장 모듈 `itertools`의 `islice` 메서드를 사용해보자. 


## Better way 7. map과 filter 대신 리스트 컴프리헨션을 사용하자.

파이썬에는 한 리스트에서 다른 리스트를 만들어내는 간결한 문법이 있다. 이 문법을 사용한 표현식을 리스트 컴프리헨션(list comprehension; 리스트 함축표현식)
이라고 한다. 예를들어 아래과 같다.

```python
squares = [x**2 for x in range(1, 10)]
```

인수가 하나뿐인 함수를 적용해야하는 상황이 아니면, 간다한 연산에는 리스트 컴프리헨션이 내장함수 `map`보다 명확하다. `map`을 쓰려면 계산에 필요한 lambda 함수를 생성해야해서 깔끔해보이지 않는다.

```python
squares = map(lambda x: x**2, a)
```

`map`과 달리 리스트 컴프리헨션을 사용하면 입력 리스트에 있는 아이템을 간편하게 걸러내서 그에 대응하는 출력을 결과에서 삭제할 수 있다. 예를 들어 2로 나누어떨어지는 숫자의 제곱만 계산한다고 하자. 다음 예에서는 루프 뒤에 조건식을 추가해서 계산을 수행한다.

```python
even_squares = [x**2 for x in a if x%2 == 0]
```

내장함수 `filter`와 `map`을 사용해서 같은 결과를 얻을 수 있지만 훨씬 읽기 어렵다.

```python
alt = map(lambda x : x**2, filter(lambda x : x % 2 == 0, a))
```

이러한 이유로 리스트 컴프리헨션을 써주는 것이 좋다!

## Better way 8. 리스트 컴프리헨션에서 표현식을 두개 넘게 쓰지 말자

## Better way 9. 컴프리헨션이 클 때는 제너레이터 표현식을 고려하자.

리스트 컴프리헨션의 문제점은 입력 시퀀스에 있는 각 값별로 아이템을 하나씩 담은 새 리스트를 통째로 생성한다는 점이다. 입력이 적을때는 괜찮지만 클 때는 메모리를 많이 소모해서 프로그램을 망가뜨리는 원인이 되기도 한다.

파이썬은 이 문제를 해결하려고 리스트 컴프리헨션과 제너레이터를 일반화한 **제너레이터 표현식**을 제공한다. 제너레이터 표현식은 실행될 때 출력 시퀀스를 모두 구체화(여기서는 메모리에 로딩)하지 않는다. 대신에 표현식에서 한번에 한 아이템을 내주는 이터레이터로 평가된다. 

제너레이터 표현식은 `()` 문자 사이에 리스트 컴프리헨션과 비슷한 문법을 사용하여 생성한다. 다음은 이전 코드와 동일한 기능을 제너레이터 표현식으로 작성한 예다. 하지만 제너레이터 표현식은 즉시 이터레이터로 평가되므로 더는 진행되지 않는다.

```python
it = (len(x) for x in open('/tmp/my_file.txt'))
print(it)

>>>
<generator object <genexpr> at 0x101b81480>
```

필요할 때 제너레이터 표현식에서 다음 출력을 생성하려면 내장함수 `next`로 반환받은 이터레이터를 한번에 전진시키면 된다. 코드에서는 메모리 사용량을 걱정하지 않고 제너레이터 표현식을 사용하면 된다.

```python
print(next(it))
print(next(it))

>>>
100
57
```

제너레이터 표현식의 또 다른 강력한 결과는 다른 제너레이터 표현식과 함께 사용할 수 있다는 점이다. 다음은 앞의 제너레이터 표현식이 반환한 이터레이터를 다른 제너레이터 표현식의 입력으로 사용한 예다.

```python
roots = ((x, x**0.5) for x in it)
```

이 이터레이터를 전진시킬 때 마다 루프의 도미노 효과로 내부 이터레이터도 전진시키고 조건 표현식을 계산해서 입력과 출력을 처리한다.

```python
print(next(roots))

>>>
(15, 3.872983346207417)
```

이처럼 제너레이터를 연결하면 파이썬에서 매우 빠르게 실행할 수 있다. 큰 입력 스트림에 동작하는 기능을 결합하는 방법을 찾을 때는 제너레이터 표현식이 최선의 도구다. 단, 제너레이터 표현식이 반환한 이터레이터에는 상태가 있으므로 이터레이터를 한번 넘게 사용하지 않도록 주의해야 한다.

## Better way 10. range보다는 enumerate를 사용하자

내장함수 range는 정수집합을 순회하는 루프를 실행할 대 유용하다.

문자열의 리스트같은 순회할 자료가 있을 때는 직접 루프를 실행할 수 있다.

```python
for element in lst:
    ...
```

종종 리스트를 순회하거나 리스트의 현제 아이템의 인덱스를 알고싶은 경우가 있다. 이 경우 사용하기 좋은 것이 `enumerate` 함수이다. `enumerate`는 지연 제너레이터(lazy generator)로 이터레이터를 감싼다. 이 제너레이터는 이터레이터에서 루프 인덱스와 다음 값을 한 쌍으로 가져와 넘겨준다. `enumerate`로 작성한 코드는 훨씬 이해하기 쉽다.

```python
for i, flavor in enumerate(flavor_list):
    print("{} : {}".format(i+1, flavor))

>>>
1 : vanilla
2 : chocolate
3 : pecan
4 : strawberry
```

`enumerate`로 세기 시작할 숫자를 지정하면 코드를 더 짧게 만들 수 있다. 

```python
for i, flavor in enumerate(flavor_list, 1):
    print("{} : {}".format(i, flavor))
```
