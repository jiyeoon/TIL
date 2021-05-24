
# Bazel이란?


[https://docs.bazel.build/versions/master/bazel-overview.html](https://docs.bazel.build/versions/master/bazel-overview.html)


-   make, maven, gradle과 같은 오픈소스 빌드 및 테스트 툴
-   바젤은 다중 플랫폼용 출력을 구축한다.
-   여러 레포지코리에 걸쳐 대규모 코드베이스를 지원한다.

## Bazel 의 장점

-   **High Level build language**
    -   추상적이고 사람이 읽을 수 있는 언어를 사용하여 프로젝트의 빌드 속성을 높은 의미 수준에서 설명한다
    -   library, binary, script, dataset의 개념으로 작동하여 compiler와 linker같은 도구에 개별 호출의 복잡성에서 자유롭다.
-   **Fast and Reliable**
    -   이전에 수행한 모든 작업을 캐시하고 파일 콘텐츠 및 빌드 명령의 변경 사항을 추적한다.
    -   이런식으로 bazel은 재구축해야하는 시기를 알고 재구축을 한다.
    -   빌드 속도를 높이기 위해 고도로 병렬화되고 증분된 방식으로 프로젝트를 설정할 수 있다.
-   **Multi platform**
    -   Linux, macOS, 윈도우에서 실행 가능하다.
    -   동일한 프로젝트에서 데스크톱, 서버 및 모바일을 포함한 여러 플랫폼 용 바이너리 및 배포 가능한 패키지를 빌드할 수 있다.
-   **Bazel scales**
    -   10만개 이상의 소스 파일로 빌드를 처리하면서 빠른 속도를 유지한다. 수만개의 여러 저장소 및 사용자 기반에서 작동한다.
-   **Extensible**
    -   확장 가능성. 많은 언어가 지원되며 다른 언어 또는 프레임워크를 지원하도록 확장할 수 있다.

## Bazel 사용 방법

bazel을 사용하여 프로젝트를 빌드하거나 테스트하려면 아래와 같은 방법을 따르면 된다.

1.  **set up Bazel**
    1.  bazel을 다운로드하고 설치한다.
2.  **Set up a project**
    1.  bazel이 빌드 입력 및 BUILD 파일을 찾고 빌드 출력을 저장하는 디렉토리 인 프로젝트 작업 공간을 설정한다.
3.  **Write a `BUILD` file**
    1.  바젤이 어떻게 빌드하고 무엇을 빌드하는지 알려주는 파일이다.
    2.  `BUILD` 파일을 작성하는데, domain-specific한 언어인 Starlark를 이용하여 빌드 대상을 선언하여 build 파일을 작성한다.
    3.  빌드 대상은 Bazel이 빌드할 입력 아티팩트와 해당 종속성, bazel이 빌드에 사용할 빌드 규칙 및 규칙을 구성하는 옵션을 지정한다.
    4.  빌드 규칙은 bazel이 사용할 빌드 도구(예. 컴파일러 및 링커, configurations)를 지정한다.
    5.  bazel이 지원되는 플랫폼에서 가장 일반적인 artifact 유형을 다루는 빌드 규칙과 함께 제공된다.
4.  **Run Bazel**
    1.  커맨드라인툴로 bazel을 실행시킨다. bazel은 workspace 작업공간 내에 출력을 배치한다.

## Bazel 빌드 프로세스

빌드 또는 테스트를 실행할 때 bazel은 아래와 같은 프로세스로 실행됩니다.

1.  `BUILD` 파일 대상과 관련된 파일을 로드합니다.
2.  입력 및 해당 종속성을 분석하고 지정된 빌드 규칙을 적용하여 작업 그래프를 생성합니다.
3.  최종 빌드 출력이 생성될 때 까지 입력에 대한 빌드 작업을 실행합니다.

모든 이전 빌드 작업이 캐시되므로 bazel은 캐시 된 아티팩트를 식별 및 재사용하고 변경된 사항만 다시 빌드하거나 다시 테스트할 수 있습니다.