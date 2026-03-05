import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import matplotlib.pyplot as plt


def parse_price_to_int(price_str: str) -> int | None:
    """
    Превращает строку цены вроде:
    "12 990 ₽", "12990", "12 990", "от 12 990 ₽"
    в число 12990.
    Возвращает None, если число не найдено.
    """
    if not price_str:
        return None

    # Убираем "узкие пробелы" и обычные пробелы приводим к нормальному виду
    s = price_str.replace("\u202f", " ").replace("\xa0", " ").strip().lower()

    # Ищем самое адекватное число (берём все цифры, игнорируя пробелы)
    digits = re.findall(r"\d+", s)
    if not digits:
        return None

    # Склеиваем все группы цифр: "12 990" -> ["12","990"] -> "12990"
    return int("".join(digits))


def build_price_histogram_from_csv(csv_path: str, bins: int = 20):
    prices = []

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            price_raw = row.get("цена", "")
            price_value = parse_price_to_int(price_raw)
            if price_value is not None:
                prices.append(price_value)

    print(f"Цен найдено: {len(prices)}")
    if not prices:
        print("Не удалось распознать ни одной цены — проверь, что в CSV в колонке 'цена' есть числа.")
        return

    # Гистограмма
    plt.figure(figsize=(10, 5))
    plt.hist(prices, bins=bins)
    plt.title("Распределение цен (гистограмма)")
    plt.xlabel("Цена")
    plt.ylabel("Количество товаров")
    plt.tight_layout()

    # Покажет окно с графиком
    plt.show()

    plt.savefig("prices_hist.png", dpi=150)






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

csv_file = "lamps.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["название товара", "цена", "ссылка"])
    writer.writerows(parsed_data)
    print(f'csv файл сохранен: {csv_file}')


# ------------------ Обработка CSV + гистограмма ------------------
build_price_histogram_from_csv(csv_file, bins=20)