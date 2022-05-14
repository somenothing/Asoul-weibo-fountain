import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options, executable_path="chromedriver/chromedriver.exe")
driver.get("https://weibo.com/p/10080861838dd4bdf01b1414e70089ca10d776/super_index")


def login():
    # login button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[3]/div[2]/ul/li[3]/a'))
    )
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[3]/div[2]/ul/li[3]/a').click()
    # switch to QRcode
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[node-type="qrcode_tab"]'))
    )
    driver.find_element(By.CSS_SELECTOR, 'a[node-type="qrcode_tab"]').click()
    # wait for login
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[onclick="window.location.reload(true);"]'))
    )
    driver.find_element(By.CSS_SELECTOR, 'a[onclick="window.location.reload(true);"]').click()


def get_sentence():
    respond = requests.request('get', 'https://api.dogcraft.top/api/d').json()
    result = "#阳光信用# %s" % respond['cnt']['c']
    return result


def aid():
    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[node-type="feed_list"]'))
    )
    index = 0
    while True:
        if index > 10:
            driver.refresh()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[node-type="feed_list"]'))
            )
            continue
        t = driver.find_elements(By.CSS_SELECTOR, 'div[node-type="feed_list_content"]')[index].text
        print(index, '|', t.replace('\n', ' '))
        if '救' not in t and '奶' not in t and '治疗' not in t:
            index += 1
            continue
        if driver.find_elements(By.CSS_SELECTOR, 'span[node-type="like_status"]')[index].get_attribute(
                'class') == ' UI_ani_praised':
            index += 1
            continue
        else:
            break
    driver.find_elements(By.CSS_SELECTOR, 'span[node-type="like_status"]')[index].click()
    time.sleep(2)
    driver.find_elements(By.CSS_SELECTOR, 'span[node-type="comment_btn_text"]>span')[index].click()
    content = get_sentence()
    print('ready to comment: ', content)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'W_input'))
    )
    driver.find_element(By.CSS_SELECTOR, 'textarea[action-type="check"]').clear()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'textarea[action-type="check"]').send_keys(content)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'a[node-type = "btnText"]').click()
    time.sleep(1)
    return True


if __name__ == '__main__':
    login()
    while True:
        try:
            aid()
        except BaseException as e:
            print('failed:', e)
        finally:
            print('completed at %s', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('input Ctrl+C to quit')
        time.sleep(45)
