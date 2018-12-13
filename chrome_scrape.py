#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time as t
import datetime
from random import randint
import subprocess
import logging
import socket
import os
import RPi.GPIO as GPIO

#set logger
logger = logging.getLogger('scrape')
handler = logging.FileHandler('/var/tmp/scrape.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def Shutdown(channel):
    logger.warning('Button shutdown')
    os.system('sudo shutdown -h now')
def Restart(channel):
    logger.warning('Button restart')
    os.system('sudo shutdown -r now')

#5-6   = GPIO3-GND
#37-39 = GPIO26-GND
#set gpio buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(3, GPIO.FALLING, callback = Shutdown, bouncetime = 3000)
GPIO.add_event_detect(26, GPIO.FALLING, callback = Restart, bouncetime = 3000)

def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

def x_clicker(sec, xpath):
    element = driver.find_element_by_xpath(xpath).click()
    t.sleep(sec)

logger.info('Starting')
club = "Spaarne"
pages = []
# set chrome options
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-fullscreen")
option.add_argument("disable-infobars")
# create new instance of chrome in incognito mode
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=option)
# check web connection
if socket.create_connection(("www.google.com", 80)):
    # go to website
    driver.get("https://ttapp.nl")
    logger.info('TTAPP loaded')
    t.sleep(5)
else:
    # reboot Pi if no wifi
    logger.error('No internet, rebooting')
    t.sleep(2)
    ################ FOR SETTING UP
    # uncomment reboot() to let Pi reboot if no wifi again
    #reboot()
# enter club to search for id
element = driver.find_element_by_id("txt-search")
element.clear
for i in range(len(club)):     # randomize input
    element.send_keys(club[i])
    t.sleep(randint(1,3))
# hit search button !!! protocol violation at boot
x_clicker(5,"//*[@id='btn-search']")
# browse to club page for id and then to the page with live scores
try:
    x_clicker(5,"//div[@data-bind='click: $parent.goclub']")
except NoSuchElementException:
    logger.error('Search button not found, rebooting')
    t.sleep(2)
    reboot()
logger.info('Search completed')
club_id = driver.current_url[-4:]
t.sleep(3)
driver.get("https://ttapp.nl/#/live/"+club_id)
t.sleep(3)
########## FOR TESTING
# set different date to test iterating through matches
##########
x_clicker(3,"//i[@onclick]")
x_clicker(3,"//td[text()='13']")
t.sleep(5)
# get match and group numbers of team that play today
n = 1
while n < 30:
    try:
        x_clicker(2,"//div[@data-bind='foreach: matches']/div["+str(n)+"]")
        pages.append(driver.current_url)
        x_clicker(2,"//a[@class='navitem']")
        pages.append(driver.current_url+"/s")
        driver.back()
        driver.back()
        t.sleep(2)
        n += 1
    except NoSuchElementException:
        n = 30
# click back to home to move cursor
x_clicker(2, "//div[@class='clickmagnetback pull-left']")
# browse through matches and standings of the teams
logger.info('Loop running for '+club_id)
while True:
    for index in range(len(pages)):
        driver.get(pages[index])
        t.sleep(7)
