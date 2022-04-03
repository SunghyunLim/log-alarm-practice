# 설명
안녕하세요. 이번 과정에서는 중앙 서버에 log 파일을 저장하는 이유와 잘 저장하는 법을 설명하려 합니다.

## 배경소개
이번 실습에서 여러분의 local PC는 하나의 instance의 역할을 하면서 실행중 로그를 생성할 것 입니다.
그리고, 이 로그 파일은 datadog(https://www.datadoghq.com/)이라는 상용 중앙 로그 시스템을 통해 수집하게 됩니다.

## 준비물
1. python3
 - mock-server.py는 python3 기반으로 동작하게 됩니다.
2. git clone
 - 이 프로젝트를 clone 합니다.
3. datadog agent 설치(https://docs.datadoghq.com/agent/ 참조)
 - mac의 경우 다음의 명령어를 통해 설치하세요.
 DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<<key>> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
4. 환경변수 변경
 - /opt/datadog-agent/etc/conf.d/datadog.yaml파일을 찾아서 다음의 내용을 추가 합니다.
   . 835 라인을 찾아 logs_enabled: false => logs_enabled: true 로 변경하고 저장
 - /opt/datadog-agent/etc/conf.d/python.d 디렉토리를 생성 후 conf.yaml에 다음 내용을 넣고 저장합니다.
 
 logs:
  - type: file
    path: <<clone한 위치>>/logs/*.log
    service: <<자신의 서비스 이름>>
    source: python

5. Datadog agent를 재시작 합니다.

## 실행
python3 mock-server.py 를 실행합니다.
이 결과가 브라우저에서 보이면 정상입니다.