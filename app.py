import csv
from datetime import datetime


from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask import jsonify,make_response
from flask_bootstrap import Bootstrap

from forms import LoginForm, RegistrarForm, SearchForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

@app.errorhandler(404)
def e_interno(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def no_encontrado(e):
    return render_template('500.html'), 500

#PARA PROBAR TEMPLATE ERROR 500
@app.route('/500')
def Error500():
    return render_template('500.html'), 500

#obtengo IP PUBLICA del que hace el request
@app.route('/hacked', methods=["GET"])
def hacked():
    ip= request.remote_addr #proxy (intermediario) entorno desarollo
    return render_template('hacked.html',ip=ip)

@app.route('/secret', methods=['GET'])
def secret():
    if 'username' in session:
        with open('usuarios.csv', encoding='utf-8') as archivoCsv:
            users = csv.reader(archivoCsv)
            lista=list(users)
            return render_template('secret.html',lista=lista)
    else:
        return render_template('sin_permiso.html')


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]: 
                    flash('Se ha logueado correctamente!')  # Cartel notificacion 
                    session['username'] = formulario.usuario.data
                    return redirect(url_for('logged'))
                registro = next(archivo_csv, None)
            else:
                flash('Los datos ingresados son incorrectos')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

@app.route('/logged')
def logged():
    if 'username' in session:
        return render_template('index.html',usuario=session['username'])
    else:
        return redirect(url_for('ingresar'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm() #instancia objeto en formulario
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data: #verifica que la Pass se haya colocado igual en ambos campos
            with open('usuarios.csv', 'a+',newline="") as archivo: #Agrego new line para que el usuario se cree sin espacios
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Se ha creado tu usuario correctamente!')
            return redirect(url_for('ingresar'))
        else:
            flash('Las contraseñas no coinciden')
    return render_template('registrar.html', form=formulario)

#Consigo cantidad de clientes tabla
def clientesCont():
    with open('clientes.csv', encoding='utf-8') as archivo:
        archivoCsv=csv.reader(archivo)
        cont=-1
        for i in archivoCsv:
            cont+=1
    return cont

 
 #'''''''''''''''''''''''''''''''''''''''' 

#Transformo en lista el archivo CSV y Utilizo la funcion anteriores para mostrar todo en un mismo template "clientes.html"
@app.route('/clientes', methods=['GET'])
def clientesListado():
    if 'username' in session:  
        with open('clientes.csv', encoding='utf-8') as archivoCsv:
            clientes = csv.reader(archivoCsv)
            lista=list(clientes) #listas por cada fila
            cont=clientesCont()  #llamo contador (funcion modularizada y reutilizable)
        return render_template('clientes.html',lista=lista,cont=cont)
    else:
        return redirect(url_for('ingresar'))

def dictCsv(csvArc):
    archivoCsv=open(csvArc, encoding='utf-8')
    lista=csv.DictReader(archivoCsv)
    return lista

@app.route('/buscador', methods=['GET','POST'])
def buscadorPais():
    if 'username' in session:
        listado=dictCsv("clientes.csv")
        formulario = SearchForm() #instancia objeto en formulario para poder usarlo
        pais=formulario.search.data #Argentina
        if formulario.validate_on_submit(): #si llena el buscador
            paises=[]
            for i in listado:
                if pais in i['País'] : #si Argentina se encuentra en columna Pais
                    paises.append(i['País']) #agerga el pais encontrado
            if paises: #si tiene contenido
                flash("Búsqueda exitosa")
            else:
                flash('No se encontraron paises')
            return render_template('buscador.html',paises=paises, formulario=formulario)#me guardo pais buscado para hipervinculo y lista para imprimir
        return render_template('buscador.html',formulario=formulario)
    return redirect(url_for('ingresar'))


#Tiene que vincular un template donde aparezca una tabla con el filtro aplicado
@app.route('/buscador/<i>') #pais
def resultadoBuscadorPais(i):
    if 'username' in session:
        with open('clientes.csv', encoding='utf-8') as archivoCsv:
            listado = csv.DictReader(archivoCsv) 
            firstRow=next(listado) #funcion nico, permite obtener primera linea
            lista=[]
            for columna in listado:
                if columna['País'] == i:
                    lista.append(columna) #si el pais elegido es igual a el contenido de la columna agrega la filalista=lista
            cont=len(lista)
            return render_template('buscadorpais.html',lista=lista,cont=cont,firstRow=firstRow)
    return redirect(url_for('ingresar'))



# ''''''''''''''''''''''''''''''''''''''''''''
@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


@app.route('/sobre', methods=['GET'])
def sobre():
    if 'username' in session:
        return render_template('sobre.html')
    else:
        return redirect(url_for('ingresar'))


#Hago lista para mostrar lista de usuarios y contraseñas en template "secret.html"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
