import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import csv
from openpyxl import load_workbook

# Khởi tạo các tùy chọn cho Chrome
chromeOptions = Options()

# domain  = input()

# domain_link = domain.replace(" ", "+")
# day_from = input()
# day_to = input()
domain_link = sys.argv[1]
day_from = sys.argv[2]
day_to = sys.argv[3]


# Khởi tạo trình duyệt Chrome với tùy chọn
driver = webdriver.Chrome(executable_path="./chromedriver")


# Điều hướng tới URL cần truy cập
driver.get(f"https://www.google.com/search?q={domain_link}")


def create_csv_file(filename, header):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

def extract_data_to_csv(driver):
    titles = driver.find_elements(By.CLASS_NAME, 'n0jPhd')
    days = driver.find_elements_by_class_name('rbYSKb')
    url = driver.find_elements_by_class_name('WlydOe')

    data = []

    # Extract the text from the web elements
    for i in range(len(titles)):
        title_text = titles[i].text
        day_text = days[i].text
        url_link = url[i].get_attribute('href')
        platform = "News"
        
        authors = driver.find_elements_by_xpath(f'//*[@id="rso"]/div/div/div[{i+1}]/div/div/a/div/div[2]/div[1]/span')
        author_data = [author.text for author in authors]
        
        contents = driver.find_elements_by_xpath(f'//*[@id="rso"]/div/div/div[{i+1}]/div/div/a/div/div[2]/div[3]')
        content_data = [content.text for content in contents]
        
        for j in range(len(author_data)):
            main_author = author_data[j]
            main_content = content_data[j]
            data.append([title_text, platform, main_author, main_content, day_text, url_link])

    df = pd.DataFrame(data, columns=['Title', 'Platform', 'Author', 'Content', 'Day', 'Link'])

    # Save the DataFrame to a CSV file
    filename = 'data.csv'
    df.to_csv(filename, index=False, mode='a', header=False)

    return data

def extract_tatca_to_csv(driver):
    titles = driver.find_elements_by_xpath(".//h3[contains(@class,'')] ")
    content_small = driver.find_elements_by_class_name('MjjYud.hlcw0c')
    url = driver.find_elements_by_xpath("//a[@jsname='qOiK6e']")
    contents = driver.find_elements_by_xpath("//div[@class='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf']")

    days = driver.find_elements_by_xpath(".//span[contains(@class,'MUxGbd')]")


    author = driver.find_elements_by_xpath("//span[@class='VuuXrf']")
    data = []


    for i in range(len(titles)):
        title_text = titles[i].text
        

        content = ''
    
        platform = 'News'
        main_author = ''
        try:
            url_link = url[i].get_attribute('href')
        except:
            url_link = ''
                    
        try:
            date_value = days[i].text
        except :
            date_value = ' '

        data.append([title_text, platform, main_author, content, date_value, url_link])
            
    df = pd.DataFrame(data, columns=['Title', 'Platform', 'Author', 'Content', 'Day', 'Link'])

    # Save the DataFrame to a CSV file
    filename = 'data.csv'
    df.to_csv(filename, index=False, mode='a', header=False)

    return data
    
   
   
def extract_video_data_to_csv(driver):
    titles = driver.find_elements_by_class_name("LC20lb")
    days = driver.find_elements_by_class_name('P7xzyf')
    data = []
    for giatri in range(len(titles)):
        title_text = titles[giatri].text
        try:
            day_text = days[giatri].text
        except IndexError:
            day_text = ""
        try:
            #youtube
            url = driver.find_element_by_xpath(f'//*[@id="rso"]/div[{giatri+1}]/div/div/div/div/div/div[1]/div[1]/div/a')
        except:
            #web,tiktok,...
            url = driver.find_element_by_xpath(f'//*[@id="rso"]/div[{giatri+1}]/div/div/div/div/div[1]/div/a')
        url_link = url.get_attribute('href')
        values = day_text.split("·")
        try:
            title_values = values[0].strip()
        except IndexError:
            title_values =""
        try:
            author_values = values[1].strip()
        except IndexError:
            author_values = ""
        try:
            day_values = values[2].strip()
        except IndexError:
            day_values = ""
        
        # main_content_elements = driver.find_elements_by_class_name('Uroaid')
        main_content = ""
        # for content in main_content_elements:
        #     main_content += content.text + " "
        
        data.append([title_text, title_values,author_values,main_content, day_values, url_link])
    df = pd.DataFrame(data, columns=['Title', 'Platform','Author','Content','Day', 'Link'])
    header = ['Title', 'Platform','Author','Content','Day', 'Link']
    # Save the DataFrame to a CSV file
    filename = 'data.csv'
    df.to_csv(filename, index=False, mode='a', header=False)
    return data





congcu_link = driver.find_element(By.ID, "hdtb-tls")
congcu_link.click()
time.sleep(0.2)
moi_ngon_ngu_element = driver.find_element(By.CLASS_NAME, "KTBKoe")
moi_ngon_ngu_element.click()
tim_tieng_viet_element = driver.find_element_by_link_text("Tìm những trang Tiếng Việt")
tim_tieng_viet_element.click()
tat_ca_div = driver.find_elements(By.CLASS_NAME, "KTBKoe")
header = ['Title', 'Platform', 'Author', 'Content', 'Day', 'Link']
create_csv_file('data.csv', header)
# create_csv_file('data.csv', header)
# Lặp qua từng phần tử và tìm phần tử "Mọi lúc" (không trùng với "Mọi ngôn ngữ")
for div_element in tat_ca_div:
        if div_element.text == "Mọi lúc" and "Mọi ngôn ngữ" not in div_element.text:
                # Nhấn vào phần tử "Mọi lúc"
                header = ['Title', 'Platform', 'Author', 'Content', 'Day', 'Link']
                create_csv_file('data.csv', header)
                div_element.click()
                span_element = driver.find_element_by_xpath('//span[text()="Phạm vi tùy chỉnh..."]')
                span_element.click()
                # Tìm phần tử input theo id
                inputdayfrom_element = driver.find_element_by_id("OouJcb")
                # Gửi dữ liệu vào ô input
                
                inputdayfrom_element.send_keys(f"{day_from}")
                time.sleep(0.2)
                inputdayto_element = driver.find_element_by_id("rzG2be")
                
                inputdayto_element.send_keys(f"{day_to}")
                time.sleep(0.2)
                tim_element = driver.find_element_by_class_name("Ru1Ao")
                tim_element.click()
                time.sleep(0.5)
                
                extract_tatca_to_csv(driver)
                has_next_page_tatca = True
                while has_next_page_tatca:
                    try:
                        nextpage_linktatca = driver.find_element_by_link_text("Tiếp")
                        
                        nextpage_linktatca.click()
                        
                        time.sleep(1)
                        extract_tatca_to_csv(driver)
                    except:
                        has_next_page_tatca = False
                        tintuc_element = driver.find_element_by_link_text("Tin tức")
                        tintuc_element.click()
                        time.sleep(1)
                        has_next_page = True

                        while has_next_page:
                            try:        
                                nextpage_link = driver.find_element_by_link_text("Tiếp")
                                extract_data_to_csv(driver)
                                nextpage_link.click()
                                time.sleep(1)
                            except:
                                has_next_page = False
                                extract_data_to_csv(driver)
                                
                                video_element = driver.find_element_by_link_text("Video")
                                video_element.click()
                                time.sleep(1)
                                has_next_page_youtube = True
                                extract_video_data_to_csv(driver)
                                while has_next_page_youtube:
                                    try:
                                        nextpage_link_video = driver.find_element_by_link_text("Tiếp")
                                        nextpage_link_video.click()
                                        extract_video_data_to_csv(driver)
                                        time.sleep(1)
                                    except:
                                        has_next_page_youtube = False
                                        extract_video_data_to_csv(driver)
                                        
                                        driver.quit()