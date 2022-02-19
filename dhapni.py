from selenium import webdriver
import time
import re
import urllib.request

driver = webdriver.Chrome("chromedriver.exe")
driver.set_window_size(1800,900)
time.sleep(5)
print("Enter test link: ")
test_link = str(input())
driver.get(test_link)
time.sleep(2)

test_title = driver.find_element_by_class_name("Header_Title__3mXad")


buttons = driver.find_elements_by_class_name("Footer_MoveToQuestionBig__1-jSA")
question = 1

while(True):
    elements = driver.find_elements_by_class_name(
        "Question_QuestionContainer__2Elg3")
    # question images
    text = elements[0].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    for link in links:
        urllib.request.urlretrieve(
            link, "test/Question " + str(question) + "." + str(i) + ".png")
        i += 1
    text = elements[1].get_attribute('innerHTML')
    # answer images
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    for link in links:
        urllib.request.urlretrieve(
            link, "test/Answer " + str(question) + "." + str(i) + ".png")
        i += 1

    print("Question " + str(question) + " done")
    question += 1

    if buttons[1].is_enabled() == False:
        break

    buttons[1].click()
    time.sleep(1)

driver.close()
