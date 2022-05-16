import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

user = os.getenv("LINK_USER")
pas = os.getenv("LINK_PASS")

s = Service(executable_path=r"c:\Development\chromedriver.exe")
browser = webdriver.Chrome(service=s)
wait = WebDriverWait(browser, 30)
browser.get(
    'https://www.linkedin.com/jobs/search/?currentJobId=3043294001&f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom')
browser.maximize_window()
login_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav__button-secondary")))
time.sleep(2)
login_button.click()
time.sleep(2)
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
username.send_keys(user)
password = wait.until(EC.presence_of_element_located((By.ID, "password")))
password.send_keys(pas)
login = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn__primary--large.from__button--floating")))
login.click()
time.sleep(3)

jobs = wait.until(EC.visibility_of_all_elements_located(
    (By.CSS_SELECTOR, 'div.full-width.artdeco-entity-lockup__title.ember-view [href*="/jobs/view"]')))

iter = 1
for job in jobs:
    time.sleep(3)
    try:
        print(job.text)
    except StaleElementReferenceException:
        print("There is no job for apply")
        break

    job.click()
    time.sleep(3)
    try:
        apply_button = browser.find_element(By.CLASS_NAME, "jobs-apply-button")
        time.sleep(3)
    except NoSuchElementException:
        print("Daha önce başvuru yapılmış")
    except TimeoutException:
        print("Daha önce başvuru yapılmış")
    else:
        apply_button.click()
        flag = True

        while flag:
            next_button3 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary")))
            time.sleep(2)
            if "Başvuruyu gönder" in next_button3.text:

                try:
                    follow = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.relative.mt5.ph5')))
                except NoSuchElementException:
                    print("No such web element")

                except TimeoutException:
                    print("Bağlantı zamanı aşımı")

                except InvalidSelectorException:
                    print("Yanlış selector")

                else:

                    if follow.is_enabled():
                        print(follow.is_enabled)
                        follow.click()
                        next_button3.click()
                        try:
                            time.sleep(2)
                            quiz = browser.find_element(By.CSS_SELECTOR, "Değerlendirme alın")
                        except NoSuchElementException:
                            time.sleep(2)
                            finish = wait.until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, 'button')))
                            finish.click()
                            flag = False
                        except TimeoutException:
                            time.sleep(2)
                            print("Zaman aşımı")
                            finish = wait.until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, 'button')))
                            finish.click()
                            flag = False
                        else:
                            time.sleep(2)
                            closeX = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                '[role="dialog"]')))
                            closeX.click()
                            flag = False

            else:
                next_button3.click()
    iter += 1
    if iter == len(jobs):
        break
print(f'You have applied for {len(jobs)} jobs')
time.sleep(3)
browser.quit()
