# pygame phyics

pyame phyics

이 라이브러리를 설치하기위해선 swig 를 설치해야한다

리눅스에 경우:
$ sudo apt-get install swig

윈도우에 경우:
[https://sourceforge.net/projects/swig/files/swigwin/swigwin-3.0.2/swigwin-3.0.2.zip/download] 접속후 기다리면 자동으로 다운로드가 진행됨

C:\swigwin-3.0.2 위치에 파일 생성 
C:\swigwin-3.0.2 위치에 다운받은 파일 압축 풀고 집어넣기

윈도우 검색창에 환경변수 으로 검색후 [시스템 환경 변수 편집] 클릭
*주의* 웹 검색 결과가 뜨면 철자주의 해서 시스템 환경 변수 편집 로 검색

뜬 창에 아래부분에 환경 변수(N)... 클릭
새롭게 뜬 창에 시스템 변수(S) 부분에서 Path 두번 클릭 

또 새로운 창이 생성되면 [새로 만들기(N)] 클릭
C:\swigwin-3.0.2 입력
그리고 컴퓨터 재시작후 라이브러리 설치 진행

pip install setuptools wheel

pip install pygame_phyics