import smtplib
from datetime import time
from email.mime.text import MIMEText

import psycopg2
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
from datetime import datetime

import crud
from models import Base, ArticleTable
from sqlalchemy.orm import Session
from database import engine, SessionLocal


def fetch_data(db: Session):
    # WebDriver 설정 (Chrome, Firefox 등)
    global updated_article
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    url = 'https://m.land.naver.com/map/37.5341296:126.972125:16/APT:OPST:VL:JWJT:DDDGG:SGJT:HOJT/B1:B2?spcMin=66&spcMax=900000000&wprcMax=50000&rprcMax=100&#mapFullList'
    driver.get(url)
    driver.set_window_size(1024, 768)  # Width, Height
    # 웹사이트 로딩 대기
    time.sleep(2)
    # Find the element
    element = driver.find_element(By.CSS_SELECTOR, '.btn_option._article')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.CSS_SELECTOR, '.tab_sorting_list')
    element.click()
    time.sleep(3)
    # BeautifulSoup을 사용하여 데이터 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elements = soup.select('#_listContainer > div > div.article_box.article_box--sale > div')

    total_elements = len(elements)
    update_status = False
    # Print each element
    for i in range(total_elements):
        element = elements[i]
        if element is not None:
            update_status = True
            try:
                title_area = element.select_one('.title_area')
                price_area = element.select_one('.price_area')
                information_area = element.select_one('.information_area')
                tag_area = element.select_one('.tag_area')
                merit_area = element.select_one('.merit_area')
                label_merit_elements = merit_area.select('.label_merit')
                label_data_element = label_merit_elements[0].select_one('.label_data')
                if label_data_element is not None:
                    label_data = label_data_element.text
                    label_data = label_data.strip('.')  # Remove any trailing periods
                    date_object = datetime.strptime(label_data, '%y.%m.%d')
                    print("Label Data:", date_object)
                item_link = element.select_one('.item_link._moreLink')
                if item_link is not None:
                    _articleno = item_link.get('_articleno')
                    # Append the href to the base URL
                    full_url = 'https://fin.land.naver.com/article/info/' + _articleno
                    # Print the full URL
                    print("Full URL:", full_url)
                    print("Article Number:", _articleno)
                else:
                    _articleno = None
                    full_url = None
                if title_area is not None:
                    print("Title Area:", title_area.text)
                if price_area is not None:
                    print("Price Area:", price_area.text)
                if information_area is not None:
                    print("Information Area:", information_area.text)
                if tag_area is not None:
                    print("Tag Area:", tag_area.text)
                if merit_area is not None:
                    print("Merit Area:", merit_area.text)
                article = ArticleTable(
                    title_area=title_area.text,
                    price_area=price_area.text,
                    information_area=information_area.text,
                    tag_area=tag_area.text,
                    merit_area=date_object,
                    full_url=full_url,
                    article_number=_articleno
                )
                updated_article = crud.store_data(db, article)
            except AttributeError:
                print("Element not found")
    time.sleep(5)
    driver.quit()

    return updated_article


def send_email(body):
    sender = 'ttttt@gmail.com'
    receiver = 'ttttt@gmail.com'
    msg = MIMEText(str(body))  # Convert the ArticleTable object to a string
    msg['Subject'] = 'Update Detected on Website'
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('ttttt@gmail.com', 'test')
        server.sendmail(sender, receiver, msg.as_string())
        print('Email sent!')


def main():
    db = SessionLocal()  # Create a new session
    Base.metadata.create_all(engine)

    while True:
        updated_article = fetch_data(db)
        if updated_article:
            send_email(updated_article)
            print('New update detected!')
        time.sleep(60)  # 10초 동안 쉬기


main()
