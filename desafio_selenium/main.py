from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from time import sleep

driver = webdriver.Chrome()
driver.get('https://www.zoom.com.br/')

sleep(1.5)
# para clicar na barra de pesquisa
search_bar = driver.find_element(By.CLASS_NAME, 'AutoCompleteStyle_autocomplete__BvELB')

# para escrever notebook na barra de pesquisa e dar ENTER
input = search_bar.find_element(By.TAG_NAME, 'input')
input.send_keys('notebook')
input.send_keys(Keys.ENTER)

sleep(1.5)
# rolando a página até chegar no final
iframe = driver.find_element(By.CLASS_NAME, 'Paginator_page__LYvDd')
ActionChains(driver).scroll_to_element(iframe).perform()

sleep(1.5)
clicar = driver.find_element(By.ID, 'page-2').click()

sleep(3)
driver.close()
