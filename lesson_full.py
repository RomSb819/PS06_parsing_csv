import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://hh.ru/vacancies/rukovoditel_otdela_logistiki"
driver.get(url)

# 1) Вместо sleep(3) — нормальное ожидание элементов
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')))

# 2) Вместо динамического класса — стабильный data-qa
vacancies = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')
print("Найдено карточек:", len(vacancies))

parsed_data = []

for vacancy in vacancies:
    try:
        # 3) Берём заголовок и ссылку из одного элемента (он же <a>)
        title_el = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]')
        title = title_el.text.strip()
        link = title_el.get_attribute('href')

        # 4) Компания
        company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text.strip()

        # 5) Зарплаты может не быть: find_elements -> безопасно
        salary_els = vacancy.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-compensation"]')
        salary = salary_els[0].text.strip() if salary_els else ""

        # 6) ВАЖНО: добавляем в список внутри цикла
        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print("произошла ошибка при парсинге:", e)
        continue

driver.quit()

print("Собрано строк:", len(parsed_data))

with open("hh.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])
    writer.writerows(parsed_data)