import random

from selenium import webdriver as wb
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pyautogui


def __login__(username, password, pathA, pathB):
    pyautogui.PAUSE = 0.5  # 设置每个动作0.2s太快来不及输入密码
    options = wb.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 切换到开发者模式
    browser = wb.Chrome(options=options)
    browser.maximize_window()  # 窗口最大化保证坐标正确
    browser.get('https://taobaolive.taobao.com/room/index.htm?spm=a21bo.2017.523825.1.3e2811d9TfuKcB&feedId=234201746964')

    # try:
    #     left,top,width,height=pyautogui.locateOnScreen(pathA)
    # except:
    #     left,top,width,height=pyautogui.locateOnScreen(pathB)  # 获取login_switch位置

    a_moveToX = 860
    a_moveToY = 440
    p_moveToX = 950
    p_moveToY = 490
    l_moveToX = 960
    l_moveToY = 540
    time.sleep(1)
    pyautogui.moveTo(a_moveToX, a_moveToY)  # 移动到账户输入框
    pyautogui.click()  # 点击切换按钮
    pyautogui.typewrite(username)
    # pyautogui.press('tab')
    pyautogui.moveTo(p_moveToX, p_moveToY)  # 移动到密码输入框
    pyautogui.click()  # 点击切换按钮
    pyautogui.typewrite(password)
    errorType = 0
    try:
        left, top, width, height = pyautogui.locateOnScreen(pathA)
        print('识别滑块')
        moveToX = left + random.randint(10, 200)
        moveToY = top
        print(moveToX, moveToY)
        pyautogui.moveTo(moveToX, moveToY)
        pyautogui.mouseDown()
        moveToX = moveToX + random.randint(300,320)
        pyautogui.moveTo(moveToX, moveToY)
        pyautogui.mouseUp()
        pyautogui.moveTo(moveToX - 250, moveToY + 60)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        time.sleep(2)
        try:
            left, top, width, height = pyautogui.locateOnScreen(pathA)
            print('识别滑块')
            moveToX = left + random.randint(10,200)
            moveToY = top
            print(moveToX, moveToY)
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseDown()
            moveToX = moveToX + random.randint(300,320)
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseUp()
            pyautogui.moveTo(moveToX - 250, moveToY + 60)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            try:
                left, top, width, height = pyautogui.locateOnScreen(pathA)
                print('识别滑块')
                moveToX = left + random.randint(10, 200)
                moveToY = top
                print(moveToX, moveToY)
                pyautogui.moveTo(moveToX, moveToY)
                pyautogui.mouseDown()
                moveToX = moveToX + random.randint(300, 320)
                pyautogui.moveTo(moveToX, moveToY)
                pyautogui.mouseUp()
                pyautogui.moveTo(moveToX - 250, moveToY + 60)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                try:
                    left, top, width, height = pyautogui.locateOnScreen(pathA)
                    print('识别滑块')
                    moveToX = left + random.randint(10, 200)
                    moveToY = top
                    print(moveToX, moveToY)
                    pyautogui.moveTo(moveToX, moveToY)
                    pyautogui.mouseDown()
                    moveToX = moveToX + random.randint(300, 320)
                    pyautogui.moveTo(moveToX, moveToY)
                    pyautogui.mouseUp()
                    pyautogui.moveTo(moveToX - 250, moveToY + 60)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    try:
                        left, top, width, height = pyautogui.locateOnScreen(pathA)
                        print('识别滑块')
                        moveToX = left + random.randint(10, 200)
                        moveToY = top
                        print(moveToX, moveToY)
                        pyautogui.moveTo(moveToX, moveToY)
                        pyautogui.mouseDown()
                        moveToX = moveToX + random.randint(300, 320)
                        pyautogui.moveTo(moveToX, moveToY)
                        pyautogui.mouseUp()
                        pyautogui.moveTo(moveToX - 250, moveToY + 60)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
                    except:
                        errorType = 1  # 识别不出滑块
                except:
                    errorType = 1  # 识别不出滑块
            except:
                errorType = 1  # 识别不出滑块

        except:
            errorType = 1  # 识别不出滑块
    except:
        print('识别滑块')
        pyautogui.moveTo(l_moveToX, l_moveToY)  # 移动到切换登录的位置
        pyautogui.click()  # 点击切换按钮
        time.sleep(2)
        try:
            left, top, width, height = pyautogui.locateOnScreen(pathA)
            print('识别滑块')
            moveToX = left + random.randint(10,200)
            moveToY = top
            print(moveToX, moveToY)
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseDown()
            moveToX = moveToX + random.randint(300,320)
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseUp()
            pyautogui.moveTo(moveToX - 250, moveToY + 60)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        except:

            errorType = 1  # 识别不出滑块
    # print(errorType)
    cookie_list = []
    for item in browser.get_cookies():
        str = '{}={}'.format(item['name'],item['value'])
        cookie_list.append(str)
    cookies_str = '; '.join(cookie_list)
    return cookies_str


if __name__ == '__main__':
    browser = __login__('', '', './pic/huakuai.png', './pic/login.png')
