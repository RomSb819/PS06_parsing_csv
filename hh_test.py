import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

wait = WebDriverWait(driver, 15)

# Ждём, когда появятся карточки вакансий (на hh обычно это data-qa атрибут)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')))

vacancies = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')
print("Найдено карточек:", len(vacancies))

parsed_data = []

for vacancy in vacancies:
    try:
        title_el = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]')
        title = title_el.text.strip()
        link = title_el.get_attribute("href")

        company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text.strip()

        # зарплаты может не быть
        salary_els = vacancy.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-compensation"]')
        salary = salary_els[0].text.strip() if salary_els else ""

        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print("Ошибка при парсинге карточки:", e)
        continue

driver.quit()

print("Собрано строк:", len(parsed_data))

with open("hh_programmist.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название вакансии", "Название компании", "Зарплата", "Ссылка на вакансию"])
    writer.writerows(parsed_data)