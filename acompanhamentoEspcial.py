import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def login(navegador):
    navegador.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
    time.sleep(8)

    usuario = navegador.find_element(By.XPATH, value='//*[@id="txtUsuario"]')
    usuario.send_keys("fsilva3")
    time.sleep(3)

    senha = navegador.find_element(By.XPATH, value='//*[@id="pwdSenha"]')
    senha.send_keys("Baalimad8*")
    time.sleep(3)

    exercicio = Select(navegador.find_element(By.XPATH, value='//*[@id="selOrgao"]'))
    time.sleep(3)
    exercicio.select_by_visible_text('SEFAZ')
    time.sleep(3)

    btnLogin = navegador.find_element(By.XPATH, value='//*[@id="Acessar"]')
    btnLogin.click()

    time.sleep(10)

    navegador.maximize_window()

def acompanhamentoEspecial(navegador):
    janelaOriginal = navegador.current_window_handle
    barraPadrao = navegador.find_element(By.ID, "divInfraBarraSistemaPadrao")
    barraPadraoD = barraPadrao.find_element(By.ID, "divInfraBarraSistemaPadraoD")
    time.sleep(15)
    trocaCaixa = barraPadraoD.find_element(By.ID, "lnkInfraUnidade")
    print(trocaCaixa)
    if trocaCaixa.text != "SEFAZ/COOEGOE":
        trocaCaixa.click()
        time.sleep(5)
        tabelaSetores = navegador.find_element(By.XPATH, value='//*[@id="divInfraAreaTabela"]')
        rows = tabelaSetores.find_elements(By.TAG_NAME, value="tr")
        for i in range(1, len(rows)):
            col = rows[i].find_elements(By.TAG_NAME, value="td")[1]
            if col.text == "SEFAZ/COOEGOE":
                col.click()
                time.sleep(10)
                break

    divInfraAreaTela = navegador.find_element(By.ID, "divInfraAreaTela")
    divInfraAreaTelaE = divInfraAreaTela.find_element(By.ID, "divInfraAreaTelaE")
    divInfraSidebarMenu = divInfraAreaTelaE.find_element(By.ID, "divInfraSidebarMenu")
    print(divInfraSidebarMenu)
    botoes = divInfraSidebarMenu.find_element(By.TAG_NAME, "li")
    print(botoes)

    for botao in botoes:
        print(botao.text)

if __name__=="__main__":
    navegador = webdriver.Firefox()
    login(navegador)