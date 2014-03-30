#!/usr/bin/env python
import sys, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# TODO: Use getopt instead?
#       That'll let me do things like configure verbose output, etc.
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
    except Exception:
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
except Exception:
    pass

# Scroll until we can scroll no more!
friends_seen = 0
while True:
    page_height = getPageHeight(driver)
    friends_shown = driver.find_elements_by_css_selector('.uiProfileBlockContent a:not(.uiLinkSubtle)')
    for friend in friends_shown[friends_seen:]:
        webdriver.ActionChains(driver).move_to_element(friend).perform()
        time.sleep(1) # Let Facebook load this hovercard, remove the old one.
        try:
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'HovercardFollowButton')))
            btn = el.find_element_by_link_text('Following')
            btn.click()
        except Exception:
            pass # We're not following this person so forget it.
        finally:
            friends_seen += 1
    time.sleep(3) # Give it a few seconds to load.
    new_page_height = getPageHeight(driver)
    if new_page_height == page_height:
        break

# And we're done! :)
driver.quit()
