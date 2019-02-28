
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#地址
URL = 'https://piao.damai.cn/139562.html?spm=a2oeg.search_category.0.0.1d9b6a63yNjM4q&clicktitle=2019%E5%BE%B7%E4%BA%91%E7%A4%BE%E5%8C%97%E4%BA%AC%E7%9B%B8%E5%A3%B0%E5%A4%A7%E4%BC%9A%E2%80%94%E2%80%94%E5%A4%A9%E6%A1%A5%E5%BE%B7%E4%BA%91%E7%A4%BE%E5%89%A7%E5%9C%BA'#手机页面
# 预估会出现的日期
KeyWord = "03-08"

driver = webdriver.Chrome()
# 设置等待时间
wait = WebDriverWait(driver, 5)
driver.get(URL)

def choose(seletor, by=By.XPATH, type=1):
    try:
        # 控件可点击时才选定
        if type == 1:
            choice = wait.until(EC.element_to_be_clickable((by, seletor)))
        else:
            choice = wait.until(driver.find_elements((by, seletor)))
        return choice
    except TimeoutException as e:
        print("Time out!")
        return None
    except Exception:
        print("Not found!")
        return None

def check():
    print("Start!!!")
    flag = 1
    while flag:
        ccbtn = None
        while None == ccbtn:
            ccbtn = choose('lst', By.CLASS_NAME)
            # print(ccbtn.text)
            if ccbtn.text.find(KeyWord) !=  -1:
                # Alert(driver).accept()
                flag = 0
                # 将焦点切换到当前页面弹出的警告，并获取弹出框的text
                confirmbtn = None
                if None == confirmbtn:
                    confirmbtn = choose("选座购买", By.LINK_TEXT)
                    confirmbtn.click()
                print("finsh!!!!")
            else:
                print("fresh")
                driver.refresh()
        print("-------------")

if __name__ == '__main__':
    check()