from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime
import time
from string import punctuation
from selenium.webdriver.firefox.options import Options
options = Options()
options.binary_location = r"C:\Users\A7793\AppData\Local\Mozilla Firefox\firefox.exe"


def change_punct(string):
    new_string = ''
    for char in string:
        if char in punctuation:
            new_string += ' '
        else:
            new_string += char
    return new_string

def string_matcher(str1, str2):
    str1 = change_punct(str1)
    str2 = change_punct(str2)
    
    str1_list = str1.split()
    str2_list = str2.split()
    
    count = 0
    for word in str1_list:
        if word in str2_list:
            count += 1
    return count

def chapter_number_extractor(chapter_number_string):
    chapter_num = ""
    for char in chapter_number_string:
        if char.isdigit():
            chapter_num += char
    return int(chapter_num)


def chapter_num_and_name_extractor(chapter):
    chapter_list = chapter.split("_")
    if len(chapter_list) > 1:
        chapter_num_string = chapter_list[0]
        chapter_name = chapter_list[1]
    else:
        chapter_num_string = chapter_list[0]
        chapter_name = ""
    chapter_num = chapter_number_extractor(chapter_num_string)

    return chapter_num, chapter_name


url = "https://editorial.elsevier.com/app/login"

delay = 20 # seconds

today_date = datetime.now().date().strftime('%d%b%y')


def get_image_notes(title,chapter):

    figures_dict = {}
    download_link = ''

    # driver = webdriver.Firefox()

    driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe', firefox_options=options)

    driver.get(url)

    chapter_num, chapter_name = chapter_num_and_name_extractor(chapter)

    ## Accepting cookies
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
        driver.execute_script("arguments[0].click();", elem)
    except TimeoutException:
        print("Cookies already accepted!")


    ## Entering Username
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'username')))
        elem.send_keys("bkaur@aptaracorp.com")
    except TimeoutException:
        print("Can't enter username")
        driver.quit()


    ## Entering password
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'password')))
        elem.send_keys("Aptara@123456")
    except TimeoutException:
        print("Can't enter password")
        driver.quit()

    ## Hitting Submit
    try:
        elem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.NAME, 'submit')))
        driver.execute_script("arguments[0].click();", elem)
    except TimeoutException:
        print("Can't click submit")
        driver.quit()

    ## Then clicking other projects on new page
    try:
        elem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'ui-id-3')))
        driver.execute_script("arguments[0].click();", elem)
    except TimeoutException:
        print("Can't click Other projects")
        driver.quit()

    ## Finding the project with out title and clicking on it
    try:
        table = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'otherProjects:report')))
        
        all_projects = table.find_elements_by_css_selector('td.projectTitle')
        filtered_projects = []
        
        for project in all_projects:
            if(project.text != "No"):
                filtered_projects.append(project)
        
        project_link = ""
        

        
        flag = False

        for project in filtered_projects:
            if title in project.text:
                flag = True
                project_link = project.find_element_by_tag_name('a').get_attribute('href')
        
        if not(flag):
            closeness = []
            for project in filtered_projects:
                closeness.append(string_matcher(title,project.text))

            project = filtered_projects[closeness.index(max(closeness))]
            project_link = project.find_element_by_tag_name('a').get_attribute('href')
                        
        if project_link:

            ## Opening the title page

            driver.get(project_link)
            
            ## Clicking on the chapter
            
            try:
                chap_table = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'chpaterHeaderForm:chapterHeaderRow')))
                
                chapters = chap_table.find_elements_by_xpath("//table//tr/td/a")

                chapter_link = ''
                for chapter in chapters:
                    temp_chapter_num = ''
                    temp_chapter_name = ''
                    # print(chapter, chapter.text)
                    for char in chapter.text:
                        if char.isdigit():
                            temp_chapter_num += char
                        if char.isalpha():
                            temp_chapter_name += char
                    
                    if temp_chapter_num:
                        temp_chapter_num = int(temp_chapter_num)
                        # print(temp_chapter_num, temp_chapter_name)
                        if chapter_num and (chapter_num == temp_chapter_num):
                            if chapter_name and (chapter_name == temp_chapter_name):
                                chapter_link = chapter
                            else:
                                chapter_link = chapter
                            break

                if chapter_link:
                    # chapter_link.click()
                    driver.execute_script("arguments[0].click();", chapter_link)
                    ## Clicking on figures tab
                    try:
                        elem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'contribviewTabsForm:figuresTabLink')))
                        driver.execute_script("arguments[0].click();", elem)

                        ## Making the dict
                        
                        try:
                            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'figure_contribviewFigures')))
                            all_figures_div = elem.find_elements_by_css_selector('div.post')
                        #     print(len(all_figures_div))
                        #     print(all_figures_div)
                            for figure_div in all_figures_div:
                                try:
                                    figure_num = figure_div.find_element_by_css_selector('span.viewFigureNumber').text
                                except:
                                    figure_num = ''
                                try:
                                    figure_note = figure_div.find_element_by_css_selector('div.noteBody').text
                                except:
                                    figure_note = ''
                                
                                if figure_num and figure_note:
                                    figures_dict[figure_num] = figure_note
                                    
                        except TimeoutException:
                            print("Can't click on Figures")
                            driver.quit()

                        ## Getting the download link
                        try:
                            elem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'downloadFigures_contribviewFigures:exportAllFigures')))
                            driver.execute_script("arguments[0].click();", elem)

                            # driver.implicitly_wait(10) # seconds
                            time.sleep(40)

                            figures_download_div = driver.find_element_by_id('downloadfig')

                            
                            figures_links = figures_download_div.find_elements_by_tag_name('a')
                            for figures_link in figures_links:
                                if today_date.lower() in figures_link.text.lower():
                                    download_link = figures_link.get_attribute('href')
                                    break

                            
                        except TimeoutException:
                            print("Can't click on download all Figures")
                            driver.quit()



                    except TimeoutException:
                        print("Can't click on Figures")
                        driver.quit()


                else:
                    raise Exception('Chapter not found')
                    driver.quit()
                    
            except TimeoutException:
                print("Can't find chapters") 
                driver.quit()                       

            
            
            
        else:
            raise Exception('Title not found') 
            driver.quit()
            
    except TimeoutException:
        print("Can't locate table") 
        driver.quit()


    driver.quit()

    return (figures_dict,download_link)


#title = "Medical Emergencies in the Dental Office, 8e"
#chapter = "CH0003_Preparation"

#fig_dict, down_link = get_image_notes(title,chapter)
#print(fig_dict, down_link)

