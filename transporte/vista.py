from webbrowser import get
from flask import Flask,  request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "login4"
DB_USER = "postgres"
DB_PASS = "76729987"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/base')   
def base():
    return render_template('base.html')


@app.route('/welcome', methods=['GET', 'POST'])   
def welcome():
    if request.method == 'POST' and 'codigo':
        codigo = request.form['codigo']
        if 'loggedin' in session:
            codValidacion=session['codigoValidacion']
            if (str(codigo) in str(codValidacion)):                    
                return redirect(url_for('questions'))
            else:
                return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    if request.method == 'POST' and 'username' and 'password' :
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()

 
        if account:
            password_rs = account['des_contraseña']
            estadoUsu = account['ind_estado']
            print(estadoUsu)
            # If account exists in users table in out database
            #check_password_hash
            if (password_rs in password):
                codigoV=random.randint(500, 1000)
                # codigoV=10
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id_cuenta']
                session['codigoValidacion']=codigoV
                # session['username'] = account['username']
                # Redirect to home page
                if (str(estadoUsu) in '1'):                    

                    username = "transporteucss@gmail.com"
                    password = "cfvotdoormuiubun"
                    mail_from = "transporteucss@gmail.com"
                    mail_to = account['id_cuenta']
                    mail_subject = "Código de validación"
                    mail_body = ("Este es el código de validación "+str(codigoV))

                    mimemsg = MIMEMultipart()
                    mimemsg['From']=mail_from
                    mimemsg['To']=mail_to
                    mimemsg['Subject']=mail_subject
                    mimemsg.attach(MIMEText(mail_body, 'plain'))
                    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
                    connection.starttls()
                    connection.login(username,password)
                    connection.send_message(mimemsg)
                    connection.quit()
                    return render_template('welcome.html', account=account)
                else:
                    return redirect(url_for('menu'))
                                # return redirect(url_for('menu'))

            else:
                # flash.success(request, "Error")
                # flash(f'Bought {messages} items successfully!', 'success')
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
                # alertify.error("El usuario no existe")

        else:
            # flash(f'Bought {messages} items successfully!', 'success')
            # flash.success(request, "Error")
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
                            # alertify.error("El usuario no existe")
 
    return render_template('index.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('codigoValidacion', None)
   return redirect(url_for('login'))

@app.route('/menu') 
def menu(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        # cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', [session['id']])
        # cursor.execute('SELECT * FROM "rolTrabajador" WHERE "id_rolTrabajador"=701')
        cursor.execute('select t.id_dni as DNI,des_nombre,des_apepat,des_apemat, c.id_cuenta,c.des_contraseña,c.ind_estado,r.des_rol from trabajador t, "ctaTrabajador" ctaT, cuenta c, "rolTrabajador" rolT, rol r where t.id_dni=ctaT.id_dni and ctaT.id_cuenta=c.id_cuenta and rolT.id_trabajador=t.id_dni and r.id_rol=rolT.id_rol and c.id_cuenta = %s', [session['id']])
        account = cursor.fetchone()
        cursor2.execute('select t.id_dni,c.id_cuenta, o.des_opcion from trabajador t, "ctaTrabajador" ctaT, cuenta c, "rolTrabajador" rolT, rol r, opcion o where t.id_dni=ctaT.id_dni and ctaT.id_cuenta=c.id_cuenta and rolT.id_trabajador=t.id_dni and r.id_rol=rolT.id_rol and o.id_rol=r.id_rol and c.id_cuenta = %s', [session['id']])
        account2 = cursor2.fetchall()

        # Show the profile page with account info
        return render_template('menu.html', account=account, account2=account2)
    # User is not loggedin redirect to login page
    return redirect(url_for('menu'))


@app.route('/questions')   
def questions():
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM pregunta')
        account = cursor.fetchall()

        return render_template('questions.html', account=account)
#    return render_template('index.html')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/OrdenPago')
def OrdenPago():
    return render_template('administrador/OrdenPago.html')

@app.route('/Cotización')
def Cotizacion():
    
    return render_template('CotizacionVehiculo.html')

@app.route('/Alquiler')
def Alquiler():
    return render_template('AlquilerVehiculo.html')


@app.route('/MantenimientoP')
def MantenimientoP():
    return render_template('administrador/MantenimientoPreventivo.html')

@app.route('/OrdenMantenimiento')
def OrdenMantenimiento():
    return render_template('Mantenimiento.html')
#----------------------------------------------------------------------
@app.route('/registro')
def registro():
    

  return render_template('administrador/registrar.html')

@app.route('/insertar', methods=['POST'])
def insertar():
    
  cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  dni=request.form["dni"]
  nom=request.form["nombres"]
  ape_pat=request.form["ape_pat"]
  ape_mat=request.form["ape_mat"]
  edad=request.form["edad"]
  numl=request.form["numl"]
  tipol=request.form["tipl"]
  #if(dni=! and numl=!):
  query=f"INSERT INTO Clientes (dni,nombre,ape_pat,ape_mat,edad,num_licencia,tipo_licencia) VALUES ('{dni}','{nom}','{ape_pat}','{ape_mat}',{edad},'{numl}','{tipol}')"
  cursor.execute(query)
  conn.commit()
  cursor.close() 
  
  
  return "Cliente registrado con Exito"



#----------------------------------------------------------------------

@app.route('/RegistroProveedor')
def RegistroProveedor():
    
    return render_template('administrador/RegistroPro.html')


if __name__=='__main__':
    app.run(debug=True, port=2002)