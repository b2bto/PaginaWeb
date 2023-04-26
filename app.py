import os
from flask import Flask
from flask import render_template, request, redirect, session 
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__)
app.secret_key='develoteca'
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitioweb'

mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img/'),imagen)

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'), archivocss)

@app.route('/arte')
def arte():
        
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `arte`")
    listarte=cursor.fetchall()
    conexion.commit()
    print(listarte)

    return render_template('sitio/arte.html',arte=listarte)
@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect('/admin/login')
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)
    
    if _usuario=='admin' and _password=='user':
        session['login']=True
        session['usuario']='Administrador'
        return redirect('/admin')
    
    return render_template('admin/login.html', mensaje="Acceso Denegado")

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')
    
    
@app.route('/admin/arte')
def admin_arte():
    if not 'login' in session:
        return redirect('/admin/login')
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `arte`")
    listarte=cursor.fetchall()
    conexion.commit()
    print(listarte)

    return render_template('admin/arte.html',arte=listarte)

@app.route('/admin/arte/guardar', methods=['POST'])
def  admin_arte_guardar():
    if not 'login' in session:
        return redirect('/admin/login')

    _nombre=request.form['txtNombre']
    _archivo=request.files['txtImagen']
    _url=request.form['txtURL']

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')
    
    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="INSERT INTO `arte` (`Id`, `nombre`, `imagen`, `url`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre,nuevoNombre,_url)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    print(_nombre)
    print(_url)
    print(_archivo)
    return redirect('/admin/arte')

@app.route('/admin/arte/borrar', methods=['POST'])
def admin_arte_borrar():
    
    if not 'login' in session:
        return redirect('/admin/login')
        
    _id=request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `arte` WHERE id=%s",(_id))
    listarte=cursor.fetchall()
    conexion.commit()
    print(listarte)
    
    if os.path.exists('templates/sitio/img/'+str(listarte[0][0])):
        os.unlink('templates/sitio/img/'+str(listarte[0][0]))

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM arte WHERE id=%s", (_id))
    conexion.commit()
    
    return redirect('/admin/arte')

if __name__ =='__main__':
    app.run(debug=True)