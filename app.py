import sqlite3
import streamlit as st
from scripts.ingredientes import insertar_ingrediente, actualizar_precio_ingrediente
from scripts.recetas import insertar_receta, asociar_ingrediente_a_receta, obtener_id_receta_por_nombre, calcular_precio_receta, listar_recetas


st.set_page_config(page_title="RMG - Escandallos Dinámicos", layout="centered")

st.title("📊 RMG - Revenue Management Gastronómico")
st.subheader("Gestión dinámica de escandallos para restaurantes y bares")

menu = st.sidebar.selectbox("Selecciona una opción", [
    "📥 Añadir ingrediente",
    "🧾 Crear receta",
    "➕ Añadir ingrediente a receta",
    "💰 Calcular precio receta",
    "📊 Ver escandallo de receta",
    "🔄 Actualizar precio de ingrediente",
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
        receta_id = insertar_receta(nombre, margen / 100)
        st.success(f"Receta '{nombre}' creada (ID: {receta_id})")

elif menu == "💰 Calcular precio receta":
    st.header("💰 Calcular precio receta")
    listar_recetas()
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
    cursor.execute("SELECT id, nombre FROM Recetas")
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
    cursor.execute("SELECT id, nombre FROM Recetas")
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
