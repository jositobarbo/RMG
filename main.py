from scripts.ingredientes import actualizar_precio_ingrediente
from scripts.recetas import obtener_id_receta_por_nombre, calcular_precio_receta

# Actualizar el precio del huevo
actualizar_precio_ingrediente("huevo", 0.35)

# Recalcular el precio de la receta afectada
receta_id = obtener_id_receta_por_nombre("Tortilla de patatas")
if receta_id:
    calcular_precio_receta(receta_id)
