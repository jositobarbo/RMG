from auth import cambiar_contrasena

# Cambia 'jose' por el usuario que quieres resetear
usuario = "jose"
nueva_contrasena = "123456"  # pon aquí la nueva

cambiar_contrasena(usuario, nueva_contrasena)
print(f"Contraseña de {usuario} cambiada a: {nueva_contrasena}")
