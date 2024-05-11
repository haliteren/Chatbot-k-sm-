from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
import openpyxl
from time import sleep
import globalConstants as c

class Test_Chatbot:
    def setup_method(self):        
        self.driver = webdriver.Chrome()
        self.driver.get(c.login_url)
        self.driver.maximize_window()
    def teardown_method(self):
        self.driver.quit()
    def test_chatbot_icon_open(self):        
        wait = WebDriverWait(self.driver, 10)      
        iframe = wait.until(ec.presence_of_element_located((By.ID, c.iframeId)))
        self.driver.switch_to.frame(iframe)
        launcherBtn = wait.until(ec.element_to_be_clickable((By.ID, c.launcherButton)))
        sleep (5)
        launcherBtn.click()
        sleep(10)
        self.driver.switch_to.default_content()
        iframe = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,c.iframeOpen)))
        WebDriverWait(self.driver,5).until(ec.frame_to_be_available_and_switch_to_it(iframe))
        tobetoMessage = WebDriverWait(self.driver,30).until(ec.visibility_of_element_located((By.CSS_SELECTOR, c.tobetoMessage)))
        sleep (5)
        assert tobetoMessage.text == "Merhaba 👋"        
    def test_chatbot_icon_close(self):
        wait = WebDriverWait(self.driver, 10)
        self.test_chatbot_icon_open()
        sleep (5)
        self.driver.switch_to.default_content()        
        iframeMessagebox = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, c.iframeMessageBox)))
        WebDriverWait(self.driver,5).until(ec.frame_to_be_available_and_switch_to_it(iframeMessagebox ))
        miniIcon = self.driver.find_element(By.CSS_SELECTOR, c.minimizeIcon)
        miniIcon.click()
        sleep(3)
        self.driver.switch_to.default_content()
        iframe = wait.until(ec.presence_of_element_located((By.ID, c.iframeId)))
        self.driver.switch_to.frame(iframe)
        chatbotBtn = WebDriverWait(self.driver,15).until(ec.visibility_of_element_located((By.CSS_SELECTOR, c.chatbotButton)))
        checkIconclose = chatbotBtn.is_displayed()
        assert checkIconclose == True
    def test_end_chat(self):
        self.test_chatbot_icon_open()
        sleep (5)
        self.driver.switch_to.default_content()
        iframe = WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, c.iframeEndChat)))
        self.driver.switch_to.frame(iframe)
        endChatbutton = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, c.endChatButton)))
        endChatbutton.click()
        sleep(6)    
        endChatbox = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, c.endChatBox)))
        endChatbox = endChatbox.is_displayed()
        assert endChatbox == True
        yesBtn = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH, c.yesButton)))
        yesBtn.click()
        sleep(10)
        answerInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH, c.sendInput)))
        answerInput.send_keys("TOBETO'da bulunup öğrenmek güzel")
        sleep(10)
        gndr_btn = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH, c.sendButton)))
        self.driver.execute_script("arguments[0].click();", gndr_btn)
        message = self.driver.find_element(By.XPATH, c.message)
        messageAnswer =  message.text == "Geri bildiriminiz için teşekkürler!"
        print(f"Görüş Bildirimi : {messageAnswer}")        
        sleep(5)