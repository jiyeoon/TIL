
- [Chapter 2. 함수](#chapter-2-함수)
  - [Better way 14. None을 반환하기보다는 예외를 일으키자](#better-way-14-none을-반환하기보다는-예외를-일으키자)
  - [Better way 15. 클로저가 변수 스코프와 상호 작용하는 방법을 알자](#better-way-15-클로저가-변수-스코프와-상호-작용하는-방법을-알자)
  - [Better way 16. 리스트를 반환하는 대신 제너레이터를 고려하자](#better-way-16-리스트를-반환하는-대신-제너레이터를-고려하자)
  - [Better Way 17. 인수를 순회할 때는 방어적으로 하자](#better-way-17-인수를-순회할-때는-방어적으로-하자)
  - [Better Way 18. 가변 위치 인수로 깔끔하게 보이게 하자](#better-way-18-가변-위치-인수로-깔끔하게-보이게-하자)
  - [Better Way 19. 키워드 인수로 선택적인 동작을 제공하자.](#better-way-19-키워드-인수로-선택적인-동작을-제공하자)
  - [Better Way 20. 동적 기본 인수를 지정하려면 None과 docstring을 사용하자](#better-way-20-동적-기본-인수를-지정하려면-none과-docstring을-사용하자)
  - [Better Way 21. 키워드 전용 인수로 명료성을 강요하자.](#better-way-21-키워드-전용-인수로-명료성을-강요하자)

---

# Chapter 2. 함수

파이썬에서 프로그래머가 사용하는 첫 번째 구성 도구는 함수다. 다른 프로그래밍 언어에서처럼 함수는 큰 프로그램을 작고 단순한 조각으로 나눌 수 있게 해준다. 함수를 사용하면 가독성이 높아지고 코드를 이해하깅 쉬워진다. 또한 재사용이나 리팩토링도 가능해진다.

파이썬에서 제공하는 함수들에는 개발자의 삶을 좀 더 편하게 해주는 다양한 부가 기능이 있다. 일부는 다른 프로그래밍 언어에서 제공하는 기능과 비슷하지만 다수는 파이썬에만 있는 기능이다. 이런 부가 기능은 함수의 목적을 더 분명하게 해준다. 또한 불필요한 요소를 제거하고 호출자의 의도를 명료하게 보여주며, 찾기 어려운 미묘한 버그를 상당 수 줄여줄 수 있다.

## Better way 14. None을 반환하기보다는 예외를 일으키자

파이썬 프로그래머들은 유틸리티 함수를 작성할 때 반환값 `None`에 특별한 의미를 부여하는 경향이 있다. 어떤 경우네는 일리 있어 보인다. 예를 들어 어떤 숫자를 다른 숫자로 나누는 헬퍼 함수를 생각해보자. 0으로 나누는 경우에는 결과가 정의되어 있지 않기 때문에 None을 반환하는 것이 자연스럽다.

```python
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return None
```

이 함수를 사용하는 코드는 반환 값을 다음과 같이 해석한다.

```python
result = divide(x, y):
if result is None:
    print("Invalid inputs")
```

그런데 분자가 0이 되면 어떤 일이 일어날까? 반환 값도 0이 되어버린다. 그러면 `if`문과 같은 조건에서 결과를 평가할 때 문제가 될 수 있다. 오류인지 알아내려고 `None`대신 `False`에 해당하는 값을 검사할 수도 있다.

```python
x, y = 0, 5
result = divide(x, y)
if not result:
    print("Invalid Inputs!")
```

이 예는 `None`에 특별한 의미가 있을 때 파이썬 코드에서 흔히 하는 실수다. 바로 이 점이 함수에서 `None`을 반환하면 오류가 일어나기 쉬운 이유다. 이런 오류가 일어날 상황을 줄이는 방법은 두 가지다.

**1. 반환 값을 두개로 나눠서 튜플에 담자**

튜플에 첫 번째 부분은 작업이 성공했는지 실패했는지를 알려준다. 두 번째 부분은 계산된 실제 결과다.

```python
def divide(a, b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None
```

이 함수를 호출하는 쪽에서 튜플을 풀어야 한다. 따라서 나눗셈의 결과만 얻을게 아니라 튜플에 들어있는 상태 부분까지 고려해야 한다.

```python
success, result = divide(x, y)
if not success:
    print("Invalid Inputs")
```

문제는 호출자가 튜플의 첫번째 부분을 쉽게 무시할 수 있다는 점이다. 이런 오류를 줄이기 위해 더 좋은 두번째 방법이 있다.

**2. 절대로 None을 반환하지 않고 호출하는 쪽에서 예외를 일으켜서 그 예외를 처리하도록 하는 것**

여기서는 호출하는 쪽에 입력값이 잘못되엇음을 알리려고 `ZeroDivisionError`를 `ValueError`로 변경했다.

```python
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError("Invalid Inputs") from e
```

이제 호출하는 쪽에서 잘못된 입력에 대한 예외를 처리해야 한다. 호출하는 쪽에서 더는 함수의 반환 값을 조건식으로 검사할 필요가 없다. 함수가 예외를 일으키지 않았다면 반환 값은 문제가 없다. 예외를 처리하는 코드도 깔끔해진다.

```python
x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print("Invalid Inputs")
else:
    print("Result : {}".format(result))
```

<br/>

## Better way 15. 클로저가 변수 스코프와 상호 작용하는 방법을 알자

숫자 리스트들을 정렬할 때 특정 그룹의 숫자들이 먼저 오도록 우선순위를 매기려고 한다고 하자. 이런 패턴은 사용자 인터페이스를 표현하거나 다른 것보다 중요한 메세지나 예외 이벤트를 먼저 보여줘야 할 때 유용하다.

이렇게 만드는 일반적인 방법은 리스트의 `sort` 메서드에 헬퍼 함수를 `key` 인수로 넘기는 것이다. 헬퍼의 반환 값은 리스트에 있는 각 아이템을 정렬하는 값으로 사용된다. 헬퍼는 주어진 아이템이 중요한 그룹에 있는지 확인하고 그에 따라 정렬 키를 다르게 할 수 있다.

```python
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)
```

이 함수는 간단한 입력값에 사용된다.

```python
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

>>>
[2, 3, 5, 6, 1, 4, 6, 8]
```

함수가 예상대로 동작하는 이유는 세가지다.

- 파이썬은 클로저(closure)를 지원한다. 클로저란 자신이 정의된 스코프에 있는 변수를 참조하는 함수다. 바로 이 점 덕분에 `helper`함수가 `sort_priority`의 `group` 임수에 접근할 수 있다.
- 함수는 파이썬에서 **일급 객체**(first-class object)다. 이 말은 함수를 직접 참조하고, 변수에 할당하고, 다른 함수의 인수로 전달하고, 표현식과 `if`문 등에서 비교할 수 있다는 의미다. 따라서 `sort` 메서드에서 클로저 함수를 `key` 인수로 받을 수 있다.
- 파이썬에는 튜플일 비교하는 특정한 규칙이 있다. 먼저 인덱스 0으로 아이템을 비교하고 그 다음으로 인덱스 1, 다음은 인덱스 2 와 같이 진행한다. `helper` 클로저의 반환 값이 정렬된 순서를 분리된 두 그룹으로 나뉘게 한 건 이 규칙 때문이다.

함수에서 우선순위가 높은 아이템을 발견했는지 여부를 반환해서 사용자 인터페이스 코드가 그에 따라 동작하게 하면 좋을 것이다. 이런 동작을 추가하는 일은 쉬워보인다. 이미 각 숫자가 어느 그룹에 포함되어 있는지 판별하는 클로저 함수가 있다. 우선순위가 높은 아이템을 발견했을 때 플래그를 뒤집는데도 클로저를 사용하는 건 어떨까? 그러면 함수는 클로저가 수정한 플래그 값을 반환할 수 있다.

다음과 같이 명확해 보이는 방식으로 코드를 수정해보았다.

```python
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            fount = True # 간단해보임
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```

앞서 사용한 것과 같은 입력으로 함수를 실행할 수 있다.

```python
found = sort_priority2(numbers, group)
print("Found : ", found)
print(numbers)

>>>
Found : False
[2, 3, 5, 7, 1, 4, 6, 8]
```

정렬된 결과는 올바르지만 `found` 결과는 다르다. `group`에 속한 아이템을 `numbers`에서 찾을 수 있었지만 함수는 `False`를 반환했다. 

표현식에서 변수를 참조할 때 파이썬 인터프리터는 참조를 해결하려고 다음과 같은 순서로 스코프(scope:유효 범위)를 탐색한다.

1. 현재 함수의 스코프
2. (현재 스코프를 담고 있는 다른 함수 같은) 감싸고 있는 스코프
3. 코드를 포함하고 있는 모듈의 스코프 (전역 스코프)
4. (`len`이나 `str` 같은 함수를 담고 있는) 내장 스코프

이 중 어느 스코프에도 참조한 이름으로 된 변수가 정의되어 있지 않으면 `NameError` 예외가 일어난다.

변수에 값을 할당할 때는 다른 방식으로 동작한다. 변수가 이미 현재 스코프에 정의되어 있다면 새로운 값을 얻는다. 파이썬은 현재 스코프에 존재하지 않으면 변수 정의로 취급한다. 새로 정의되는 변수의 스코프는 그 할당을 포함하고 있는 함수가 된다.

이 할당 동작은 `sort_priority2` 함수의 반환 값이 잘못된 이유를 설명해준다. `found` 변수는 `helper` 클로저에서 `True`로 할당된다. 클로저 할당은 `sort_priority2`에서 일어나는 할당이 아닌 `helper` 안에서 일어나는 새 변수 정의로 처리된다.

```python
def sort_priority2(numbers, group):
    found = False           # 스코프 : sort_priority2
    def helper(x):
        if x in group:
            fount = True    # 스코프 : helper ---> 안좋음!!
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```

이 문제는 버그같이 보이지만 언어 설계자가 의도한 결과다. 이 동작은 함수의 지역 변수가 자신을 포함하는 모듈을 오염시키는 문제를 막아준다. 그렇지 않았다면 함수 안세어 일어나는 모든 할당이 전역 모듈 스코프에 쓰레기를 넣는 결과로 이어졌을 것이다. 그렇게 되면 불필요한 할당에 그치지 않고 결과로 만들어지는 전역 변수들의 상호 작용으로 알기 힘든 버그가 생긴다.


**데이터 얻어오기**

파이썬3에서는 클로저에서 데이터를 얻어오는 특별한 문법이 있다. `nonlocal` 문은 특정 변수 이름에 할당할 때 스코프 탐색이 일어나야 함을 나타낸다. 유일한 제약은 `nonlocal`이 (전역 변수의 오염을 피하려고) 모듈 수준 스코프까지 탐색할 수 없다는 점이다.

다음은 `nonlocal`을 사요하여 같은 함수를 다시 정의한 예다.

```python
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        nonlocal found # 추가!! 
        if x in group:
            fount = True 
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```

`nonlocal`문은 클로저에서 데이터를 다른 스코프에 할당하는 시점을 알아보기 쉽게 해준다. `nonlocal`문은 변수 할당이 모듈 스코프에 직접 들어가게 하는 `global`문을 보완한다.

하지만 전역 변수의 안티 패턴(anti-pattern)과 마찬가지로 간단한 함수 이외에는 `nonlocal`문을 사용하지 않도록 주의해야 한다. `nonlocal`문의 부작용은 알아내기가 상당히 어렵다. 특히 `nonlocal`문과 관련 변수에 대한 할당이 멀리 떨어진 긴 힘수에서는 이애하기가 더욱 어렵다.

`nonlocal`을 사용할 때 복잡해지기 싲가하면 헬퍼 클래스로 상태를 감싸는 방법을 이용하는게 낫다. 이제 `nonlocal`을 사용할 때와 같은 결과를 얻는 클래스를 정의해보자. 코드는 약간 더 길지만 이해하기는 훨씬 쉽다. 

```python
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False
    
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True
```

**파이썬2의 스코프**

불행하게도 파이썬2는 `nonlocal` 키워드를 지원하지 않는다. 비슷한 동작을 얻으려면 파이썬의 스코프 규칙을 이용한 다른 방법이 필요하다. 그다지 깔끔한 방법은 아니지만 일반적인 파이썬 표현 방식이다.

```python
def sort_priority(numbers, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found[0]
```

앞에서 설명한대로 파이썬은 현재 값을 알아내려고 `found` 변수가 어디서 참조되었는지 상위 스코프로 탐색해나간다. 트릭은 `found`의 값이 수정 가능한(mutable) 리스트라는 점이다. 이 말은 클로저에서 일단 `found`를 받아온 후에는 내부 스코프에서 (`found[0] = True`로) `found`의 상태를 바꿔서 데이터를 보낼 수 있다는 의미다.

이 방법은 스코프를 탐색하는 데 사용되는 변수가 딕셔너리나 세트 혹은 여러분이 정의한 클래스의 인스턴스일때도 적용된다.


## Better way 16. 리스트를 반환하는 대신 제너레이터를 고려하자

일련의 결과를 생성하는 함ㅅ에서 택할 가장 간단한 방법은 아이템의 리스트를 반환하는 것이다. 예를 들어 문자열에 있는 모든 단어의 인덱스를 출력하고 싶다고 하자. 다음 코드에서는 `append` 메서드로 리스트에 결과들을 누적하고 함수가 끝낭ㄹ 때 해당 리스트를 반환한다.

```python
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index+1)
    return result
```

샘플 입력이 몇 개뿐일 때는 함수가 기대한 대로 동작한다. 하지만 위의 함수는 문제가 있다.

먼저 코드가 약간 복잡하고 깔끔해 보이지 않는다. 새로운 결과가 나올 때마다 `append` 메소드를 호출해야 한다. 메서드 호출(`result.append`)이 많아서 리스트에 추가하는 값(`index+1`)이 덜 중요해 보인다. 결과 리스트를 생성하는데 한 줄이 필요하고, 그 값을 반환하는 데도 한 줄이 필요하다.

이 함수를 작성하는 더 좋은 방법은 제너레이터를 사용하는 것이다. 제너레이터는 `yield` 표현식을 사용하는 함수다. 제너레이터 함수는 호출되면 실제로 실행되지 않고 바로 이터레이터를 반환한다. 내장 함수 `next`를 호출할 때 마다 이터레이터는 다음 `yield` 표현식으로 진행하게 된다. 제너레이터에서 `yield`에 전달한 값을 이터레이터가 호출하는 쪽에 반환한다.

다음은 앞에서 본 버전과 동일한 결과를 생성하는 제너레이터 함수다.

```python
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1
```

결과 리스트와 연동하는 부분이 모두 사라져서 훨씬 이해하기 쉽다. 결과는 리스트가 아닌 `yield` 표현식으로 전달된다. 제너레이터 호출로 반환되는 이터레이터를 내장 함수 `list`에 전달하면 손쉽게 리스트로 변환할 수 있다.

```python
result = list(index_words_iter(address))
```

`index_words`의 두 번째 문제는 반환하기 전에 모든 결과를 리스트에 저장해야 한다는 점이다. 입력이 매우 많다면 프로그램 실행 중에 메모리가 고갈되어 동작을 멈추는 원인이 된다. 반면에 제너레이터로 작성한 버전은 다양한 길이의 입력에도 쉽게 이용할 수 있다.

다음은 파일에서 입력을 한번에 한 줄씩 읽어서 한 번에 한 단어씩 출력을 내어주는 제너레이터다. 이 함수가 동작할 때 사용하는 메모리는 입력 한 줄의 최대 길이까지다.

```python
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset
```

이 제너레이터를 실행하면 앞에서 본 예제와 같은 결과가 나온다.

```python
with open('/tmp/address.txt', 'r') as f:
    it = index_file(f)
    results = islice(it, 0, 3)
    print(list(results))

>>>
[0, 5, 11]
```

그렇다.. 이런 결과가 나온다.. 

## Better Way 17. 인수를 순회할 때는 방어적으로 하자


## Better Way 18. 가변 위치 인수로 깔끔하게 보이게 하자

선택적인 위치 인수(이런 파라미터의 이름을 관례적으로 `*args`라고 해서 종종 'star args'라고도 한다.)를 받게 만들면 함수 호출을 더 명확하게 할 수 있고 보기에 방해가 되는 요소들을 없앨 수 있다.

예를 들어 디버그 정보 몇개를 로그로 남긴다고 해보자. 인수의 개수가 고정되어 있다면 메세지와 값 리스트를 받는 함수가 필요할 것이다.

```python
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('{}: {}'.format(message, values_str))

log('My numbers are : ', [1, 2])
log('Hi there', [])

>>>
My numbers are : 1, 2
Hi there
```

로그로 남길 값이 없을 때 빈 리스트로 넘겨야 한다는 것은 불편하고 성가신 일이다. 두번째 인수를 아예 남겨둔다면 더 좋을 것이다. 파이썬에서는 * 기호를 마지막 위치 파라미터 이름 앞에 붙이면 된다. 로그 메세지(`log` 함수의 `message` 인수)를 의미하는 첫 번째 파라미터는 필수지만, 다음에 나오는 위치 인수는 몇개든 선택적이다. 함수 본문은 수정할 필요가 없고 호출하는 쪽만 수정해주면 된다.

```python
def log(message, *values): # 유일하게 다른 부분
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print("{}: {}".format(message, values_str))

log('My numbers are : ', 1, 2) # 값들을 전달
log('Hi there') # 훨씬 나음

>>>
My numbers are : 1, 2
Hi there
```

리스트를 `log`같은 가변 인수 함수를 호출하는데 사용하고 싶다면 * 연산자를 쓰면 된다. 그러면 파이썬은 시퀀스에 들어있는 아이템들을 위치 인수로 전달한다.

```python
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

>>>
Favorite colors : 7, 33, 99
```

가변 개수의 위치 인수를 받는 방법에는 두 가지 문제가 있다. 

첫 번째 문제는 *(1)가변 인수가 함수에 전달되기에 앞서 항상 튜플로 변환된다*는 점이다. 이는 <u>함수를 호출하는 쪽에서 제너레이터에 * 연산자를 쓰면 제너레이터가 모두 소진될 때 까지 순회됨</u>을 의미한다. 결과로 만들어지는 튜플은 제너레이터로부터 생성된 모든 값을 담으므로 메모리를 많이 차지해 결국 프로그램이 망가지게 할 수도 있다.

```python
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)

>>>
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9) # 값을 모두 불러옴
```

`*args`를 받는 함수는 인수 리스트에 있는 입력의 수가 적당히 적다는 사실을 아는 상황에서 가장 좋은 방법이다. 이런 함수는 많은 리터럴이나 변수 이름을 한꺼번에 넘기는 함수 호출에 이상적이다. 주로 개발자들을 편하게하고 코드의 가독성을 높이려고 사용한다.

두 번째 문제는 추후에 *(2)호출 코드를 모두 변경하지 않고서는 새 위치 인수를 추가할 수 없다*는 점이다. 인수 리스트의 앞쪽에 위치 인수를 추가하면 기존의 호출 코드가 수정 없이는 이상하게 동작한다.

```python
def log(sequence, message, *values):
    if not values:
        print("{}: {}".format(sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print("{}: {}: {}".format(sequence, message, values_str))

log(1, 'Favorites', 7, 33) # 새로운 용법은 ok!
log('Favorite numbers', 7, 33) # 오래된 용법은 제대로 동작하지 않음

>>>
1: Favorties: 7, 33
Favortie numbers: 7, 33
```

이 코드의 문제는 두번째 호출이 `sequence` 인수를 받지 못했기 때문에 7을 `message`의 파라미터로 사용한다는 점이다. 이런 버그는 코드에서 예외를 일으키지 않고 계속 실행되므로 발견하기가 어렵다. 이런 문제가 생길 가능성을 완전히 없애려면 `*args`를 받는 함수를 확장할 때 **키워드 전용**(keyword-only) 인수를 사용해야 한다.

## Better Way 19. 키워드 인수로 선택적인 동작을 제공하자. 

## Better Way 20. 동적 기본 인수를 지정하려면 None과 docstring을 사용하자

키워드 인수의 기본값으로 비정적 타입을 사용해야 할 때도 있다. 예를 들어 이벤트 발생 시각까지 포함해 로킹 메세지를 출력한다고 하자. 기본적인 경우에는 함수를 호출한 시각을 메세지에 포함하려고 한다. 함수가 호출될 때 마다 기본 인수를 평가한다고 가정하고 다음과 같이 처리하려 할 것이다.

```python
def log(message, when=datetime.now()):
    print("{}: {}".format(when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!)

>>>
2021-02-24 16:54:32.184212: Hi there!
2021-02-24 16:54:32.184212: Hi again!
```
`datetime.now`는 함수를 정의할 때 딱 한번만 실행되므로 타임스탬프가 동일하게 출력된다. 기본 인수의 값은 모듈이 로드될 때 한번만 평가되며 보통 프로그램이 시작할 때 일어난다. 이 코드를 담고 있는 모듈이 로드된 후에는 기본 인수인 `datetime.now`를 다시 평가하지 않는다.

파이썬에서 결과가 기대한대로 나오게 하려면 기본값을 `None`으로 설덩하고 docstring(문서화 문자열)으로 실제 동작을 문서화 하는게 관례다. 코드에서 인수값으로 None이 나타나면 알맞은 기본값을 할당하면 된다.

```python
def log(message, when=None):
    when = datetime.now() if when is None else when
    print("{}: {}".format(when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')

>>>
2021-02-24 17:00:31.239632: Hi there!
2021-02-24 17:00:31.340415: Hi again!
```

기본 인수 값으로 `None`을 사용하는 방법은 인수가 수정 가능(mutable)할 때 특히 중요하다. 예를 들어 JSON 데이터로 인코드 된 값을 로드한다고 해보자. 데이터 디코딩이 실패하면 기본값으로 빈 딕셔너리를 반환하려고 한다. 다음과 같은 방법을 써볼 수 있다.

```python
def decode(data, default=[]):
    try:
        return json.loads(data)
    except ValueError:
        return default
```

위의 코드에서는 `datetime.now` 제와 같은 문제가 있다. 기본 인수 값은 모듈이 로드될 때 딱 한번만 평가되므로, 기본값으로 설정한 딕셔너리를 모든 `decode` 호출에서 공유한다. 이 문제는 예상치 못한 동작을 야기한다. 

```python
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo : ', foo)
print('Bar : ', bar)

>>>
Foo :  {'stuff': 5, 'meep': 1}
Bar :  {'stuff': 5, 'meep': 1}
```

아마 각각 단일 키와 값을 담은 서로 다른 딕셔너리 두 개를 예상했을 것이다. 하지만 하나를 수정하면 다른 하나도 수정되는 것처럼 보인다. 이런 문제의 원인은 `foo`와 `bar` 둘 다 기본 파라미터와 같다는 점이다. 즉, 이 둘은 같은 딕셔너리 객체다. 

```python
assert foo is bar
```

키워드 인수의 기본값을 `None`으로 설정하고 함수의 docstring에 동작을 문서화해서 이 문제를 고친다.

```python
def decode(data, default=None):
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default
```

이제 앞서 나온 테스트 코드를 실행하면 기대한 결과를 볼 수 있다.

```python
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo : ', foo)
print('Bar : ', bar)
assert foo is bar

>>>
Foo :  {'stuff': 5}
Bar :  {'meep': 1}
Traceback (most recent call last):
  File "/Users/a1101497/studystudy/main.py", line 18, in <module>
    assert foo is bar
AssertionError
```

## Better Way 21. 키워드 전용 인수로 명료성을 강요하자.

키워드로 인수를 넘기는 방법은 파이썬 함수의 강력한 기능이다. 키워드 인수의 유연성 덕분에 쓰임새가 분명한 코드를 작성할 수 있다.

예를 들어 어떤 숫자를 다른 숫자로 나눈다고 해보자. 하지만 특별한 경우를 매우 주의해야 한다. 때로는 `ZeroDivisionError` 예외를 무시하고 무한대 값을 반환하고 싶을 수 있다. 어떨 때는 `OverflowError` 예외를 무시하고 0을 반환하고 싶을 수도 있다.

```python
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisior
    except OverflowError:
        if ignore_overflow:
            return 0
		else:
			raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
		else:
			raise
```

이 함수를 사용하는 방법은 간단하다. 다음 함수 호출은 나눗셈에서 일어나는 `float` 오버플로우를 무시하고 0을 반환한다.

```python
result = safe_division(1, 10**500, True, False)
print(result)

>>>
0.0
```

다음 함수 호출은 0으로 나누면서 일어나는 오류를 무시하고 무한대 값을 반환한다.

```python
result = safe_division(1, 0, False, True)
print(result)

>>>
inf
```

문제는 예외 무시 동작을 제어하는 두 부울 인수의 위치를 혼당하기 쉽다는 점이다. 이때문에 찾기 어려운 버그가 쉬이 발생할 수 있다. 이런 코드의 가독성을 높이는 한 가지 방법은 키워드 인수를 사용하는 방법이다. 

```python
def safe_division_b(number, divisor,
                    ignore_overflow=False,
                    ignore_zero_division = False):
    #...
```

그러면 호출하는 쪽에서 키워드 인수로 특정 연산에는 기본 동작을 덮어쓰고 무시할 플래그를 지정할 수 있다.

```python
safe_division_b(1, 10**500, ignore_overflow=True)
safe_division_b(1, 0, ignore_zero_division=True)
```

문제는 이런 키워드 인수가 선택적인 동작이라서 함수를 호출하는 쪽에 키워드 인수로 의도를 명확하게 드러내라고 강요할 방법이 없다는 점이다. `safe_division_b`라는 새 함수를 정의한다고 해도 여전히 위치 인수를 사용하는 이전 방식으로 호출할 수 있다.

```python
safe_division(10, 10**500, True, False)
```
이처럼 복잡한 함수를 작성할 때는 호출하는 쪽에서 의도를 명확히 드러내도록 요구하는게 낫다. 파이썬 3에서는 키워드 전용 인수로 함수를 정의해서 의도를 명확하게 드러내도록 요구할 수 있다. 키워드 전용 인수는 키워드로만 넘길 뿐, 위치로는 절대 넘길 수 없다.

다음은 키워드 전용 인수로 `safe_division` 함수를 다시 정의한 버전이다. 인수 리스트에 있는 * 기호는 위치 인수의 끝과 키워드 전용 인수의 시작을 가리킨다.

```python
def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    # ...
```

이제 키워드 인수가 아닌 위치 인수를 상뇽하는 함수 호출 동작은 동작하지 않는다.

```python
def safe_division_c(1, 10**500, True, False)

>>>
Traceback (most recent call last):
  File "/Users/a1101497/studystudy/main.py", line 17, in <module>
    safe_division_c(1, 10**500, True, False)
TypeError: safe_division_c() takes 2 positional arguments but 4 were given
```

키워드 인수와 그 기본 값은 기대한대로 동작한다. 

