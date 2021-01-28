### Better way 1. 사용중인 파이썬 버전을 알자

`python --version` 명령어로 확인 가능하다.

### Better way 2. PEP 8 스타일 가이드를 따르자

> 파이썬 개선 제안서 (Phython Enhancement Proposal) #8

파이썬 코드를 어떻게 구상할지에 대한 스타일 가이드.

자세한 내용은 블로그 글 참고!

### Better way 3. bytes, str, unicod의 차이점을 알자

- python 3 : `bytes`와 `str`
    - `bytes` : raw 8비트를 저장
    - `str` : 유니코드 문자를 저장.
- python 2 : `str`과 `unicode`
    - `str` : raw 8비트 값을 저장
    - `unicode` : 유니코드 문자 저장

유니코드 문자를 바이너리 데이터로 표현하는 방법은 많다. 가장 대표적인 인고징은 UTF-8!

여기서 중요한 것은 파이썬3의 `str` 인스턴스와 파이썬2의 

