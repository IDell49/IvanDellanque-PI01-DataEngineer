import pandas as pd
import unidecode  as und


#Import the file and see columns + rows
sucursal = pd.read_csv('./Datasets relevamiento precios/sucursal.csv')
sucursal.head()

#See if it has any null values
sucursal.info()

#Create tables for repeated string values to increase query time:
# first let's start with comercioId+banderaId:
#1) Grab relevant columns for new table
comercio_bandera = sucursal[['comercioId','banderaId','banderaDescripcion','comercioRazonSocial']]
#2) Drop the duplicates as they are the exact reason we're creating this table, then sort to keep things tidy
comercio_bandera = comercio_bandera.drop_duplicates(['banderaDescripcion','comercioRazonSocial'])
comercio_bandera.sort_values(['comercioId','banderaId'],inplace=True)
#3) Reset index and then create a new Id to group up comercioId + BanderaId 
comercio_bandera = comercio_bandera.reset_index().drop('index', axis =1)
comercio_bandera['comercioBanderaId'] = comercio_bandera.index + 1
#4) Reorganize the columns and leave out the redundant ones
comercio_bandera = comercio_bandera[['comercioBanderaId','banderaDescripcion','comercioRazonSocial']]
#5) Lastly, replace ['comercioId','banderaId','banderaDescripcion','comercioRazonSocial'] with comercioBanderaId on main table sucursal
sucursal = sucursal.merge(comercio_bandera, left_on=['comercioRazonSocial','banderaDescripcion'], right_on=['comercioRazonSocial','banderaDescripcion'])

sucursal = sucursal[['id','comercioBanderaId','provincia','localidad','direccion','lat','lng','sucursalNombre','sucursalTipo']]

# Then sucursalTipo:
#1) Grab relevant columns for new table
sucursalTipo = sucursal['sucursalTipo']
#2) Drop the duplicates, then sort to keep things tidy
sucursalTipo = sucursalTipo.drop_duplicates()
#3) Reset index and then create a new Id for sucursal
sucursalTipo = sucursalTipo.reset_index().drop('index', axis =1)
sucursalTipo['sucursalTipoId'] = sucursalTipo.index + 1
#4) Rearange columns to keep things tidy
sucursalTipo = sucursalTipo[['sucursalTipoId','sucursalTipo']]
#5) Change sucursal
sucursal = sucursal.merge(sucursalTipo, left_on=['sucursalTipo'], right_on=['sucursalTipo'])
sucursal.drop('sucursalTipo',axis=1, inplace=True)

# Then localidad:
provinciaLocalidad = sucursal
#1) Grab relevant columns for new table
provinciaLocalidad = sucursal[['provincia','localidad']]
#2) Drop the duplicates as they are the exact reason we're creating this table, then sort to keep things tidy
provinciaLocalidad = provinciaLocalidad.drop_duplicates()
provinciaLocalidad.sort_values(['provincia','localidad'],inplace=True)
#3) Reset index and then create a new Id to group up comercioId + BanderaId 
provinciaLocalidad = provinciaLocalidad.reset_index().drop('index', axis =1)
provinciaLocalidad['provinciaLocalidadId'] = provinciaLocalidad.index + 1
#4) Reorganize the columns and leave out the redundant ones
provinciaLocalidad = provinciaLocalidad[['provinciaLocalidadId','provincia','localidad']]
#5) replace ['comercioId','banderaId','banderaDescripcion','comercioRazonSocial'] with comercioBanderaId on main table sucursal
sucursal = sucursal.merge(provinciaLocalidad, left_on=['provincia','localidad'], right_on=['provincia','localidad'])
sucursal = sucursal[['id','comercioBanderaId','provinciaLocalidadId','direccion','lat','lng','sucursalNombre','sucursalTipoId']]
#6) Lastly, replace provincia with provinciaId to, again, reduce redundancy
#6.1)
provincia = provinciaLocalidad[['provincia']]
#6.2)
provincia = provincia.drop_duplicates()
#6.3)
provincia = provincia.reset_index().drop('index', axis =1)
provincia['provinciaId'] = provincia.index + 1
#6.4)
provincia = provincia[['provinciaId','provincia']]
#6.5)
provinciaLocalidad = provinciaLocalidad.merge(provincia, left_on=['provincia'], right_on=['provincia'])
provinciaLocalidad.drop('provincia',axis=1, inplace=True)
provinciaLocalidad = provinciaLocalidad[['provinciaLocalidadId','provinciaId','localidad']]

#now we rearrange the columns to have it look nice
sucursal = sucursal[['id','sucursalNombre','comercioBanderaId','sucursalTipoId','provinciaLocalidadId','direccion','lat','lng']]
sucursal = sucursal.rename({'lat':'latitud', 'lng':'longitud', 'id':'sucursalId' }, axis =1)
#Trim all the strings to make sure no extra spaces are on them
sucursal.sucursalNombre = sucursal.sucursalNombre.str.strip()
sucursal.direccion = sucursal.direccion.str.strip()

#Export each dataframe into their respective csv file
sucursal.to_csv('./Datasets relevamiento precios new/sucursal.csv',index=False)
provinciaLocalidad.to_csv('./Datasets relevamiento precios new/provinciaLocalidad.csv',index=False)
comercio_bandera.to_csv('./Datasets relevamiento precios new/comercio_bandera.csv',index=False)
sucursalTipo.to_csv('./Datasets relevamiento precios new/sucursalTipo.csv',index=False)
provincia.to_csv('./Datasets relevamiento precios new/provincia.csv',index=False)