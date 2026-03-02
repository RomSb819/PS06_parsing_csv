import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.divan.ru/category/svet"
driver.get(url)

wait = WebDriverWait(driver, 15)

# Ждём появления карточек
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ProductCardMain_container__WXc_c")))

cards = driver.find_elements(By.CSS_SELECTOR, "div.ProductCardMain_container__WXc_c")
print("Найдено карточек:", len(cards))

parsed_data = []

for card in cards:
    try:
        # Название (в твоём HTML оно есть)
        name = card.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text.strip()

        # Ссылка на товар (берём первую ссылку на /product/)
        link = card.find_element(By.CSS_SELECTOR, 'a[href*="/product/"]').get_attribute("href")

        # Цена (в HTML это meta content)
        price = card.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content").strip()

        parsed_data.append([name, price, link])

    except Exception as e:
        print("произошла ошибка при парсинге:", e)
        continue

driver.quit()

print("Собрано строк:", len(parsed_data))

with open("lamps.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["название товара", "цена", "ссылка"])
    writer.writerows(parsed_data)