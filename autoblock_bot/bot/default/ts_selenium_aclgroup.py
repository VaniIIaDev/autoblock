# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 아이디 설정
id = "test"
password = "password"
# 변수 설정
username = "test"  # 실제 사용자 이름으로 변경
username_is_ip = False  # True 또는 False로 변경
block_time = "1년"  # "영구", "5분", "10분", "30분", "1시간", "2시간", "1일", "3일", "5일", "7일", "2주", "3주", "1개월", "3개월", "6개월", "1년" 중 하나로 변경
note = "자동으로 진행된 차단입니다. 이의가 있으시다면 차단 소명 게시판으로 문의해주세요."

# ChromeDriver 경로 설정
driver_path = "./chromedriver/chromedriver"  # 실제 경로로 변경

# Chrome 브라우저 경로 설정
chrome_path = "/opt/google/chrome/chrome"  # 실제 경로로 변경

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--remote-debugging-port=9222")

# 웹 드라이버 설정 (예: Chrome)
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

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

# /aclgroup 페이지로 이동
print("/aclgroup 페이지로 이동 중...")
driver.get("http://haneul.wiki/aclgroup")
print("/aclgroup 페이지로 이동 완료.")

# 페이지 로드 대기
print("/aclgroup 페이지 로드 대기 중...")
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='usernameInput']")))
    print("/aclgroup 페이지 로드 완료.")
except Exception as e:
    print("/aclgroup 페이지 로드 중 오류 발생:", e)

# modeSelect 선택 상자에서 값 선택
print("modeSelect 선택 상자 찾는 중...")
try:
    mode_select_box = Select(driver.find_element(By.XPATH, "//*[@id='modeSelect']"))
    if username_is_ip:
        mode_select_box.select_by_index(0)  # 첫 번째 값 선택
        print("modeSelect 첫 번째 값 선택 완료.")
    else:
        mode_select_box.select_by_index(1)  # 두 번째 값 선택
        print("modeSelect 두 번째 값 선택 완료.")
except Exception as e:
    print("modeSelect 선택 상자를 찾을 수 없습니다:", e)

# usernameInput 입력란 찾기 및 값 입력
print("usernameInput 입력란 찾는 중...")
try:
    username_input = driver.find_element(By.XPATH, "//*[@id='usernameInput']")
    username_input.send_keys(username)
    print("usernameInput 입력 완료.")
except Exception as e:
    print("usernameInput 입력란을 찾을 수 없습니다:", e)

# noteInput 입력란 찾기 및 값 입력
print("noteInput 입력란 찾는 중...")
try:
    note_input = driver.find_element(By.XPATH, "//*[@id='noteInput']")
    note_input.send_keys(note)
    print("noteInput 입력 완료.")
except Exception as e:
    print("noteInput 입력란을 찾을 수 없습니다:", e)

# block_time에 따라 select 상자에서 값 선택
if block_time != "영구":
    print("block_time 선택 상자 찾는 중...")
    try:
        select_box = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form[1]/div[3]/select"))
        if block_time == "5분":
            select_box.select_by_index(1)
        elif block_time == "10분":
            select_box.select_by_index(2)
        elif block_time == "30분":
            select_box.select_by_index(3)
        elif block_time == "1시간":
            select_box.select_by_index(4)
        elif block_time == "2시간":
            select_box.select_by_index(5)
        elif block_time == "1일":
            select_box.select_by_index(6)
        elif block_time == "3일":
            select_box.select_by_index(7)
        elif block_time == "5일":
            select_box.select_by_index(8)
        elif block_time == "7일":
            select_box.select_by_index(9)
        elif block_time == "2주":
            select_box.select_by_index(10)
        elif block_time == "3주":
            select_box.select_by_index(11)
        elif block_time == "1개월":
            select_box.select_by_index(12)
        elif block_time == "3개월":
            select_box.select_by_index(13)
        elif block_time == "6개월":
            select_box.select_by_index(14)
        elif block_time == "1년":
            select_box.select_by_index(15)
        print("block_time 선택 완료.")
    except Exception as e:
        print("block_time 선택 상자를 찾을 수 없습니다:", e)
else:
    print("block_time이 '영구'이므로 선택 상자를 선택하지 않습니다.")

# 추가 버튼 찾기 및 클릭
print("추가 버튼 찾는 중...")
try:
    add_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form[1]/div[4]/button")
    add_button.click()
    print("추가 버튼 클릭 완료.")
except Exception as e:
    print("추가 버튼을 찾을 수 없습니다:", e)

# 결과를 확인하기 위해 5초 대기
print("5초 대기 중...")
import time
time.sleep(5)

# 화면 캡처 (선택 사항)
print("화면 캡처 중...")
driver.save_screenshot("screenshot.png")
print("화면 캡처 완료. 'screenshot.png' 파일을 확인하세요.")

# 드라이버 종료
print("드라이버 종료 중...")
driver.quit()
print("드라이버 종료 완료.")
