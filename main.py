import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import logging

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

def acompanhamentoEspecial(navegador, numBloco = "506041", tipoAcc = "FIANÇA E VALOR APREENDIDO", tipoBloco = "Assinatura"):
    logging.basicConfig(level=logging.INFO, filename="log.log",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    barraPadrao = navegador.find_element(By.ID, "divInfraBarraSistemaPadrao")
    barraPadraoD = barraPadrao.find_element(By.ID, "divInfraBarraSistemaPadraoD")
    time.sleep(5)
    trocaCaixa = barraPadraoD.find_element(By.ID, "lnkInfraUnidade")
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
    pesquisaBloco = navegador.find_element(By.ID, "txtInfraPesquisarMenu")
    pesquisaBloco.send_keys("Blocos")
    pesquisaBloco.send_keys(Keys.ENTER)
    time.sleep(5)
    divInfraAreaTelaE = navegador.find_element(By.ID, "divInfraAreaTelaE")
    itens = divInfraAreaTelaE.find_elements(By.TAG_NAME, "li")
    for item in itens:
        if item.text=="Blocos":
            item.click()
            time.sleep(5)
            break
    submenu = divInfraAreaTelaE.find_elements(By.TAG_NAME, "li")
    for menu in submenu:
        if menu.text==tipoBloco:
            menu.click()
            time.sleep(5)
            break
    pesquisaBloco = navegador.find_element(By.ID, "txtPalavrasPesquisaBloco")
    pesquisaBloco.send_keys(numBloco)
    pesquisaBloco.send_keys(Keys.ENTER)
    time.sleep(5)

    divInfraAreaTabela = navegador.find_element(By.ID, "divInfraAreaTabela")
    tblBlocos = divInfraAreaTabela.find_element(By.ID, "tblBlocos")
    blocos = tblBlocos.find_elements(By.TAG_NAME, "td")
    for bloco in blocos:
       if bloco.text == numBloco:
           bloco.click()
           time.sleep(5)
           break
    divInfraAreaTabela = navegador.find_element(By.ID, "divInfraAreaTabela")
    tblProtocolosBlocos = divInfraAreaTabela.find_element(By.ID, "tblProtocolosBlocos")
    listProcessos = tblProtocolosBlocos.find_elements(By.TAG_NAME, "tr")
    for i in range(1,len(listProcessos)):
        try:
            time.sleep(5)
            itensTbl = listProcessos[i].find_elements(By.TAG_NAME, "a")
            processo = itensTbl[1].text
            for item in itensTbl:
                if item.get_attribute('href') is not None:
                    item.click()
                    break
            time.sleep(5)
            processoAberto = navegador.window_handles[1]
            navegador.switch_to.window(processoAberto)
            conteudoTelaProcesso = navegador.find_element(By.ID, "divInfraAreaTela")
            iframeVisualizacao = conteudoTelaProcesso.find_element(By.ID, "ifrVisualizacao")
            iframeArvore = conteudoTelaProcesso.find_element(By.ID, "ifrArvore")
            navegador.switch_to.frame(iframeArvore)
            time.sleep(5)
            topmenu = navegador.find_element(By.ID, "topmenu")
            itensTopMenu = topmenu.find_elements(By.TAG_NAME, "img")
            accEspecial = False
            for item in itensTopMenu:
                if item.get_attribute('title') == '1 Acompanhamento Especial':
                    accEspecial = True
                    break
            if accEspecial == False:
                time.sleep(5)
                listaDocs = navegador.find_element(By.ID, "divArvore")
                docs = listaDocs.find_elements(By.TAG_NAME, "a")
                for doc in docs:
                    if re.search("Despacho sobre Autorização de Despesa", doc.text) is not None:
                        doc.click()
                        time.sleep(5)
                        navegador.switch_to.default_content()
                        ifrVisualizacao = navegador.find_element(By.ID, "ifrVisualizacao")
                        navegador.switch_to.frame(ifrVisualizacao)
                        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
                        corpoTexto.click()
                        ifrArvoreHtml = navegador.find_element(By.ID, 'ifrArvoreHtml')
                        navegador.switch_to.frame(ifrArvoreHtml)
                        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
                        corpoTexto.click()
                        paragrafos = navegador.find_elements(By.TAG_NAME, 'p')
                        for par in paragrafos:
                            if re.search("Processo:", par.text) is not None:
                                numProcesso = par.text
                            if re.search("Beneficiário:", par.text) is not None:
                                beneficiario = par.text
                            if re.search("Forma de Pagamento:", par.text) is not None:
                                pagamento = par.text
                        navegador.switch_to.default_content()
                        navegador.switch_to.frame(ifrVisualizacao)
                        divArvoreAcoes = navegador.find_element(By.ID, 'divArvoreAcoes')
                        botoes = divArvoreAcoes.find_elements(By.TAG_NAME, 'img')
                        for botao in botoes:
                            if botao.get_attribute('title') == "Acompanhamento Especial":
                                botao.click()
                                break
                        time.sleep(5)
                        try:
                            btnAdicionar = navegador.find_element(By.ID, "btnAdicionar")
                            btnAdicionar.click()
                        except:
                            None
                        time.sleep(5)
                        selGrupoAcompanhamento = Select(navegador.find_element(By.ID, "selGrupoAcompanhamento"))
                        time.sleep(5)
                        selGrupoAcompanhamento.select_by_visible_text(tipoAcc)
                        txaObservacao = navegador.find_element(By.ID, "txaObservacao")
                        txaObservacao.send_keys(numProcesso)
                        txaObservacao.send_keys(Keys.ENTER)
                        time.sleep(5)
                        txaObservacao.send_keys(beneficiario)
                        txaObservacao.send_keys(Keys.ENTER)
                        time.sleep(5)
                        txaObservacao.send_keys(pagamento)
                        txaObservacao.send_keys(Keys.ENTER)
                        time.sleep(5)
                        infraButton = navegador.find_elements(By.CLASS_NAME, "infraButton")
                        for botao in infraButton:
                            if botao.get_attribute('name') == "sbmCadastrarAcompanhamento":
                                botao.click()
                                break
                        time.sleep(5)
                        logging.info(f"O processo {processo} teve o acompanhamento especial incluído")
                        navegador.close()  # Fecha a janela 2 [1]
                        navegador.switch_to.window(navegador.window_handles[0])
            else:
                logging.info(f"O processo {processo} já possuía o acompanhemnto especial cadastrado")
                navegador.close()  # Fecha a janela 2 [1]
                navegador.switch_to.window(navegador.window_handles[0])
        except:
            logging.info(f"Não foi possível acessar o {processo}")
            navegador.switch_to.window(navegador.window_handles[0])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    navegador = webdriver.Firefox()
    login(navegador)
    acompanhamentoEspecial(navegador)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
