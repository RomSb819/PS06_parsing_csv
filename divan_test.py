
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.divan.ru/category/svet"
driver.get(url)

wait = WebDriverWait(driver, 15)

# Ждём, пока на странице появятся ссылки на товары (карточки)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/product/"]')))

product_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
print("Найдено ссылок на товары:", len(product_links))

parsed_data = []
seen = set()

for a in product_links:
    try:
        link = a.get_attribute("href")
        title = a.text.strip()

        # Пропускаем пустые/дубли
        if not link or link in seen or not title:
            continue
        seen.add(link)

        # Пытаемся найти цену рядом (в пределах карточки)
        card = a.find_element(By.XPATH, "./ancestor::*[self::div or self::article][1]")

        price = ""
        # 1) иногда цена хранится в itemprop
        price_els = card.find_elements(By.CSS_SELECTOR, '[itemprop="price"]')
        if price_els:
            price = price_els[0].get_attribute("content") or price_els[0].text.strip()

        # 2) если не нашли — пробуем по частому паттерну "₽"
        if not price:
            candidates = card.find_elements(By.XPATH, ".//*[contains(text(),'₽')]")
            if candidates:
                price = candidates[0].text.strip()

        parsed_data.append([title, price, link])

    except Exception as e:
        print("Ошибка при парсинге карточки:", e)
        continue

driver.quit()

print("Собрано строк:", len(parsed_data))

with open("lamps.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["название товара", "цена", "ссылка"])
    writer.writerows(parsed_data)