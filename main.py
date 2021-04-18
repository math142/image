from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pyautogui
import mysql.connector as connector
import paperclip


def main():
    driver = configuration()
    mycursor = connexion_bd()
    info = extract_information(mycursor)
    recherche(driver,info)
    #click_save()
def configuration():
    path = "/usr/lib/chromium-browser/chromedriver"
    driver = webdriver.Chrome(path)
    driver.get("https://www.google.com/imghp?hl=xx-elmer")
    return driver
def connexion_bd():
    config ={
        "host":"localhost",
        "user":"fernweh",
        "password":"clem02069008",
        "database":"kino"}
    c = connector.connect(**config)

    return c
def extract_information(mycursor):
    info = []

    sql = """select Titel from folge"""
    cur = mycursor.cursor()
    cur.execute("select Titel from folge")
    titre = cur.fetchall()
    for x in titre:
        info.append(x)
    return info



def recherche(driver,info):
    for x in range(len(info)):
        actionChain = ActionChains(driver)
        try:
            search = driver.find_element_by_class_name('gLFyf')
            buffer = info[x][0].replace(" ", "")
            motcle = u"tatort"+ " "  + " " "dvd"+ buffer

            search.send_keys(motcle)
            search.send_keys(Keys.RETURN)


            result = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="islrg"]')))
            element = result.find_element_by_class_name('isv-r')
            actionChain.move_to_element(element).context_click().perform()
            time.sleep(1)
            click_save(motcle, driver)
            driver.back()
        except TimeoutException:
            driver.back()
        except NoSuchElementException:
            driver.back()

        except:
            driver.back()








def click_save(motcle,driver):
    for x in range(7):
        pyautogui.press("down")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("backspace")
    new_motcle = replacement(motcle)
    pyautogui.typewrite(new_motcle)
    pyautogui.press("enter")
    time.sleep(2)
    #element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//div[@class="isv-r"]')))
def replacement(motcle):
    if 'ä' in motcle:
        motcle.replace('ä','ae')
    if 'ö' in motcle:
        motcle.replace('ö','oe')
    if 'ü' in motcle:
        motcle.replace('ü','ue')
    if 'ß' in motcle:
        motcle.replace('ß','ss')
    return motcle
if __name__ == '__main__':

    main()