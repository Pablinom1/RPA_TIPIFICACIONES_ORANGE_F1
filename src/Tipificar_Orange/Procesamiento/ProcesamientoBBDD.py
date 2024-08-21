import pyodbc
import logging
from datetime import datetime
import pandas  as pd



#configuracion de la conexion a SQL Server
def get_db_connection(data):
    try:
        logging.info("Inicia Conexion bbdd")
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
        return conexionexitosa
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
           
    


# Función para obtener registros de la base de datos
def get_records_from_db(data):
    logging.info("Inicia Conexion bbdd")
    try:      
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
       
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
        
    

    try:
        # Consulta SQL para obtener 50 registros
        if conexionexitosa == True:
            cursor = conn.cursor()
             # Llamar al procedimiento almacenado        
            cursor.execute("{CALL NumCaso_f1}")                
            # Obtener los resultados        
            rows = cursor.fetchall()         
                  
            if rows != 0:
                #TableResult = """select TOP 50(*)  from RPA_SIEBEL_f1 where Fecha_Siebel is null and telefono<>'' and Cuscode<>''  and  IDStado=2 and fecha>='2023-06-06'"""
                fechainicio = datetime.now()
                valores =(fechainicio,'N')
                sql_update_query = """update notificar set Ultima_Fecha= ?, notificado= ?"""
                cursor.execute(sql_update_query,valores)
                conn.commit()
                #cursor.execute("{CALL ClientesBajaCodSiebel_f1}")   
                #rows_ = cursor.fetchall() 
                cursor.execute("""select TOP 50 ID,Fecha,Cuscode,Tipo,Telefono,Comentarios,Fecha_Siebel,Observaciones,IDEjecucion,IdStado,Reintentos,FechaInicioRPA  from RPA_SIEBEL_f1 where Fecha_Siebel is null and telefono !='' and Cuscode !=''  and  IDStado=2 and Fecha>='2024-08-08'""")
                rows = cursor.fetchall()
                # Convertir a una lista de diccionarios
                records = [{"ID": row.ID, "Fecha": row.Fecha, "Cuscode": row.Cuscode, "Tipo": row.Tipo, "Telefono": row.Telefono, "Comentarios": row.Comentarios, "Fecha_Siebel": row.Fecha_Siebel, "Observaciones": row.Observaciones, "IDEjecucion": row.IDEjecucion, "IdStado": row.IdStado, "Reintentos": row.Reintentos, "FechaInicioRPA": row.FechaInicioRPA} for row in rows]
                #for record in records:
                #    print(f"tipo de record: {type(record)}")
                return records    

    except pyodbc.Error as e:
        logging.error(f"Error al ejecutar la consulta: {e}")
        records = []

    finally:
        cursor.close()
        conn.close()

#update a la base de datos
def UpdateregistroKO(record,data,comen,ID):
    logging.info("Inicia Conexion bbdd")
    try:
        
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
       
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
    try:         
        if conexionexitosa == True:
            cursor = conn.cursor()
            fechainicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Observaciones = comen
            Id_estado = "3"
            id_valor = record["ID"]
            sql_update_query = """update RPA_SIEBEL_f1 set Fecha_Siebel=CONVERT(datetime,?,120), Observaciones= ?, IdStado= ? WHERE ID =? """
            cursor.execute(sql_update_query,(fechainicio,Observaciones,Id_estado,ID))
            conn.commit()
            updateExitoso= True

    except Exception as e:
        updateExitoso = False
        logging.error("Error Conexion bbdd" +str(e))
        return updateExitoso     

#update OK
def UpdateregistroOK(record,data,comen,ID):
    logging.info("Inicia Conexion bbdd")
    try:
        
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
       
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
    try:         
        if conexionexitosa == True:
            cursor = conn.cursor()
            fechainicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Observaciones = "OK"
            Id_estado = "10"
            id_valor = record["ID"]
            sql_update_query = """update RPA_SIEBEL_f1 set Fecha_Siebel=CONVERT(datetime,?,120), Observaciones= ?, IdStado= ? WHERE ID =? """
            cursor.execute(sql_update_query,(fechainicio,Observaciones,Id_estado,ID))
            conn.commit()
            updateExitoso= True

    except Exception as e:
        updateExitoso = False
        logging.error("Error Conexion bbdd" +str(e))
        return updateExitoso     




def UpdateregistroInicio(record,data,comen,ID):
    logging.info("Inicia Conexion bbdd")
    try:
        
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
       
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
    try:         
        if conexionexitosa == True:
            cursor = conn.cursor()
            fechainicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Observaciones = ""
            Id_estado = ""
            id_valor = record["ID"]
            sql_update_query = """update RPA_SIEBEL_f1 set FechaInicioRPA=CONVERT(datetime,?,120), Observaciones= ?, IdStado= ? WHERE ID =? """
            cursor.execute(sql_update_query,(fechainicio,Observaciones,Id_estado,ID))
            conn.commit()
            updateExitoso= True

    except Exception as e:
        updateExitoso = False
        logging.error("Error Conexion bbdd" +str(e))
        return updateExitoso

def UpdateregistroNoEncotrado(record,data,comen,ID):
    logging.info("Inicia Conexion bbdd")
    try:
        
        print(pyodbc.drivers())    
        print(pyodbc.dataSources())
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+data["Server"]+';'
                                'DATABASE='+data["Database"]+';'
                                'UID='+data["usuarioBBDD"]+';'
                                'PWD='+data["PasswordBBDD"])
        conexionexitosa = True
       
    except pyodbc.Error as e:
        conexionexitosa = False
        logging.error("Error Conexion bbdd" +str(e))
        return conexionexitosa
    try:         
        if conexionexitosa == True:
            cursor = conn.cursor()
            fechainicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Observaciones = "KO"
            Id_estado = "5"
            id_valor = record["ID"]
            sql_update_query = """update RPA_SIEBEL_f1 set Fecha_Siebel=CONVERT(datetime,?,120), Observaciones= ?, IdStado= ? WHERE ID =? """
            cursor.execute(sql_update_query,(fechainicio,Observaciones,Id_estado,ID))
            conn.commit()
            updateExitoso= True

    except Exception as e:
        updateExitoso = False
        logging.error("Error Conexion bbdd" +str(e))
        return updateExitoso     





