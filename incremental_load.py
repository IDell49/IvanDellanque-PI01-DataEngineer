import pandas as pd
from sqlalchemy import create_engine
import re

# Load it
df = pd.read_csv('./Datasets relevamiento precios/precios_semana_20200518.txt',delimiter = '|')
df['precioId'] = df.index + 1 
# Create index for semanaId
df['semanaId'] = 20200518
df = df[['semanaId','precioId','producto_id','sucursal_id','precio']]

my_conn = create_engine("mysql://root:{clave}@{address}/{db}".format(address='localhost',clave='H7TZ_4mQSb9Ec6_uD4u',db='pi_01_dataengineer'))
df.to_sql(con=my_conn, name='precios_semana', if_exists='append', index=False)