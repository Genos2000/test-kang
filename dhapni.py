from selenium import webdriver
import time
import re
import os
import urllib.request

from docx import Document
from docx.shared import Inches

driver = webdriver.Chrome()
driver.set_window_size(1280, 720)

time.sleep(5)
print("Enter test link: ")
test_link = str(input())
driver.get(test_link)
time.sleep(2)

test_title = driver.find_element_by_class_name("Header_Title__3mXad")
test_title_text = re.findall(
    r'<p>(.*)</p>', test_title.get_attribute('innerHTML'))[0]
try:
    os.mkdir(test_title_text)
except:
    pass

document = Document()
document.add_heading(test_title_text, 0)

buttons = driver.find_elements_by_class_name("Footer_MoveToQuestionBig__1-jSA")
question = 1

while(True):
    elements = driver.find_elements_by_class_name(
        "Question_QuestionContainer__2Elg3")
    # question images
    text = elements[0].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)

    # add question no to doc
    document.add_heading(
        'Q '+str(question)+')', level=2)


    i = 1
    for link in links:
        urllib.request.urlretrieve(
            link, test_title_text + "/Question " + str(question) + "." + str(i) + ".png")
        # add question image(S) to doc
        document.add_picture(test_title_text + "/Question " +
                             str(question) + "." + str(i) + ".png", width=Inches(5.5))
        i += 1
    text = elements[1].get_attribute('innerHTML')



    # answer images
    links = re.findall(r'src="([^"]*)"', text)

    # add question no to doc
    document.add_heading(
        'A '+str(question)+')', level=2)

    i = 1
    for link in links:
        urllib.request.urlretrieve(
            link, test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
        # add answer image(S) to doc
        document.add_picture(test_title_text + "/Answer " +
                             str(question) + "." + str(i) + ".png", width=Inches(5.5))
        i += 1

    print("Question " + str(question) + " done")
    question += 1

    if buttons[1].is_enabled() == False:
        break

    buttons[1].click()
    time.sleep(1)
    document.add_page_break()

driver.close()
document.save(test_title_text+"/"+test_title_text+'.docx')
