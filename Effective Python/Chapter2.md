
- [Chapter 2. 함수](#chapter-2-함수)
  - [Better way 14. None을 반환하기보다는 예외를 일으키자](#better-way-14-none을-반환하기보다는-예외를-일으키자)
  - [Better way 15. 클로저가 변수 스코프와 상호 작용하는 방법을 알자](#better-way-15-클로저가-변수-스코프와-상호-작용하는-방법을-알자)
  - [Better way 16. 리스트를 반환하는 대신 제너레이터를 고려하자](#better-way-16-리스트를-반환하는-대신-제너레이터를-고려하자)

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

결과 리스트와 연동하는 부분이 모두 사라져서 훨씬 이해하기 쉽다. 
