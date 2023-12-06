# Import required libraries
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import URL

# Extract data from mysql
def extract(tbl_name):
    try: 
        conn = mysql.connector.connect(
                    user = 'root', 
                    password = 'password',
                    host = 'localhost',
                    database = 'test_db')
        cursor = conn.cursor()
        cursor.execute(f'select * from {tbl_name}')
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        return df
        
    except Exception as e:
        print("Data Extract error " + str(e))
        
    finally:
        cursor.close()
        conn.close()
        print('Data Extract Succes')
        
 # Trasform data       
def transform(data):
    data.columns = data.columns.str.replace(' ', '_')
    data.rename(columns=lambda x: x.lower(), inplace=True)
    data.drop_duplicates(inplace=True)
    data.dropna(inplace=True)
    print("Data Succesfull Transform")
 

#load data to postgres
def load(data, tbl_name):
    url_postgres = URL.create(
        drivername="postgresql",
        username="postgres",
        password="Pangrib14",  
        host="localhost",
        port="5432",
        database="belajar")
    enginepstgres = create_engine(url_postgres)
    rows_loaded = 0
    print(f'Loading rows {rows_loaded} to {rows_loaded + len(data)}')
    data.to_sql(f"{tbl_name}", enginepstgres, if_exists='replace', index=False)
    rows_loaded += len(data)
    print("Data Succesful load")


if __name__ == "__main__":
    data = extract('rakamin_order')
    transform(data)
    load(data, 'rakamin_order_new')
    
    

    

    
