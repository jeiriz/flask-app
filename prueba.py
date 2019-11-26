import csv

with open('clientesfalso.csv', encoding='utf-8') as archivoCsv:
	clientesReader = csv.reader(archivoCsv)
	clientesDictReader=csv.DictReader(archivoCsv)
	for columna in clientesDictReader:
		print(columna['Nombre'],columna['Edad'])

	# for e in clientesDictReader:
	# 	print("esto es clientesDictReader ",e) #crea una lista x cada fila conteniendo tantos diccionarios como columnas, utilizando primera fila como referencia del contenido, es decir [(nombre,mario),(edad,4)],[(nombre,juan),(edad,3)]


 #    # lista=list(clientes)
    # print("esto es lista ", lista)


results=[]
with open('clientesfalso.csv', encoding='utf-8') as archivoCsv:
	clientesReader = csv.reader(archivoCsv)
	clientesDictReader=csv.DictReader(archivoCsv)
	for columna in clientesDictReader:
		results.append(columna)
	print(results)

# guarda todo en la lista
