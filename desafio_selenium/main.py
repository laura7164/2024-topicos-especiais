from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import re

# para inicializar o driver
driver = webdriver.Chrome()
driver.get('https://www.zoom.com.br/')

# para esperar até que a barra de pesquisa esteja visível e depois clicar na barra de pesquisa
wait = WebDriverWait(driver, 10)
search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.AutoCompleteStyle_autocomplete__BvELB input')))

sleep(1.5)  # para aguardar 1,5 segundos antes de escrever na barra

# para escrever 'notebook' na barra de pesquisa e dar ENTER
search_bar.send_keys('notebook')
sleep(1.5)  # para aguardar 1,5 segundos antes de dar ENTER
search_bar.send_keys(Keys.ENTER)

# função para capturar os produtos de uma página
def get_products():
    sleep(3)  # para guardar o carregamento da página
    # para selecionar os produtos pelo seletor apropriado
    products = driver.find_elements(By.CSS_SELECTOR, 'h2[id^="product-card-"]')
    product_data = []

    # para extrair os nomes e links dos produtos
    for product in products:
        name = product.text
        link = product.find_element(By.XPATH, './ancestor::a').get_attribute('href')  # pega o link do produto
        product_data.append((name, link))

    # para verificar o número de produtos encontrados e os nomes capturados
    # print(f"Produtos encontrados: {len(products)}")
    # print("Produtos capturados:")
    # for product in list_products:
    #     print(product)

    return product_data

# função para capturar produtos de todas as páginas
def capture_all_products():
    all_products = []
    
    for page in range(1, 4):  # capturar produtos nas páginas 1, 2 e 3
        print(f"Capturando produtos da página {page}...")
        all_products.extend(get_products())
        
        if page < 3:  # não tentar navegar para uma página além da última
            next_page = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@aria-label, '{page + 1}')]")))
            sleep(1.5)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_page)
            sleep(3)  # para aguardar o carregamento da próxima página
    
    return all_products

# para capturar produtos sem filtro
all_products = capture_all_products()

# para escrever os produtos no arquivo de texto 'products.txt'
with open('products.txt', 'w', encoding='utf-8') as file:
    for i, (product, link) in enumerate(all_products, 1):
        file.write(f"{i}: {product} | {link}\n")


# para voltar à primeira página
driver.get('https://www.zoom.com.br/search?q=notebook&page=1')  # para navegar diretamente para a primeira página da pesquisa

# para alterar o filtro de busca de "mais relevante" para "melhor avaliado"
try:
    filter_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.Select_Select__1HNob')))
    filter_dropdown.click()
    sleep(1.5) # para aguardar o menu suspenso aparecer

    # selecionar a opção com valor 'rating_desc'
    select_element = driver.find_element(By.CSS_SELECTOR, '.Select_Select__1HNob')
    select = Select(select_element)
    select.select_by_value('rating_desc')

    # para capturar os produtos da primeira página com o filtro atualizado
    sleep(1.5)  # para aguardar o carregamento do filtro

    # para capturar produtos filtrados
    all_products_filtered = capture_all_products()

    # para adicionar os produtos filtrados no arquivo 'products_best_rated.txt'
    with open('products_best_rated.txt', 'w', encoding='utf-8') as file:
        for i, (product, link) in enumerate(all_products_filtered, 1):
            file.write(f"{i}: {product} | {link}\n")

except Exception as e:
    print(f"Erro ao aplicar filtro: {e}")


# para voltar à primeira página
driver.get('https://www.zoom.com.br/search?q=notebook&page=1')  # para navegar diretamente para a primeira página da pesquisa

# para alterar o filtro de busca de "melhor avaliado" para "menor preço"
try:
    filter_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.Select_Select__1HNob')))
    filter_dropdown.click()
    sleep(1.5)

    # selecionar a opção com valor 'price_asc'
    select_element = driver.find_element(By.CSS_SELECTOR, '.Select_Select__1HNob')
    select = Select(select_element)
    select.select_by_value('price_asc')

    sleep(1.5)

    all_products_filtered = capture_all_products()

    # para escrever os produtos filtrados no arquivo 'products_lowest_price.txt'
    with open('products_lowest_price.txt', 'w', encoding='utf-8') as file:
        for i, (product, link) in enumerate(all_products_filtered, 1):
            file.write(f"{i}: {product} | {link}\n")

except Exception as e:
    print(f"Erro ao aplicar filtro: {e}")


# função para ler os produtos de um arquivo
def read_products(file_name):
    products = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'(\d+): (.+?) \| (.+)', line.strip())
            if match:
                index, name, link = match.groups()
                products.append((int(index), name, link))
    return products

# função para extrair o nome dos produtos
def extract_product_names(products):
    return {name for _, name in products}

# para ler produtos dos arquivos
best_rated_products = read_products('products_best_rated.txt')
lowest_price_products = read_products('products_lowest_price.txt')

# para extrair os nomes dos produtos
best_rated_data = {name: link for _, name, link in best_rated_products}
lowest_price_data = {name: link for _, name, link in lowest_price_products}

# para encontrar os produtos que estão em ambos os arquivos
common_products = set(best_rated_data.keys()).intersection(lowest_price_data.keys())

# para limitar a 5 produtos
top_5_products = list(common_products)[:5]

print("\nTop 5 produtos:")
for product in top_5_products:
    print(f"{product}: {best_rated_data[product]}")


def get_product_details(product_url):
    driver.get(product_url)
    sleep(3)  # espera o carregamento da página

    try:
        title = driver.find_element(By.CSS_SELECTOR, 'h1').text  # título do produto
        price = driver.find_element(By.CSS_SELECTOR, '.Price_ValueContainer__ndCqK').text  # preço
        specifications = driver.find_elements(By.CSS_SELECTOR, '.Text.MobileLabelS')  # lista de especificações

        specs_text = "\n".join([spec.text for spec in specifications])

        return {
            'title': title,
            'price': price,
            'specifications': specs_text
        }
    except Exception as e:
        print(f"Erro ao extrair detalhes do produto: {e}")
        return None


# para criar um arquivo para salvar as configurações
with open('top_5_product_details.txt', 'w', encoding='utf-8') as details_file:
    for product in top_5_products:
        link = best_rated_data[product]  # link do produto
        details = get_product_details(link)

        if details:
            details_file.write(f"Produto: {details['title']}\n")
            details_file.write(f"Preço: {details['price']}\n")
            details_file.write(f"Especificações:\n{details['specifications']}\n")
            details_file.write("\n" + "="*40 + "\n\n")  # separador entre produtos


sleep(3)
driver.close()
