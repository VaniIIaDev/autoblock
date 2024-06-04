# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 아이디 설정
id = "test"
password = "password"

# ChromeDriver 경로 설정
driver_path = "./chromedriver/chromedriver"  # 실제 경로로 변경

# Chrome 브라우저 경로 설정
chrome_path = "/opt/google/chrome/chrome"  # 실제 경로로 변경
print("1번째 과정 완료")

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--remote-debugging-port=9222")
print("2번째 과정 완료")

service = Service(executable_path=driver_path, log_path='./chromedriver.log')
print("3번째 과정 완료")
# 웹 드라이버 설정 (예: Chrome)
# driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
print("4번째 과정 완료")

# 웹사이트로 이동
print("웹사이트로 이동 중...")
driver.get("http://haneul.wiki/member/login")
print("웹사이트로 이동 완료.")

# 페이지 로드 대기
print("페이지 로드 대기 중...")
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form/div[1]/input")))
    print("페이지 로드 완료.")
except Exception as e:
    print("페이지 로드 중 오류 발생:", e)

# 아이디 입력란 찾기 및 값 입력
print("아이디 입력란 찾는 중...")
try:
    username_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form/div[1]/input")
    username_input.send_keys(id)
    print("아이디 입력 완료.")
except Exception as e:
    print("아이디 입력란을 찾을 수 없습니다:", e)

# 비밀번호 입력란 찾기 및 값 입력
print("비밀번호 입력란 찾는 중...")
try:
    password_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form/div[2]/input")
    password_input.send_keys(password)
    print("비밀번호 입력 완료.")
except Exception as e:
    print("비밀번호 입력란을 찾을 수 없습니다:", e)

try:
    agree_checkbox = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form/div[3]/label/input")
    agree_checkbox.click()
    print("자동 로그인 클릭 완료")
except Exception as e:
    print("agreeCheckbox를 찾을 수 없습니다:", e)

# 로그인 버튼 찾기 및 클릭
print("로그인 버튼 찾는 중...")
try:
    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form/button")
    login_button.click()
    print("로그인 버튼 클릭 완료.")
except Exception as e:
    print("로그인 버튼을 찾을 수 없습니다:", e)

# 결과를 확인하기 위해 10초 대기
print("10초 대기 중...")
import time
time.sleep(10)

# 화면 캡처 (선택 사항)
print("화면 캡처 중...")
driver.save_screenshot("screenshot.png")
print("화면 캡처 완료. 'screenshot.png' 파일을 확인하세요.")

# 드라이버 종료
print("드라이버 종료 중...")
driver.quit()
print("드라이버 종료 완료.")
