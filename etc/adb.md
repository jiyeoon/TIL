
# ADB (Android Device Bridge)

안드로이드 디바이스와 통신?할 수 있게 해주는 도구. 

- 여러 adb 커맨드 리스트 : <https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8?fbclid=IwAR0fPFOEyVc0-JFyBu3G1OcklvxW_8b7SApvBlj7eYtBIpo3DjFJFUXMNRU>


# 유용하게 쓰일 adb 커맨드 리스트

- `adb devices` : 현재 연결된? 디바이스 리스트 출력
- `adb shell ***` : 연결된 adb 디바이스에서 유닉스 명령어를 사용할 수 있다.
    - `adb shell rm` : 삭제
    - `adb shell ls` : 해당 디렉토리 파일 및 디렉토리 리스트 출력
    - `adb shell chmod +x FILE` : 파일을 실행 가능하게 권한 변경
- `adb push FROM TO` : 컴퓨터에의 파일 FROM을 TO로 이동
- `adb shell ./...` : 파일 실행.

- 