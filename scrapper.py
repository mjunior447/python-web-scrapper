# Web scrapping em python usando o Selenium Webdriver para interagir
# especificamente com o navegador Google Chrome
# Para rodar o código, baixe o ChromeDriver no link
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# Depois, extraia o arquivo, insira o local do arquivo extraído na variável PATH
# e exporte a PATH


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlsxwriter
import math

url = 'https://www.amazon.com/'
driver = webdriver.Chrome()
driver.get(url)

search_box = driver.find_element_by_id("twotabsearchtextbox")
search_box.send_keys("iphone")
search_box.send_keys(Keys.RETURN)

cellphone_names = driver.find_elements_by_css_selector(".s-result-item div h2 a span.a-size-medium.a-color-base.a-text-normal")
names = []
prices = []

# pegando a lista de títulos de aparelhos
for cellphone in cellphone_names:
    names.append(cellphone.text)

# pegando lista de preços de aparelhos
i = 0
while (i < len(names)):
    item = driver.find_element_by_xpath("//div[@class='s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col sg-col-12-of-16']/following-sibling::div[" + str(i + 1) + "]")
    item_text = driver.find_element_by_xpath("//div[@class='s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col sg-col-12-of-16']/following-sibling::div[" + str(i + 1) + "]").text

    # Caso o item tenha um preço, esse preço será inserido
    # na lista de precos. Caso não o tenha, um traço '-'
    # será inserido na lista, indicando que não há preço para este produto.
    # Os preços foram divididos em sua parte inteira (whole) e fracionária (fraction), pois
    # não foi possível recuperar o preço completo de cada item com um único comando
    if (len(item.find_elements_by_css_selector('span.a-offscreen')) > 0):
        cellphone_price_whole = item.find_element_by_css_selector(".s-result-item div span.a-price-whole").text
        cellphone_price_fraction = item.find_element_by_css_selector(".s-result-item div span.a-price-fraction").text
        cellphone_price = float(str(cellphone_price_whole) + '.' + str(cellphone_price_fraction))
        prices.append(cellphone_price)
    else:
        prices.append('-')

    i += 1

# criando arquivo excel com os dados das
# listas de nomes e de preços
workbook = xlsxwriter.Workbook('prices-table.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
i = 0

while i < len(names) or i < len(prices):
    worksheet.write(row, col,     names[i])
    worksheet.write(row, col + 1, prices[i])
    row += 1
    i   += 1

workbook.close()
driver.close()