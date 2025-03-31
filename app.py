import sqlite3
import streamlit as st
import pandas as pd
import streamlit as st
from auth import crear_tabla_usuarios, registrar_usuario, verificar_usuario
from scripts.ingredientes import insertar_ingrediente, actualizar_precio_ingrediente
from scripts.recetas import insertar_receta, asociar_ingrediente_a_receta, obtener_id_receta_por_nombre, calcular_precio_receta, listar_recetas
from scripts.ingredientes import actualizar_stock_ingrediente, obtener_stock_ingrediente


st.set_page_config(page_title="RMG - Escandallos Dinámicos", layout="centered")

crear_tabla_usuarios()

menu = ["Inicio de sesión", "Registro"]
eleccion = st.sidebar.selectbox("Menú", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if eleccion == "Registro":
    st.title("Registro")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Registrarme"):
        if registrar_usuario(username, password):
            st.success("Usuario registrado correctamente.")
        else:
            st.error("El usuario ya existe.")

elif eleccion == "Inicio de sesión":
    st.title("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if verificar_usuario(username, password):
            st.success(f"Bienvenido, {username}")
            st.session_state.logged_in = True
            st.session_state.user = username
        else:
            st.error("Credenciales incorrectas")

if st.session_state.logged_in:
    if st.session_state.user == "jose":
        st.sidebar.markdown("### 👑 Admin")
        if st.sidebar.button("🛠 Panel de usuarios"):
            st.session_state.panel_usuarios = True
    else:
        st.session_state.panel_usuarios = False

    st.sidebar.success(f"Sesión iniciada como {st.session_state.user}")
    # Aquí iría tu sistema de escandallos personalizado para ese usuario
    
    st.title("📊 RMG - Revenue Management Gastronómico")
    st.subheader("Gestión dinámica de escandallos para restaurantes y bares")

    menu = st.sidebar.selectbox("Selecciona una opción", [
        "📥 Añadir ingrediente",
        "🧾 Crear receta",
        "➕ Añadir ingrediente a receta",
        "💰 Calcular precio receta",
        "📊 Ver escandallo de receta",
        "📈 Dashboard resumen",
        "📤 Exportar escandallo a Excel",  # <-- Nueva opción
        "🔄 Actualizar precio de ingrediente",
        "🖨️ Exportar escandallo a PDF",
        "📦 Gestionar stock",
        "📋 Ver recetas"
    ])

    if menu == "📥 Añadir ingrediente":
        st.header("📥 Añadir nuevo ingrediente")
        nombre = st.text_input("Nombre del ingrediente")
        unidad = st.text_input("Unidad (kg, litro, ud...)")
        coste = st.number_input("Coste unitario (€)", min_value=0.0, format="%.2f")
        if st.button("Guardar"):
            insertar_ingrediente(nombre, unidad, coste)
            st.success(f"Ingrediente '{nombre}' añadido correctamente.")

    elif menu == "🧾 Crear receta":
        st.header("🧾 Crear receta")
        nombre = st.text_input("Nombre de la receta")
        margen = st.slider("Margen objetivo (%)", 0, 100, 70)
        if st.button("Crear receta"):
            receta_id = insertar_receta(nombre, margen / 100, st.session_state.user)
            st.success(f"Receta '{nombre}' creada (ID: {receta_id})")

    elif menu == "💰 Calcular precio receta":
        st.header("💰 Calcular precio receta")
        listar_recetas(st.session_state.user)
        nombre = st.text_input("Nombre de la receta")
        if st.button("Calcular precio"):
            receta_id = obtener_id_receta_por_nombre(nombre)
            if receta_id:
                precio = calcular_precio_receta(receta_id)
                st.success(f"💸 Precio sugerido: {precio:.2f} €")

    elif menu == "🔄 Actualizar precio de ingrediente":
        st.header("🔄 Actualizar precio de ingrediente")
        nombre = st.text_input("Nombre del ingrediente")
        nuevo_precio = st.number_input("Nuevo precio unitario (€)", min_value=0.0, format="%.2f")
        if st.button("Actualizar"):
            actualizar_precio_ingrediente(nombre, nuevo_precio)
            st.success(f"Precio de '{nombre}' actualizado a {nuevo_precio:.2f} €")

    elif menu == "📋 Ver recetas":
        st.header("📋 Todas las recetas registradas")
        listar_recetas()

    elif menu == "➕ Añadir ingrediente a receta":
        st.header("➕ Añadir ingrediente a una receta")

        # Obtener nombres de recetas
        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Recetas WHERE usuario = ?", (st.session_state.user,))
        recetas = cursor.fetchall()
        conn.close()

        receta_seleccionada = st.selectbox("Selecciona una receta", recetas, format_func=lambda x: x[1])

        # Obtener ingredientes
        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Ingredientes")
        ingredientes = cursor.fetchall()
        conn.close()

        ingrediente_seleccionado = st.selectbox("Selecciona un ingrediente", ingredientes, format_func=lambda x: x[1])

        cantidad = st.number_input("Cantidad utilizada (en la unidad correspondiente)", min_value=0.0, format="%.2f")
    
    elif menu == "📦 Gestionar stock":
    
        st.header("📦 Gestión de stock de ingredientes")

        # Obtener ingredientes
        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Ingredientes")
        ingredientes = [row[0] for row in cursor.fetchall()]
        conn.close()

        ingrediente = st.selectbox("Selecciona un ingrediente", ingredientes)

        stock_actual = obtener_stock_ingrediente(ingrediente)
        st.info(f"Stock actual: **{stock_actual:.2f}** unidades")

        nuevo_stock = st.number_input("Nuevo stock", min_value=0.0, value=stock_actual, format="%.2f")

        if st.button("Actualizar stock"):
        actualizar_stock_ingrediente(ingrediente, nuevo_stock)
        st.success(f"Stock de '{ingrediente}' actualizado a {nuevo_stock:.2f}")


        if st.button("Añadir a la receta"):
            receta_id = receta_seleccionada[0]
            ingrediente_id = ingrediente_seleccionado[0]
            asociar_ingrediente_a_receta(receta_id, ingrediente_id, cantidad)
            st.success("Ingrediente añadido correctamente a la receta.")

    elif menu == "📊 Ver escandallo de receta":
        st.header("📊 Escandallo completo")

        # Obtener lista de recetas
        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Recetas WHERE usuario = ?", (st.session_state.user,))
        recetas = cursor.fetchall()
        conn.close()

        receta_seleccionada = st.selectbox("Selecciona una receta", recetas, format_func=lambda x: x[1])

        if st.button("Mostrar escandallo"):
            from scripts.recetas import obtener_escandallo_completo
            receta_id = receta_seleccionada[0]
            data = obtener_escandallo_completo(receta_id)

            st.subheader(f"🧾 Receta: {data['receta']}")
            st.write(f"📉 Margen objetivo: {data['margen']*100:.0f}%")
            st.write(f"🧮 Coste total: {data['coste_total']:.2f} €")
            st.success(f"💰 Precio sugerido: {data['precio_sugerido']:.2f} €")

            st.markdown("### 📋 Ingredientes utilizados:")

            for nombre, cantidad, unidad, precio, coste in data["ingredientes"]:
                st.markdown(f"- **{nombre}**: {cantidad} {unidad} × {precio:.2f} € = `{coste:.2f} €`")
        
    elif menu == "📈 Dashboard resumen":
            from scripts.recetas import obtener_resumen_recetas
            import pandas as pd

            st.header("📈 Dashboard resumen")

            data = obtener_resumen_recetas()
            df = pd.DataFrame(data)

            if not df.empty:
                st.dataframe(df)

                st.subheader("🥇 Recetas más rentables (por margen real)")
                top = df.sort_values("margen_real", ascending=False).head(5)
                st.table(top)

                st.subheader("⚠️ Recetas con margen inferior al 50%")
                bajas = df[df["margen_real"] < 50]
                if not bajas.empty:
                    st.error("¡Atención! Estas recetas tienen margen bajo:")
                    st.table(bajas)
                else:
                    st.success("Todas las recetas tienen buen margen ✅")
            else:
                st.info("No hay recetas registradas aún.")
                
    elif menu == "📤 Exportar escandallo a Excel":
        from scripts.recetas import obtener_escandallo_completo
        
        st.header("📤 Exportar escandallo a Excel")

        # Seleccionar receta
        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Recetas WHERE usuario = ?", (st.session_state.user,))
        recetas = cursor.fetchall()
        conn.close()

        receta_seleccionada = st.selectbox("Selecciona una receta", recetas, format_func=lambda x: x[1])

        if st.button("Exportar a Excel"):
            receta_id = receta_seleccionada[0]
            data = obtener_escandallo_completo(receta_id)

            # Preparar DataFrame
            df = pd.DataFrame(data["ingredientes"], columns=["Ingrediente", "Cantidad", "Unidad", "Precio unitario", "Coste"])

            # Crear archivo Excel
            nombre_archivo = f"{data['receta']}_escandallo.xlsx"
            df.to_excel(nombre_archivo, index=False)

            st.success(f"Escandallo exportado como: {nombre_archivo}")
            with open(nombre_archivo, "rb") as file:
                st.download_button("📥 Descargar Excel", file, file_name=nombre_archivo)

    elif menu == "🖨️ Exportar escandallo a PDF":
        from scripts.recetas import obtener_escandallo_completo, exportar_escandallo_a_pdf

        st.header("🖨️ Exportar escandallo a PDF")

        conn = sqlite3.connect("db/escandallos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Recetas WHERE usuario = ?", (st.session_state.user,))
        recetas = cursor.fetchall()
        conn.close()

        receta_seleccionada = st.selectbox("Selecciona una receta", recetas, format_func=lambda x: x[1])

        if st.button("Exportar a PDF"):
            receta_id = receta_seleccionada[0]
            data = obtener_escandallo_completo(receta_id)

            nombre_archivo = f"{data['receta'].replace(' ', '_')}_escandallo.pdf"
            exportar_escandallo_a_pdf(data, nombre_archivo)

            st.success(f"Escandallo exportado como: {nombre_archivo}")
            with open(nombre_archivo, "rb") as file:
                st.download_button("📥 Descargar PDF", file, file_name=nombre_archivo)
                
# ----- PANEL DE ADMINISTRACIÓN -----
if st.session_state.get("panel_usuarios", False):
    st.header("🛠 Panel de Administración de Usuarios")

    usuarios = obtener_todos_los_usuarios()

    for user in usuarios:
        col1, col2, col3 = st.columns([3, 3, 2])
        with col1:
            st.markdown(f"👤 **{user}**")
        with col2:
            nueva_pwd = st.text_input(f"🔐 Nueva contraseña para {user}", key=f"pwd_{user}")
            if nueva_pwd:
                cambiar_contrasena(user, nueva_pwd)
                st.success(f"Contraseña de {user} actualizada.")
        with col3:
            if user != st.session_state.user:
                if st.button("🗑 Eliminar", key=f"del_{user}"):
                    eliminar_usuario(user)
                    st.warning(f"Usuario {user} eliminado.")

