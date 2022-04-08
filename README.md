# Intro
안녕하세요. 
이번 과정에서는 '중앙 서버에 log를 저장하는 이유'와 'log를 잘 저장하는 법'을 체험해보려고 합니다. 실감나는 체험을 위해서, 우리는 아래와 같은 상황에 처해있다고 상상할 겁니다! 😎
```
우리회사가 온라인으로 콘서트 굿즈를 파는 서비스를 시작한다. 
지난 몇 개월동안 열심히 개발했고 최종 QA도 마쳤고, 지난주에 배포도 되어있다. 
모든 것이 다 완벽하다.
드디어 오늘 저녁 아홉시에 BTS 콘서트가 있다! 펜들과 함께하는 우리 굿즈 서비스!! 
그런데, CTO와 팀장님들은 해외출장을 갔다ㅠㅠ그들은 비행기 안에 있다.
이제 우리끼리 오늘 오후에 서비스를 오픈해야 하는데...이제, 우리 팀 뭘 해야 하지?
```

## 미션 배경 설명
- 인기 많은 서비스는 여러대의 서버를 두고 운영합니다. 우리는 인기 많은 서비스가 될거니까, 여러대의 서버가 필요해요!
![여러대 서버예시](https://docs.oracle.com/it/solutions/design-ha/img/public-lb.png)
- 이번 미션에서 여러분의 local PC는 우리서비스의 여러대의 서버 중 하나의 서버 instance의 역할을 한다고 생각해주세요!    
(위 그림에서 VM1, VM2, VM3 이 각자의 local PC와 같은 역할이에요.)
- 제공되는 미션 repo에 있는 'mock-server.py'를 실행하면, logList에 로그들이 랜덤하게 로그파일에 생성될 것입니다.    
(cf.실제 서비스에서도 서버를 실행하면 많은 로그들이 로그파일에 쌓이기 시작합니다.)
- 우리는 이 미션에서 datadog(https://www.datadoghq.com/) 이라는 상용 중앙 로그 시스템의 도움을 받을 거에요! datadog은 log를 중앙서버에 수집해주는 고마운 친구입니다. 

## 미션 준비물
**1. python 3**
- python 버전 3이상이 필요해요!
- mac OS라면, brew를 통해 설치하는 것을 추천합니다.
- python3이 설치되어있는지 터미널에서 확인해볼까요?     
Hint : `python3 --version` 

**2. datadog agent 설치**
- mac OS  
아래 명령어를 통해 설치 
```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY={제공되는 key} DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
```
![성공결과](https://github.com/SunghyunLim/log-alarm-practice/blob/main/img/result.png)

- windows 
설치시 필요한 API key는 별도로 제공 필요
// todo windows에서도 설치만 하면, 이후 환경변수 설정시 path가 똑같을까? 확인필요.
https://docs.datadoghq.com/agent/basic_agent_usage/windows/?tab=gui

**3. DD_API_KEY**
- 강의에서 제공 예정  

**4. datadog ID, PASSWORD**
- 강의에서 제공 예정

### P.S 1 : Don't Worry!
- 이 미션을 수행하기 위해서 python 문법을 몰라도 됩니다. 걱정마세요🥳
- 이 미션을 수행하기 위해서 datadog 이 뭔지, 어떻게 사용하는지 잘 몰라도 됩니다. 걱정마세요🥳
### P.S 2 : Don't Worry!
- 이번에 알게 되었어요. terminal에서 vscode 실행하기 : https://code.visualstudio.com/docs/setup/mac 
----------
## 미션 1. 나의 local 환경에서, log를 확인하기
### step1. git clone
- 이 프로젝트를 clone 합니다.
- clone한 프로젝트가 위치한 path를 메모해두세요. 이후에 나올 미션에서 사용됩니다.
Hint! `pwd`     

### step2. 'mock-server.py'를 실행하기
- clone한 프로젝트에서 아래 명령어 실행
```
python3 mock-server.py
```
- 아래 스크린샷처럼 로그가 프린트 되면 미션 1 성공!
![성공결과](https://github.com/SunghyunLim/log-alarm-practice/blob/main/img/mock-server.png)

- 구조를 살펴보고,logList.txt에 로그를 추가해보세요. 
----
## Q. 지금 상태에서 우리 팀의 다른 서버(우리 팀원)의 로그를 함께 보려면 어떻게 해야 할까요?
----
## 미션 2. 다른 서버의 로그도 보기위해서, 로그를 중앙서버로 보냅시다. datadog의 도움을 받을 거에요.

### step1. datadog 환경변수 변경
- /opt/datadog-agent/etc/datadog.yaml파일을 찾기
- '/opt/datadog-agent/etc/datadog.yaml'파일의 835번째 라인을 찾고, 아래와 같이 변경하고 저장하기       
 ``` logs_enabled: true ```  
 
변경 전 -> 변경 후
 ``` logs_enabled: false -> logs_enabled: true ```

### step2. log에 표시될 나만의 서비스 이름 만들기
- /opt/datadog-agent/etc/conf.d/python.d 디렉토리를 생성하기
- 위에서 생성한 디렉토리에 'conf.yaml'파일을 생성해서 아래 내용을 추가하고 저장합니다.
 ```
 logs:
  - type: file
    path: {git clone한 위치}/logs/*.log
    service: {나만의 서비스 이름}
    source: python
```

'conf.yaml' Example
```
logs:
 - type: file
   path: /Users/whale/solar/log-alarm-practice/logs/*.log
   service: solar
   source: python
```

### step3. datadog-agent를 재시작 합니다.
- datadog-agent 종료
```
datadog-agent stop
```

- datadog-agent 시작
```
datadog-agent run
```
- datadog-agent가 정상적으로 시작되면, 성공!
  - datadog-agent가 실행되면, 로그파일을 중앙서버로 전송할 수 있습니다!
// todo 정상적으로 시작되었을때 스샷 추가

### step4. mock-server 실행
- python3 mock-server.py 를 실행합니다.
  - 미션1.step2를 참고하세요.
----------
## 미션3. datadog을 활용해 나의 log 확인하기
- datadog login
`https://app.datadoghq.com/account/login`

- 로그인 후, 좌측 메뉴 중 Logs > Search

- 수 많은 log중에서 나의 log만 찾아낼 수 있다면, 미션 성공!
----
## Q. 여러 로그가 섞였을 때 우리 팀의 다른 서버(우리 팀원)의 로그를 보려면 어떻게 해야 할까요?
----
## 미션4. 우리팀의 log를 확인하기
- mock-server.py, datadog agent, datadog 서버 등을 활용하여 우리 팀의 서버에서 발생하는 로그를 필터링해보세요.

<심화학습>
## 미션5. 찾기전에 알려주기
- 자, 이제 수많은 로그가 발생하고 있습니다. 여기에서 error가 1분당 10건 이상 발생하는지 어떻게 알 수 있을까요?
- 이 정보를 내가 잘 받을 수 있도록 alarm으로 한번 받아보세요.(첫 번째 성공하신 분에게는 뭔가 좋은 것을 받지 않을까요?)

----------
# datadog 삭제
이제 모든 작업을 끝냈으면 다시 처음으로 돌아가야죠.
다음의 절차에 따라 진행하세요.
```
sudo rm -rf /opt/datadog-agent
sudo rm -rf /usr/local/bin/datadog-agent
sudo rm -rf ~/.datadog-agent/** #to remove broken symlinks
launchctl remove com.datadoghq.agent
sudo rm -rf /var/log/datadog
```
