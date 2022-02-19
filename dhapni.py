from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import re
import os
import urllib.request

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)

time.sleep(5)
print("Enter test link: ")
test_link = str(input())
driver.get(test_link)
time.sleep(2)

test_title = driver.find_element_by_class_name("Header_Title__3mXad")
test_title_text = re.findall(
    r'<p>(.*)</p>', test_title.get_attribute('innerHTML'))[0]
os.mkdir(test_title_text)

buttons = driver.find_elements_by_class_name("Footer_MoveToQuestionBig__1-jSA")
question = 1
elements = driver.find_elements_by_class_name(
    "Question_QuestionContainer__2Elg3")

while(True):
    # question images
    text = elements[0].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    for link in links:
        urllib.request.urlretrieve(
            link, test_title_text + "/Question " + str(question) + "." + str(i) + ".png")
        i += 1

    # answer images
    text = elements[1].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    if links:
        for link in links:
            urllib.request.urlretrieve(
                link, test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
            i += 1
    else:
        answer = driver.find_element_by_class_name("Options_Container__2YfYv")
        ActionChains(driver).move_to_element(answer).perform()
        png = answer.screenshot_as_png
        with open(test_title_text + "/Answer " + str(question) + "." + str(i) + ".png", 'wb') as f:
            f.write(png)
        i += 1
        if elements[1].size['height']:
            ActionChains(driver).move_to_element(elements[1]).perform()
            png = elements[1].screenshot_as_png
            with open(test_title_text + "/Answer " + str(question) + "." + str(i) + ".png", 'wb') as f:
                f.write(png)


    print("Question " + str(question) + " done")
    question += 1

    if buttons[1].is_enabled() == False:
        break

    buttons[1].click()
    # time.sleep(1)

driver.close()
