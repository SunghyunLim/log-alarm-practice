import threading, time, random, logging

# 로그 생성 및 출력기준 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(levelname)s - %(message)s')

# log 콘솔 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('logs/mock-server202204.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 랜덤으로 사용할 로그레벨 관리
loglevelList=[
    logging.INFO, logging.WARN, logging.ERROR
]

# 랜덤으로 사용할 로그 텍스트 관리
with open('logList.txt') as f:
    logmsgList = f.readlines()

# 2초에 한 번 로그를 남기는 함수
def print_log():
    logger.log(random.choice(loglevelList), random.choice(logmsgList).strip())
    threading.Timer(2, print_log).start()

# 실행
print_log()