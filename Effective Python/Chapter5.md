
# Chapter 5. 병행성과 병렬성

## Better Way 36. 자식 프로세스를 관리하려면 subprocess를 사용하자

파이썬은 실전에서 단련된 자식 프로세스 실행과 관리용 라이브러리를 갖추고 있다. 따라서 명령줄 유틸리티 같은 다른 도구들을 연계하는데 아주 좋은 언어다. 기존 셸 스크립트가 시간이 지나면서 점점 복잡해지면, 자연히 파이썬 코드로 재작성하여 가독성과 유지보수성을 확보하려고 하기 마련이다.

파이썬으로 시작한 자식 프로세슨는 병렬로 실행할 수 있으므로, 파이썬을 사용하면 머신의 CPU코어를 모두 이용해 프로그램의 처리량을 극대화할 수 있다. 파이썬 자체는 CPU속도에 의존할수도 있지만 파이썬을 사용하면 CPU를 많이 사용하는 작업을 관리하고 조절하기 쉽다.


수년간 파이썬에서는  `popen`, `popen2`, `os.exec*` 를 비롯하여 서브프로세스를 실행하는 방법이 여러개 있어왔다. 요즘의 파이썬에서 자식 프로세스를 관리하는 최선이자 가장 간단한 방법은 내장 모듈 `subprocess`를 사용하는 것이다. `subprocess`는 아래와 같이 import해주면 된다.


```python
import subprocess
```

`subprocess`로 자식 프로세스를 실행하는 방법은 간단하다. 아래 코드에서는 `Popen` 생성자가 프로세스를 시작한다. `communicate` 메서드는 자식 프로세스의 출력을 읽어오고 자식 프로세스가 종료할 때 까지 대기한다.


```python
proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE
)
out, err = proc.communicate()
print(out.decode('utf-8'))

>>>
Hello from the child!
```

자식 프로세스는 부모 프로세스와 파이썬 인터프리터와는 독립적으로 실행된다. 자식 프로세스의 상태는 파이썬이 다른 작업을 하는 동안 주기적으로 폴링(polling)된다.

```python
proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None:
    print("Working...")
    # 시간이 걸리는 작업 몇개를 수행
    # ...
print("Exit status", proc.poll())

>>>
Working...
Working...
Exit status 0
```

부모에서 자식 프로세스로 떼어낸다는 것은 부모 프로세스가 자유롭게 여러 자식 프로세스를 병렬로 실행할 수 있음을 의미한다. 자식 프로세스를 떼어내려면 모든 자식 프로세스를 먼저 시작하면 된다.

```python
def run_sleep(period):
    proc = subprocess.Popen(['sleep', 'str(period)'])
    return proc

start = time()
procs = []

for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)
```

이후에는 `communicate` 메서드로 자식 프로세스들이 I/O를 마치고 종료하기를 기다리면 된다.

```python
for proc in procs:
    proc.communicate()
end = time()
print('Finished in %.3f seconds' % (end - start))

>>>
Finished in 0.017 seconds
```

파이썬 프로그램에서 파이프(pipe)를 이용해 데이터를 서브 프로세스로 보낸 다음 서브프로세스의 결과를 받아올 수도 있다. 이 방법을 이용하면 다른 프로그램을 활용하여 작업을 병렬로 수행할 수 있다. 예를 들어 어떤 데이터를 암호화하는 데 `openssl` 명령줄 도구를 사용하려 한다고 하자. 명령줄 인수와 I/O 파이프를 사용하여 자식 프로세스를 실행하는건 간단하다.

```python
def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush() # 자식 프로세스가 입력을 반드시 받게 함
    return proc
```

예제에서는 파이프로 암호화 함수에 임의의 바이트를 전달하지만 실전에서는 사용자 입력, 파일 핸들, 네트워크 소켓 등을 전달할 것이다.

```python
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)
```

자식 프로세스는 병렬로 실행되고 입력을 소비한다. 다음 코드에서는 자식 프로세스가 종료할 때 까지 대기하고 최종 결과를 받는다.

```python
for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])

>>>
b'5\xc6\xa6h\xe2\xa7q8\x01U'
b'\xc2E/\xda#C\xe2g\x016'
b'\xd5\xe8:\x0e\x01^;8\x87\xc0'
```

유닉스의 파이프처럼 한 자식 프로세스의 결과를 다른 프로세스의 입력으로 연결하여 병렬 프로세스의 체인을 생성할 수도 있다. 다음은 자식 프로세스를 시작하여 `md5` 명령줄 도구에서 입력 스트림을 소비하게 하는 함수다.

```python
def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin = input_stdin,
        stdout = subprocess.PIPE
    )
    return proc
```

> Check!

파이썬의 내장 모듈 `hashlib`는 `md5` 함수를 제공하므로 `subprocess`를 항상 이렇게 실행할 필요는 없다.

이제 데이터를 암호화하는 `openssl`  프로세스 집합과 암호화된 결과를 `md5`로 해시(hash)하는 프로세스 집합을 시작할 수 있다.

```python
input_procs = []
hash_procs = []

for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)
```

일단 자식 프로세스들이 시작하면 이들 사이의 I/O는 자동으로 일어난다. 할일은 모든 작업이 끝나고 최종 결과물이 출력되기를 기다리는 것 뿐이다.

```python
for proc in input_procs:
    proc.communicate()

for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())

>>>
b'2e343f8ffb357931445431aaa481dbca'
b'f983298f133f37caba04cc730c751d69'
b'822e99bcc50a2b4e5ef4ac09651c3460'
```

자식 프로세스가 종료되지 않거나 입력 또는 출력 파이프에서 블록될 염려가 있다면 `communicate` 메서드에 `timeout` 파라미터를 넘겨야 한다. 이렇게 하면 자식 프로세스가 일정한 시간 내에 응답하지 않을 때 예외가 일어나서 오동작하는 자식 프로세스를 종료할 기회를 얻는다.

```python
proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print("Exit status", proc.poll())

>>>
Exit status -15
```

> Reference

- 이펙티브 파이썬
- 공식 문서 : <https://docs.python.org/ko/3/library/subprocess.html>