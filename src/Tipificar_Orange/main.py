import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timedelta
import logging
import json
from time import sleep
from Procesamiento import *
import os.path as path
from os import remove
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service as ChromeService
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import random
import os

 
def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - timedelta(days=1)
 
def process_records_in_thread(data, batch,thread_id,username,password):
    print(f"Inicio Hilo {thread_id} con {len(batch)} registros")
    logging.info(f"Inicio Hilo {thread_id} con {len(batch)} registros")
    # Configuración del navegador
    #chrome_options = Options()
    # user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")     
    # profile_path = os.path.join(user_data_dir, "Default")
    # chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    # chrome_options.add_argument(f"profile-directory={profile_path}") 
    #chrome_options.add_argument(f"user-data-dir=C:\\Users\\RPARPRO03\\AppData\\Local\\Google\\Chrome\\User Data")
    #chrome_options.add_argument("profile-directory=Default")
    #user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")     
    #profile_path = os.path.join(user_data_dir, "Default")

    #chrome_options.add_argument("--no-first-run")     
    # chrome_options.add_argument("--no-default-browser-check")     
    # chrome_options.add_argument("--disable-default-apps") 
    # chrome_options.add_argument("--disable-extensions")
 
    #driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome() 
    # Ruta al EdgeDriver
    edge_driver_path = 'C:\\Users\\RPARPRO03\\Documents\\Python\\RPA_TIPIFICACIONES_ORANGE_F1\\resources\\drivers\\edgedriver_win32\\msedgedriver.exe'
    
    # Configuración de opciones para Edge
    edge_options = EdgeOptions()
    #edge_options.add_argument('--inprivate')
    edge_options.add_argument('--start-maximized')  # Abrir la ventana maximizada
    
    # Crear una instancia del servicio de Edge
    edge_service = EdgeService(executable_path=edge_driver_path)
    
    # Iniciar el navegador Edge
    driver = webdriver.Edge(service=edge_service, options=edge_options)
    
    # Acceder a una página web
    #driver.get(data["url"])
    # Navegar a la página deseada
    #driver.maximize_window()

 
    try:
        # Iniciar sesión una vez por hilo
        Login(driver, data,username,password) 
        # Procesar cada registro dentro de la misma sesión
        for record in batch:
            print(f"Hilo {thread_id} porcesando registro: {record["Telefono"]}")
            fill_form(record,data,driver)
 
    finally:
        # Cerrar el navegador
        driver.quit()

def main():
        
    while True:
        try:
            # Abrir archivo json de parámetros
            with open('C:\\Users\\RPARPRO03\\Documents\\Python\\RPA_TIPIFICACIONES_ORANGE_F1\\src\\config.json', 
            encoding='utf-8') as json_file:
                data = json.load(json_file)
            credentials=[
                {"username": data['user1'], "password": data['pass1']},
                {"username": data['user2'], "password": data['pass2']}
            ]
            current_date = datetime.today().strftime('%d-%m-%Y')
            logging.basicConfig(filename=data["ruta_logs"]+current_date+'.txt', 
                                filemode='a', format='%(asctime)s %(levelname)-8s %(message)s',
                                level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
            logging.info("Inicia ejecución RPA Tipificaciones F1")
            records = get_records_from_db(data)

            if not records:
                logging.info("Sin registros esperando antes de reintentar .... RPA Tipificaciones F1")
                print("Sin registros esperando antes de reintentar .... RPA Tipificaciones F1")
                sleep(60)
                continue
            # Usar ThreadPoolExecutor para manejar múltiples hilos
            num_threads = 2
            batch_size = len(records) // num_threads

            record_batches = [records[i:i + batch_size] for i in range(0,len(records),batch_size)]
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Enviar tareas a los hilos
                for i, batch in enumerate(record_batches):
                    creds = credentials[i % len(credentials)]
                    executor.submit(process_records_in_thread,data,batch,i,creds['username'],creds['password'])
            logging.info("Finaliza ejecución Tipificaciones Orange F1")
            executor.shutdown(wait=True)

            logging.info("Finaliza ejecución Tipificaciones Orange F1")
            
        except Exception as e:
            print("error"+str(e))
            logging.error("Error main"+ str(e)) 
            sleep(30)

if __name__ == '__main__':
    main()
 