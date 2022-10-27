import pandas as pd
import re

## precios_semana_20200413.csv

# Had to change encoding of precios_semana_20200413.csv to UTF-8 in the file itself as it wouldn't let me read it with pandas
semana_string = './Datasets relevamiento precios/precios_semana_20200413.csv'
precios413 = pd.read_csv(semana_string)

# Create index for each precio this week
# Also is good to note that separating semanaId and precioId makes queries much faster, if the user wants to only see certain weeks later in the main table
precios413['precioId'] = precios413.index + 1 
# Create index for semanaId
semanaNumber= re.findall('[0-9]+', semana_string)
precios413['semanaId'] = semanaNumber[0]
precios413 = precios413[['semanaId','precioId','producto_id','sucursal_id','precio']]

#export into csv
precios413.to_csv('./Datasets relevamiento precios new/precios_semana_20200413.csv',index=False)

## precios_semanas_20200419_20200426.xlsx
xls = pd.ExcelFile('./Datasets relevamiento precios/precios_semanas_20200419_20200426.xlsx')
precios426 = pd.read_excel(xls, 'precios_20200426_20200426')
precios419 = pd.read_excel(xls, 'precios_20200419_20200419')

semana_string_ab= ['precios_semana_20200419','precios_semana_20200426']

precios_list = [precios419,precios426]

# Create index for each precio this week
# Also is good to note that separating semanaId and precioId makes queries much faster, if the user wants to only see certain weeks later in the main table
for i, week in enumerate (precios_list):
    week['precioId'] = week.index + 1 
    # Create index for semanaId
    semanaNumber= re.findall('[0-9]+', semana_string_ab[i])
    week['semanaId'] = semanaNumber[0]
    week = week[['semanaId','precioId','producto_id','sucursal_id','precio']]

precios426 = precios426[['semanaId','precioId','producto_id','sucursal_id','precio']]
precios419 = precios419[['semanaId','precioId','producto_id','sucursal_id','precio']]

# Replaced every badly inputed value in sucursal_id with 'Sin Dato', because the rest of the information in the row is still relevant
precios419.loc[precios419.sucursal_id.str.contains('00:00:00', na=True), 'sucursal_id'] = 'Sin Dato'

# Replace all scientific notations with the real producto_id
precios426.producto_id = precios426.producto_id.astype('string')
precios426.producto_id = precios426.producto_id.str.rstrip('.0')

precios426.producto_id = precios426.producto_id.str.zfill(13)


#export into csv 
precios426.to_csv('./Datasets relevamiento precios new/precios_semana_20200426.csv',index=False)
precios419.to_csv('./Datasets relevamiento precios new/precios_semana_20200419.csv',index=False)


##precios_semana_20200503.json

semana_string = './Datasets relevamiento precios/precios_semana_20200503.json'
precios503 = pd.read_json(semana_string)

# Create index for each precio this week
# Also is good to note that separating semanaId and precioId makes queries much faster, if the user wants to only see certain weeks later in the main table
precios503['precioId'] = precios503.index + 1 
# Create index for semanaId
semanaNumber= re.findall('[0-9]+', semana_string)
precios503['semanaId'] = semanaNumber[0]
precios503 = precios503[['semanaId','precioId','producto_id','sucursal_id','precio']]


#export into csv 
precios503.to_csv('./Datasets relevamiento precios new/precios_semana_20200503.csv',index=False)