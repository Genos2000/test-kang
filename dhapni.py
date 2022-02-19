from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import re
import os
import urllib.request

# docx imports
from docx import Document
from docx.shared import Inches


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
try:
    os.mkdir(test_title_text)
except:
    pass

buttons = driver.find_elements_by_class_name("Footer_MoveToQuestionBig__1-jSA")
question = 1
elements = driver.find_elements_by_class_name(
    "Question_QuestionContainer__2Elg3")

questions_image_furls = []
answers_image_furls = []

while(True):
    # question images
    text = elements[0].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    question_image_furls = []
    for link in links:
        urllib.request.urlretrieve(
            link, test_title_text + "/Question " + str(question) + "." + str(i) + ".png")
        question_image_furls.append(
            test_title_text + "/Question " + str(question) + "." + str(i) + ".png")
        i += 1
    questions_image_furls.append(question_image_furls)

    # answer images
    text = elements[1].get_attribute('innerHTML')
    links = re.findall(r'src="([^"]*)"', text)
    i = 1
    answer_image_furls = []
    if links:
        for link in links:
            urllib.request.urlretrieve(
                link, test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
            answer_image_furls.append(test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
            i += 1
    else:
        answer = driver.find_element_by_class_name("Options_Container__2YfYv")
        ActionChains(driver).move_to_element(answer).perform()
        png = answer.screenshot_as_png
        with open(test_title_text + "/Answer " + str(question) + "." + str(i) + ".png", 'wb') as f:
            f.write(png)
            answer_image_furls.append(
                test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
        i += 1
        if elements[1].size['height']:
            ActionChains(driver).move_to_element(elements[1]).perform()
            png = elements[1].screenshot_as_png
            with open(test_title_text + "/Answer " + str(question) + "." + str(i) + ".png", 'wb') as f:
                f.write(png)
                answer_image_furls.append(
                    test_title_text + "/Answer " + str(question) + "." + str(i) + ".png")
    answers_image_furls.append(answer_image_furls)


    print("Question " + str(question) + " done")
    question += 1

    if buttons[1].is_enabled() == False:
        break

    buttons[1].click()
    # time.sleep(1)

driver.close()

# docx prep start


document = Document()

# add test name as title to  doc
document.add_heading(test_title_text, 0)

document.add_heading('Questions', level=1)

for q_no, q_furls in enumerate(questions_image_furls):
    # add question no to doc
    document.add_heading('Q '+str(q_no+1)+')', level=2)
    for q_furl in q_furls:
        try:
            document.add_picture(q_furl, width=Inches(5.5))
        except:
            document.add_paragraph('some err', style='Intense Quote')
    document.add_page_break()


document.add_page_break()
document.add_heading('Answers', level=1)

for ans_no, ans_furls in enumerate(answers_image_furls):
    # add ans no to doc
    document.add_heading('A '+str(ans_no+1)+')', level=2)
    for ans_furl in ans_furls:
        try:
            document.add_picture(ans_furl, width=Inches(5.5))
        except:
            document.add_paragraph('some err', style='Intense Quote')
    document.add_page_break()

document.save(test_title_text+"/"+test_title_text+'.docx')



