"""
But:Programme ayant pour but de prendre tous les titres des épisodes qui sont dans ma base de données et de chercher une
photo correspondante.

Auteur:Mathieu Cléroux
"""

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

def configuration():
    """
    Permet de faire la configuration nécessaire pour faire le scrapping
    :return: driver
    """

    path = "/usr/lib/chromium-browser/chromedriver"
    driver = webdriver.Chrome(path)
    driver.get("https://www.google.com/imghp?hl=xx-elmer")
    return driver
def connexion_bd():
    """
    Établit la connexion avec la base de donnée
    :return: accès à la base de donnée
    """
    config ={
        "host":"localhost",
        "user":"fernweh",
        "password":"clem02069008",
        "database":"kino"}
    c = connector.connect(**config)
    return c
def extract_information(mycursor):
    """
    Extrait les titre
    :param mycursor:
    :return: Retourne un array avec tous les titres
    """
    info = []
    sql = """select Titel from folge"""
    cur = mycursor.cursor()
    cur.execute("select Titel from folge")
    titre = cur.fetchall()
    for x in titre:
        x = replacement(x)
        info.append(x)
    return info

def recherche(driver,info):
    """
    Recherche le titre de l'épisode sur google
    :param driver:
    :param info:

    """
    for x in range(len(info)):
        actionChain = ActionChains(driver)
        try:
            search = driver.find_element_by_class_name('gLFyf')
            buffer = info[x].replace(' ','')
            motcle = u"tatort"+ " "  + " " "dvd" + ' ' +buffer

            search.send_keys(motcle)
            search.send_keys(Keys.RETURN)
            result = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="islrg"]')))
            element = result.find_element_by_class_name('isv-r')
            actionChain.move_to_element(element).context_click().perform()
            time.sleep(1)
            click_save(motcle, driver)
            driver.back()
            #S'il n'y a aucun résultat il passe au prochain
        except TimeoutException:
            driver.back()
        except NoSuchElementException:
            driver.back()
        except:
            driver.back()

def click_save(motcle,driver):
    """
    Enregistre la phot sur mon ordinateur
    :param motcle:
    :param driver:
    :return:
    """
    for x in range(8):
        pyautogui.press("down")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("backspace")

    pyautogui.write(motcle)
    pyautogui.press("enter")
    time.sleep(2)
    #element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//div[@class="isv-r"]')))
def replacement(motcle):
    """
    Traite les caractères spéciaux parce que le programme ommettait les caractère. Le replacement des lettres
    n'est pas laissé au hasard. C'est le standard de la langue allemande pour remplacer les lettres en un alphabet
    latin.
    :param motcle:
    :return:
    """
    motcle = ''.join(motcle)
    motcle= motcle.replace("ä","ae")
    motcle = motcle.replace("ö","oe")
    motcle = motcle.replace("ü","ue")
    motcle = motcle.replace("ß","ss")
    return motcle
if __name__ == '__main__':
    main()