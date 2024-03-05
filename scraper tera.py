import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

URL="https://www.terabyteshop.com.br/"
PRODUTO=""
NOME_ARQUIVO=f"{PRODUTO}.csv"

LINKPRODUTOS = []
NOMEPRODUTOS = []
PRECOPRODUTOS = []

boptions = Options()
boptions.add_argument('--headless')

driver = webdriver.Chrome()
driver.get(URL)

inputBusca = driver.find_element(By.ID, 'isearch')
inputBusca.send_keys(PRODUTO)
inputBusca.send_keys(Keys.ENTER)

try:
    wait = WebDriverWait(driver, 2)

    try:
        html = driver.find_elements(By.TAG_NAME, 'body')[0]
    except:
        print('not found')
        driver.refresh()
    
    html = html.get_attribute("innerHTML")

    bs = BeautifulSoup(html, 'html.parser')

    for item in bs.find_all('div', { 'class': 'pbox'}):
        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'prod-name')))

        link = item.find('a', class_='prod-name').get('href')
        nome = item.find('a', class_='prod-name').text

        # eu nao gosto mas se quiser adicionar um produto aqui que nao tem estoque fique a vonts
        if item.find('div', {'class': 'prod-new-price'}) is None:
            continue
        else:
            valor = item.find('div', {'class': 'prod-new-price'}).text

        LINKPRODUTOS.append(link)
        NOMEPRODUTOS.append(nome)
        PRECOPRODUTOS.append(valor)
    
except Exception as ex:
    print('[Error] ', ex)

driver.quit()

file = pd.DataFrame()
file['link'] = LINKPRODUTOS
file['nome'] = NOMEPRODUTOS
file['valor'] = PRECOPRODUTOS
file.to_csv(NOME_ARQUIVO)



