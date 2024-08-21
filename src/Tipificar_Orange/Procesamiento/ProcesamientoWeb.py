from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import logging
from datetime import datetime
#from selenium.webdriver.chrome.service import Service as ChromeService
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import re
from datetime import datetime, timedelta
from Procesamiento.ProcesamientoBBDD import *
import time


def Login(driver,data,username,password):   

    # URL de la página web de inicio de sesión
    try: 
            # Abrir pagina orange y loguearse
            
            # Crear una instancia de las opciones de Chrome
            #print(f"tipo de record: {type(record)}")
            #print(f"contenido de 'record': {record}")
            logging.info("Inicia Logueo Orange")
            driver.get(data["url"])
            #driver.get("https://fichadecliente.si.orange.es")
            #driver.refresh()
            try:
                search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'o-comp__headerBlock--btn')]")))             
                search_button.click()
                #//button[contains(@class, 'o-comp__headerBlock--btn')]
            except Exception as e:
                print("No esta logado")
            username_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='temp-username']")))
            username_field.send_keys(username)
            password_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='temp-password']")))
            password_field.send_keys(password)
            login_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"submit-button")))
            login_button.click()
            LogueoExitoso = True
            logging.info("Finaliza Logueo Orange")
    except Exception as e:
            LogueoExitoso = False
            logging.error("Error en el Logueo Orange: " + str(e))    


# Función para llenar el formulario web con un registro
def fill_form(record,data,driver):   
    try:       
        LogueoExitoso= True
        existeFacturas = False
        if LogueoExitoso ==True:
            # Navegar a la página del formulario
            # ingresar Telefono   
            logging.info("Procesando Registro "+ str(record["Telefono"])) 
            print(record)
            ID = record["ID"]
            comen = ""
            UpdateregistroInicio(record,data,comen,ID)       
            if isinstance(record,dict):
                phone_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'o-comp__locator--text') and contains(@name, 'locatorCtrl.inputMsisdn')]")) )
                phone_field.clear()
                phone_field.send_keys(record["Telefono"])
                search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscar')]")))             
                search_button.click()
                # Llenar el formulario con los datos del registro
                sleep(4)
                
                try:
                    existeFacturas = False
                    # Esperar hasta que el documento esté listo
                    boolclienteNoExiste = False  
                    WebDriverWait(driver, 10).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete'
                    )
                    elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'error-message')]/div[@class='ng-binding']") 
                    if len(elements) > 1:  
                        error_message_text = elements[1].text   
                        
                    if error_message_text.__contains__("Cliente Pyme"):
                        print("realizar update a siebele F2")
                        ID = record["ID"]
                        comen = "OK"
                        UpdateregistroNoEncotrado(record,data,comen,ID)
                        boolclienteNoExiste = True  
                    if error_message_text.__contains__("No se han encontrado"):
                        print("realizar update a siebele F2")
                        ID = record["ID"]
                        comen = "OK"
                        UpdateregistroNoEncotrado(record,data,comen,ID) 
                        boolclienteNoExiste = True  
                
                except Exception as e:
                    # Maneja el caso donde el elemento no está presente
                    print("El mensaje de error no está presente en la página." + str(e))
                #Validar popup  
                try:
                    WebDriverWait(driver, 10).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete'
                    )
                except Exception as e:
                    logging.info("no cargo la pagina" + str(e))             
                if boolclienteNoExiste == False:
                    try:
                        wait = WebDriverWait(driver, 12)
                        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='undefined']/div/div/div/div[2]/div/div/div/div/div[5]")))
                        time.sleep(4)
                        num_elements = len(elements)
                        print(f"Se encontraron {num_elements} elementos.")
                        for i in range(num_elements):
                            elements =wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='undefined']/div/div/div/div[2]/div/div/div/div/div[5]")))
                            wait.until(EC.element_to_be_clickable(elements[i]))
                            elements[i].click()
                        #existe_pop = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='undefined']/div/div/div/div[2]/div/div/div/div/div[5]")))             
                        #existe_pop.click()
                        existe_btncerrar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary')))
                        existe_btncerrar.click()
                    except Exception as e:
                        logging.error("no tiene pop up"+str(e))  

                    try:
                        wait = WebDriverWait(driver, 2)
                        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cerrar')]")))
                        close_button.click()    
                        print("Botón 'Cerrar' clickeado exitosamente.")
                    except Exception as e:
                        print(f"Error al intentar hacer clic en el botón 'Cerrar': {e}")    
                    # region facturas
                    try:
                        #Seleccionar factura
                        sleep(2)
                        # Esperar a que la tabla esté presente en la página
                        
                        cell = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, 'tooltips-example'))
                        )
                    
                        # Scroll para asegurarse de que la tabla está en la vista
                        #driver.execute_script("arguments[0].scrollIntoView();", table)
                    
                        # Localizar la celda de la tabla que contiene el símbolo '€' y hacer clic
                        cell = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//td[span/strong[contains(text(), '€')]]"))
                        )
                        cell.click()
                        existeFacturas = True
                    except Exception as e:
                        existeFacturas = False
                        logging.error("no tiene facturas pendientes"+str(e))
                    # end region facturas    
                    try:
                        if existeFacturas==True:        
                            #seleccionar Caso
                            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                            buttonCaso = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Casos")]')) )
                            buttonCaso.click()
                            #seleccionar Nuevo caso
                            buttonNuevoCaso = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Nuevo caso")]')) )
                            buttonNuevoCaso.click()
                            #Proceso Select Canal de contacto
                            select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Canal de contactoundefined')))
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text('Llamada')
                            #Proceso Select saliente o entrante
                            if (record.get("Tipo") == "AVAYA") or (record.get("Tipo") == "Entrante") or (record.get("Tipo") == "BACKOFFICE") :
                                record["Tipo"] = "INTERACCION ENTRANTE"
                            if (record.get("Tipo") == "Saliente") or (record.get("Tipo") == "Gestion Sin Llamada"):
                                record["Tipo"] = "INTERACCION SALIENTE"    
                            if record.get("Tipo") == "WHATSAPP":
                                record["Tipo"] = "INTERACCION ENTRANTE"    
                            try:
                                #Seleccionar Tipo
                                select_element_tipo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'TipoINTERACCION ENTRANTE')))
                                # Crear un objeto Select para el <select> encontrado
                                select_tipo = Select(select_element_tipo)
                                # Seleccionar la opción por texto visible
                                select_tipo.select_by_visible_text(record["Tipo"])
                            except Exception as e:
                                logging.info("Erro en seleccioanr Tipo" + str(e))
                            #Seleccionar Razon 1
                            select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Razón 1undefined')))
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text("RECOBRO")
                            #Seleccionar Razon 2
                            select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Razón 2null')))
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text("INCIDENCIA")
                            #Seleccionar Razon 3
                            select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Razón 3null')))
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text("RECOBRO")

                            #Seleccionar Solucion
                            select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Soluciónnull')))
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text("ON LINE:EXPLICACION")
                            #Seleccionar Producto
                            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Productoundefined')))
                            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", select_element)    
                            # Esperar hasta que el <select> sea visible después del desplazamiento    
                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Productoundefined')) )
                            # Crear un objeto Select para el <select> encontrado
                            select = Select(select_element)
                            # Seleccionar la opción por texto visible
                            select.select_by_visible_text("TARIFA")

                            #Escribir en Comentarios 
                            print(record["Comentarios"])
                            comentario = record["Comentarios"] 
                            ajustar_comentario(comentario)
                            Texto_cliente = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='case-text']/div/textarea")) )
                            Texto_cliente.send_keys(comentario)
                            button_Guardar_Cerrar = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"create-case-save")))
                            button_Guardar_Cerrar.click()
                            sleep(3)
                            
                            try:
                                # Esperar a que el elemento esté visible en la página
                                popup = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'message-relevant success')]"))
                                )

                                # Localizar el botón de cierre dentro del elemento emergente
                                close_button = popup.find_element(By.XPATH, ".//button[@class='btn-close']")
                            
                                # Hacer clic en el botón de cierre
                                close_button.click()
                                button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Cambiar cliente']")))
                                # Hacer clic en el botón
                                button.click()
                                procesoOK=True
                            except Exception as e:
                                logging.info("No encontro el popup" + str(e))
                                procesoOK=False
                                driver.back()
                                driver.get(data["url"])
                                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Cambiar cliente']")))
                                    
                           
                        else:
                            driver.back()
                            driver.get(data["url"])
                            try:
                                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Cambiar cliente']")))
                                # Hacer clic en el botón
                                button.click()
                            except Exception as e:
                                print("No hay boton cambiar cliente")
                        
                            procesoOK = False
                    except Exception as e:
                        driver.back()
                        driver.get(data["url"])
                        #driver.refresh()
                        procesoOK=False
                        #driver.back()
                        print("fallo"+str(e))    
            
                    # update todo OK
                    if procesoOK == True:
                        logging.info("Proceso OK =  True realizar update")  
                        #update 
                        try:
                            ID = record["ID"]
                            comen = "OK"
                            UpdateregistroOK(record,data,comen,ID)
                        except Exception as e:
                            procesoOK=False
                            print("fallo update"+str(e))    
                    else:
                        logging.info("Proceso KO =  False realizar update")
                        try:
                            ID = record["ID"]
                            comen = "KO"
                            UpdateregistroKO(record,data,comen,ID)
                        except Exception as e:
                            procesoOK=False
                            print("fallo update KO"+str(e))    
                            sleep(5)
    except Exception as e:
        print(f"Error al llenar el formulario para {['name']}: {e}")
        logging.error(f"Error al llenar el formulario " +str(e))
        driver.refresh()

def ajustar_comentario(comentario):
    # Expresión regular para encontrar fechas en formato YYYY/MM/DD
    patron_fecha = r"(\d{4}/\d{2}/\d{2})"
    # Buscar todas las fechas en el comentario
    fechas = re.findall(patron_fecha, comentario)
 
    # Si se encuentra una fecha, ajustar la primera encontrada
    if fechas:
        for fecha in fechas:
            # Convertir la cadena de fecha a un objeto datetime
            fecha_obj = datetime.strptime(fecha, "%Y/%m/%d")
 
            # Restar 2 días a la fecha
            nueva_fecha_obj = fecha_obj - timedelta(days=2)
 
            # Convertir la nueva fecha de vuelta a cadena
            nueva_fecha = nueva_fecha_obj.strftime("%Y/%m/%d")
 
            # Reemplazar la fecha original con la nueva fecha
            comentario = comentario.replace(fecha, nueva_fecha, 1)  # Solo reemplaza la primera aparición
    return comentario


