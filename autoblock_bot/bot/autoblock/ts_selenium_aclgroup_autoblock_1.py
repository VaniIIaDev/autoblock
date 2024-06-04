# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# 변수 설정
keyword = "사퇴하세요"
username_is_ip = False  # True 또는 False로 변경
block_time = "1년"  # "영구", "5분", "10분", "30분", "1시간", "2시간", "1일", "3일", "5일", "7일", "2주", "3주", "1개월", "3개월", "6개월", "1년" 중 하나로 변경
note = "자동으로 진행된 차단입니다. 이의가 있으시다면 차단 소명 게시판으로 문의해주세요."
blocked_users = {}  # {사용자명: [차단된 문서들]} 형태로 저장

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

def check_sidebar():
    driver.get("http://haneul.wiki/sidebar.json")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
    page_source = driver.find_element(By.TAG_NAME, "pre").text
    
    try:
        sidebar_data = json.loads(page_source)
    except json.JSONDecodeError as e:
        print("JSON 디코드 오류:", e)
        return None

    for item in sidebar_data:
        if keyword in item["document"]:
            return item["document"]
    return None

def get_creator(document):
    driver.get("http://haneul.wiki/RecentChanges?logtype=create")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "c0O2TLGQ")))
    
    try:
        creator_element = driver.find_element(By.XPATH, "//div[@class='c0O2TLGQ']/strong/a")
        return creator_element.text
    except Exception as e:
        print(f"창작자를 찾을 수 없습니다: {e}")
        return None

def block_user(username):
    driver.get("http://haneul.wiki/aclgroup")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='usernameInput']")))

    # modeSelect 선택 상자에서 값 선택
    try:
        mode_select_box = Select(driver.find_element(By.XPATH, "//*[@id='modeSelect']"))
        if username_is_ip:
            mode_select_box.select_by_index(0)  # 첫 번째 값 선택
        else:
            mode_select_box.select_by_index(1)  # 두 번째 값 선택
    except Exception as e:
        print("modeSelect 선택 상자를 찾을 수 없습니다:", e)

    # usernameInput 입력란 찾기 및 값 입력
    try:
        username_input = driver.find_element(By.XPATH, "//*[@id='usernameInput']")
        username_input.send_keys(username)
    except Exception as e:
        print("usernameInput 입력란을 찾을 수 없습니다:", e)

    # noteInput 입력란 찾기 및 값 입력
    try:
        note_input = driver.find_element(By.XPATH, "//*[@id='noteInput']")
        note_input.send_keys(note)
    except Exception as e:
        print("noteInput 입력란을 찾을 수 없습니다:", e)

    # block_time에 따라 select 상자에서 값 선택
    if block_time != "영구":
        try:
            select_box = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form[1]/div[3]/select"))
            block_time_dict = {
                "5분": 1,
                "10분": 2,
                "30분": 3,
                "1시간": 4,
                "2시간": 5,
                "1일": 6,
                "3일": 7,
                "5일": 8,
                "7일": 9,
                "2주": 10,
                "3주": 11,
                "1개월": 12,
                "3개월": 13,
                "6개월": 14,
                "1년": 15
            }
            select_box.select_by_index(block_time_dict[block_time])
        except Exception as e:
            print("block_time 선택 상자를 찾을 수 없습니다:", e)

    # 추가 버튼 찾기 및 클릭
    try:
        add_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/form[1]/div[4]/button")
        add_button.click()
        print(username + " 차단 완료")
    except Exception as e:
        print("추가 버튼을 찾을 수 없습니다:", e)

    # 결과를 확인하기 위해 5초 대기
    time.sleep(5)

    # 화면 캡처 (선택 사항)
    driver.save_screenshot("screenshot.png")
    print("찰칵")

while True:
    document = check_sidebar()
    if document:
        username = get_creator(document)
        if username and username not in blocked_users:
            blocked_users[username] = []
        if username and document not in blocked_users[username]:
            block_user(username)
            blocked_users[username].append(document)
    time.sleep(10)
