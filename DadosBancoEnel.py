from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

import requests
import time
import json
import pandas as pd


#Resgatar valores da planilha

#header = ['CLIENTE','CNPJ'] #Quando não tiver cabeçalho
#acesso = pd.read_csv('acesso.csv',header=None,names=header,index_col=0)

acesso = pd.read_csv('acesso.csv')
acesso.head()

cliente = acesso["CLIENTE"]
cnpj = acesso["CNPJ"]

###################################

#Variaveis

################################### 

url = "https://www.eneldistribuicao.com.br/ce/loginAcessoRapidopagamento.aspx"
#binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe')


#Escrever resultado no .txt
#page = requests.get(url)
#result = page.status_code

#with open('status.txt','w') as f:
 #f.write(format(result))
###################################

driver.get(url)

#Realizando Login
login = driver.find_element_by_id("CONTENT_Formulario_NumeroCliente")
login.clear()
login.send_keys(cliente.to_string())
login.send_keys(Keys.RETURN)
time.sleep(3)

password = driver.find_element_by_id("CONTENT_Formulario_Documento")
password.clear()
password.send_keys(cnpj.to_string())
password.send_keys(Keys.RETURN)
time.sleep(15)

#Resgatando informações da tabela.
dadostabela = driver.find_element_by_id('CONTENT_Formulario_GridViewSegVia')
html_content = dadostabela.get_attribute('outerHTML')

#Estruturando o HTML
soup = BeautifulSoup(html_content,'html.parser')
tabela = soup.find(id='CONTENT_Formulario_GridViewSegVia')

dataframe = pd.read_html( str(tabela) )[0].head(2)

#click no checkbox
#driver.find_element_by_xpath(
#"//table[@id='CONTENT_Formulario_GridViewSegVia']//thead//tbody//tr//td//span[@class='big-size-cb']//input[@id='CONTENT_Formulario_GridViewSegVia_CheckFatura_0']").click()

###################################

driver.quit()








