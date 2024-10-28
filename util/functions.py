from util.widgets import Button
from tkinter import messagebox
from util_alerts import error_advice

def create_button_with_permission(frame, text, command, required_permission, permisos, x, y):
    # Determina si el botón debe estar habilitado o deshabilitado
    state = 'normal' if required_permission in permisos or required_permission is None else 'disabled'
    # Crea y devuelve el botón con el estado configurado
    return Button(frame, text=text, command=command, x=x, y=y, state=state)

def perform_restore_action(item_id, table, permisos, switch_status, show_status, update_table, recover_function, confirmation_message, error_message):

    try:
        confirmar = messagebox.askyesno("Confirmar", confirmation_message)

        if confirmar:
            recover_function(item_id)
            switch_status.select(True)      # Cambia el estado del interruptor a activo
            show_status(permisos)           # Actualiza el estado mostrado
            update_table()                   # Refresca la tabla

    except Exception as e:
        error_advice()
        mensaje = f'{error_message}: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')