from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "login"
DB_USER = "postgres"
DB_PASS = "76729987"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/base')   
def base():
    return render_template('base.html')





@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #rol = request.form['rol']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', (username,))
        #cursor.execute('SELECT * FROM rol WHERE id_rol = %s', (rol,103))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['des_contraseña']
            #rol_rs = account['id_rol']
            print(password_rs)
            #print(rol_rs)
            # If account exists in users table in out database
            #check_password_hash
            if (password_rs in password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id_cuenta']
                # session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('menu'))
            else:
                # messages.success(request, "Error")
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
                # alertify.error("El usuario no existe")
        else:
            # messages.success(request, "Error")
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
                            # alertify.error("El usuario no existe")
 
    return render_template('index.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
#    session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/menu') 
def menu(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('menu.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('menu'))


    
    

@app.route('/REGISTRO')
def registro():
  
    return render_template('REGISTRO.html')

@app.route('/COTIZACIÓN')
def cotizacion():
    
    return render_template('COTIZACION.html')

@app.route('/ALQUILER')
def alquiler():
    return render_template('ALQUILER.html')


@app.route('/DEVOLUCION')
def devolucion():
    return render_template('DEVOLUCION.html')










if __name__=='__main__':
    app.run(debug=True, port=2000)