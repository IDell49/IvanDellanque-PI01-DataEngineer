import pandas as pd
import unidecode  as und

producto = pd.read_parquet('./Datasets relevamiento precios/producto.parquet')

print(producto[producto.duplicated()])
producto.info()

# We Have to take care of extra columns, as they more than 99% of the it as Null we can get rid of categoria1,2,3
#but it's always good practice to keep the outliers somewhere safe
productosConCategoria = producto.loc[(producto['categoria1'].notnull()) | (producto['categoria2'].notnull()) | (producto['categoria3'].notnull())]
producto.drop(['categoria1','categoria2','categoria3'],inplace=True,axis=1)

# Clean up producto for redundant information
# nombre has presentacion at the end of the string, so we split it
producto['nombre'] = producto['nombre'].str.rsplit(' ', 2).str[0]
# there are 2 None rows that have no particular useful information, they seem like a mistake
producto.dropna(inplace=True)

# let's get rid of marca in the product's name, first:
#1) make a new marca name column so we can keep old names, and at the same time have it be capitalized in the same manner as nombre 
producto['marca_st'] = producto.apply((lambda i : und.unidecode(str(i['marca']).lower())), axis=1)
#2) change nombre to a capitalized standard
producto['nombre'] = producto['nombre'].str.strip().str.capitalize()
#3) strip the marca name from product name
producto['nombre'] = producto.apply(lambda i: i['nombre'].replace(str(i['marca_st']),''), axis=1) 

# Make marca table:
#1) get marca uniques
marca = producto.marca.drop_duplicates()
#3) Reset index and then create a new Id for marcaId
marca = marca.reset_index().drop('index', axis =1)
marca['marcaId'] = marca.index + 1
#4) Reorganize the columns 
marca = marca[['marcaId','marca']]
#5) replace marca with marcaId on main table producto
producto = producto.merge(marca, left_on=['marca'], right_on=['marca'])
producto = producto[['id','marcaId','nombre','presentacion']]
#6) Here we get rid of all latin accents in marca name
marca['marca'] = marca.apply((lambda i : und.unidecode(str(i['marca']))), axis=1)


#Export into csv files:
producto.to_csv('./Datasets relevamiento precios new/producto.csv',index=False)
marca.to_csv('./Datasets relevamiento precios new/marca.csv',index=False)