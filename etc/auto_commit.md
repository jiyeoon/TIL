# 자동으로 깃허브에 커밋하는걸 만들 것이다.... 

## Step 1. watch 설치하기

```bash
brew install watch
```

watch를 설치해준다. watch는 모니터링 툴인데 지정된 시간마다 실행하고싶은 명령어를 실행하여 로그로 남겨준다.

## Step 2. 쉘 스크립트 생성

```bash
#!/bin/zsh

watch -n 43200 -g -d git status

m = "$(git status --short)"
# ./auto-test-push.sh $m

message = "auto commit and push"
git add .
git commit -am "$message"
git push
```
