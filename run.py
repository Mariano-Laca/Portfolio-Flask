#Importar
from flask import Flask, render_template, request
import requests, json #Solución import requests from venv
from forms import miformulario
from flask_bootstrap import Bootstrap #importamos Bootstrap para el formulario
from flask_recaptcha import ReCaptcha # Importar ReCaptcha
from flask_mail import Mail, Message

#Crear app medante instancia
app = Flask(__name__)
#Configuraciones
app.secret_key = "pythones.netelmejorblog"
Bootstrap(app) #Decoramos nuestra app con bootstrap
#Recaptcha
app.config['RECAPTCHA_SITE_KEY'] = 'captcha' 
app.config['RECAPTCHA_SECRET_KEY'] = 'captcha' 
recaptcha = ReCaptcha(app)
#Flask-Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'maniacp3@gmail.com'
app.config['MAIL_PASSWORD'] = 'captcha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 



#Crear rutas con sus correspondientes funciones
#INICIO
@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')
#MI BLOG
@app.route('/blog', methods=['GET'])
def blog():
    return render_template('/blog.html')
#MIS PROYECTOS
@app.route('/mis-proyectos', methods=['GET'])
def mostrarproyectos():
    return render_template('mis-proyectos.html')
#MIS HABILIDADES
@app.route('/habilidades', methods=['GET'])
def habilidades():
    return render_template('mis-habilidades.html')
#CONTACTO
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    sitekey = "captcha"

    if request.method == "POST":
        name = request.form['Nombre']
        email = request.form['Email']
        Mensaje = request.form['Mensaje']

        respuesta_del_captcha = request.form['g-recaptcha-response']
        
        if comprobar_humano(respuesta_del_captcha):
           #Si devuelve True
            status = "Exito."
            enviar_correo(request.form)
            print (status)
        else:
           #Si devuelve False
            status = "Error, vuelve a comprobar que no eres un robot."
            print (status)

    return render_template("contacto.html", sitekey=sitekey)


#CONTACTO2 - FLASKFORMS WTFORMS
@app.route("/contacto2", methods=["GET", "POST"])
def contacto2():
    miform = miformulario()
    if miform.validate_on_submit() and recaptcha.verify():
        print(f"Name:{miform.name.data},Email:{miform.email.data},Mensaje:{miform.message.data}")
        mimensaje = {
            'Email': miform.email.data,
            'Mensaje' : miform.message.data }

        enviar_correo(mimensaje)
    else:
        print("Algún dato es invalido")
    return render_template("contacto2.html", form=miform)


def comprobar_humano(respuesta_del_captcha):
    secret = "captcha"
    payload = {'response':respuesta_del_captcha, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

def enviar_correo(mensaje):
    msg = Message(
    subject  = (f"{mensaje.get('Email')} quiere contactarse contigo desde tu app"), 
    sender = mensaje.get('Email'), 
    recipients = ['maniacp3@gmail.com'], 
    body= mensaje.get('Mensaje')
    )  
    mail.send(msg)

#Ejecutar nuestra app cuando ejecutemos este archivo run.py
if __name__ == '__main__':
    app.run(debug=True)