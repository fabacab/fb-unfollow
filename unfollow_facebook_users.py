#!/usr/bin/env python
import sys, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

FB_USER = sys.argv[1]
FB_PASS = sys.argv[2]

def loginToFacebook (username, password):
    driver.find_element_by_id('email').send_keys(FB_USER)
    driver.find_element_by_id('pass').send_keys(FB_PASS)
    driver.find_element_by_id('loginbutton').click()

def clickThruCheckpoints (driver):
    try:
        driver.find_element_by_css_selector('[name="name_action_selected"][value="dont_save"]').click()
        driver.find_element_by_id('checkpointSubmitButton').click()
    except:
        driver.find_element_by_id('checkpointSubmitButton').click()
        driver.find_element_by_id('checkpointSecondaryButton').click() # "This is Okay"
        driver.find_element_by_css_selector('[name="name_action_selected"][value="dont_save"]').click()
        driver.find_element_by_id('checkpointSubmitButton').click()

def getPageHeight (driver):
    return int(driver.execute_script('return document.body.scrollHeight;'))

driver = webdriver.Firefox()
driver.get('https://www.facebook.com/' + FB_USER + '/friends')

if 'Content Not Found | Facebook' == driver.title:
    loginToFacebook(FB_USER, FB_PASS)

try:
    while driver.find_element_by_id('checkpointSubmitButton'):
        clickThruCheckpoints(driver)
except:
    pass

# Scroll until we can scroll no more!
while True:
    page_height = getPageHeight(driver)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3) # Give it a couple seconds to load
    new_page_height = getPageHeight(driver)
    if new_page_height == page_height:
        break

friends_shown = driver.find_elements_by_css_selector('.uiProfileBlockContent a:not(.uiLinkSubtle)')
for friend in friends_shown:
    webdriver.ActionChains(driver).move_to_element(friend).perform()
    try:
        el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Following')))
        el.click()
    except:
        pass # We're not following this person so forget it.

# And we're done! :)
driver.quit()
