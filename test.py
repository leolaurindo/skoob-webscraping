import json
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def perform_login(driver, email, password):
    driver.get(config['login_url'])
    sleep(4)
    driver.find_element(By.ID, "UsuarioEmail").send_keys(email)
    element_pass = driver.find_element(By.ID, "UsuarioSenha")
    element_pass.send_keys(password)
    sleep(1)
    element_pass.send_keys(Keys.ENTER)
    print("Login OK")


def extract_user_id(driver):
    original_url = driver.current_url
    match = re.search(r"/(\d+)-", original_url)
    if match:
        user_id = match.group(1)
        return f"https://www.skoob.com.br/estante/livros/todos/{user_id}"
    else:
        print("No match found")
        return None


def click_filter_checkbox(driver):
    check_box_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div/div[2]/div/div[1]/a[2]'))
    )
    check_box_element.click()
    print("Successful screen adjustment")


def get_quantity_of_books(driver):
    try:
        element = driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[4]/div[2]/div[1]/div[1]/div/span[1]')
        qty_books_text = element.text
    except Exception as e:
        print("Error finding element:", e)
        qty_books_text = "0"
    qty_books = re.findall("[0-9]+", qty_books_text)

    return round(int(qty_books[0]) / 36) + 1 if qty_books else 0


def scrape_books(driver, qty_pages):
    l_books = []
    page_number = 1

    while page_number <= qty_pages:
        print("Processing page:", page_number)

        sleep(2.5)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'clivro')))
        books = driver.find_elements(By.CLASS_NAME, 'clivro')

        for i in range(len(books)):
            book = driver.find_elements(By.CLASS_NAME, 'clivro')[i]

            WebDriverWait(driver, 10).until(EC.visibility_of(book))
            WebDriverWait(book, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'livro-conteudo'))
                )
            d = book.find_element(By.CLASS_NAME, 'livro-conteudo')
            title = d.find_element(By.CLASS_NAME, 'ng-binding').text
            author_publisher = d.find_element(By.TAG_NAME, 'p').text
            author_publisher = author_publisher.split('\n')
            author = author_publisher[0]
            publisher = author_publisher[1]
            b_details = {'title':title,'author': author,'publisher': publisher, 'info': None}

            # Instead of clicking the book, get its link
            relative_link = book.find_element(By.CSS_SELECTOR, 'div.livro-capa > a').get_attribute('href')
            book_link = relative_link

            # Open a new tab with the book link
            driver.execute_script(f'window.open("{book_link}","_blank");')

            # Switch to the new tab (it's always the last one)
            driver.switch_to.window(driver.window_handles[-1])

            # Now get the information as before, but without needing to go back
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.sidebar-desc'))
            )
            sidebar_desc = driver.find_element(By.CSS_SELECTOR, '.sidebar-desc')
            sidebar_text = sidebar_desc.text
            sidebar_lines = sidebar_text.split("\n")
            for line in sidebar_lines:
                if 'Páginas' in line:
                    pages_data = line.strip()
                    break

            b_details['info'] = pages_data
            l_books.append(b_details)
            df_books = pd.DataFrame(l_books)
            df_books.to_csv('my_books2222.csv', index=False)
            print("Saved book data for page:", page_number, ", book:", i + 1)

            # Close the tab after getting the data and switch back to the main window
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        # Increment the page number
        page_number += 1

    return pd.DataFrame(l_books)


def main():
    config = read_config()
    driver = webdriver.Chrome()
    perform_login(driver, config['email'], config['password'])
    new_url = extract_user_id(driver)
    if new_url:
        driver.get(new_url)
        sleep(3)
        click_filter_checkbox(driver)
        qty_pages = get_quantity_of_books(driver)
        print(f"Total number of pages: {qty_pages}")
        df_books = scrape_books(driver, qty_pages)
        df_books.to_csv(config['csv_output_path'], index=False)
        print(f"Total number of rows in DataFrame: {len(df_books)}")


if __name__ == "__main__":
    main()
