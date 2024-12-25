import pandas as pd
import re


from config_loader import load_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


start_time = time()

config = load_config()
output_path_excel = config["output_path_excel"]
output_path_csv = config["output_path_csv"]
# driver_path = config["driver_path"]
password = config["password"]
email = config["email"]

driver = webdriver.Chrome()

url="https://www.skoob.com.br/login/"
driver.get(url)
sleep(4)
# driver.find_element(By.ID, "UsuarioEmail").send_keys("leolaurindorj@gmail.com")
driver.find_element(By.ID, "UsuarioEmail").send_keys(email)
element_pass = driver.find_element(By.ID, "UsuarioSenha")

# element_pass.send_keys("yeahyeah")
element_pass.send_keys(password)
sleep(1)

element_pass.send_keys(Keys.ENTER)

print("Login Ok")

sleep(1.5)
original_url = driver.current_url

# Extract the number using regular expression
match = re.search(r"/(\d+)-", original_url)
if match:
    user_id = match.group(1)
    # Compose new URL
    new_url = f"https://www.skoob.com.br/estante/livros/todos/{user_id}"
    print(new_url)  # Or navigate to it using driver.get(new_url)
else:
    print("No match found")


driver.get(new_url)
driver.refresh
sleep(3)

check_box_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH,'/html/body/div/div[2]/div[2]/div/div/div[2]/div/div[1]/a[2]'))
     )
check_box_element.click()

print("Sucssefull screen ajustment ")

try:
    element = driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[4]/div[2]/div[1]/div[1]/div/span[1]')
    qty_books_text = element.text
except Exception as e:
    print("Error finding element:", e)
    qty_books_text = "0"

qty_books = re.findall("[0-9]+", qty_books_text)

if qty_books:
    qty_pages = round(int(qty_books[0])/36) + 1
else:
    qty_pages = 0

print(qty_pages)

print("Rodou até aqui")

l_books=[]
qty=1

page_number = 1  # Starting from page 1 instead of reading from a file.

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

        author = author_publisher[0] if len(author_publisher) > 0 else None
        publisher = author_publisher[1] if len(author_publisher) > 1 else None
        image_element = book.find_element(By.TAG_NAME, "img")
        image_url = image_element.get_attribute("src")

        b_details = {'title':title,'author': author,'publisher': publisher, 'info': None, 'image': image_url}

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

    if page_number <= qty_pages:
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[ng-click="selectPage(page + 1)"]')

            # Check if next button is disabled
            parent_li = next_button.find_element(By.XPATH, value='..')  # Get parent <li> of the <a> tag
            if 'disabled' not in parent_li.get_attribute('class'):
                next_button.click()
                sleep(3)
            else:
                print("Reached last page earlier than expected.")
                break
        except:
            print("Error: Next button not found.")
            break

    sleep(3)

print("Total number of books fetched:", len(l_books))

df_books = pd.DataFrame(l_books)

df_books[['year', 'pages']] = df_books['info'].str.extract(r'Ano: (\d+) / Páginas: (\d+)')
df_books['year'] = df_books['year'].astype(int)
df_books['pages'] = df_books['pages'].astype(int)

# Drop the original 'info' column if needed
df_books.drop('info', axis=1, inplace=True)

df_books.to_csv(output_path_csv, index=False)

df_books.to_excel(output_path_excel, index=False)

print("Total number of rows in DataFrame:", len(df_books))
