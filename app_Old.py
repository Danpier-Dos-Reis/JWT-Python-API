from dal import VentaDBManager


# Uso de la clase VentaDBManager
if __name__ == "__main__":
    # Configuración de la conexión
    db_manager = VentaDBManager(
        host="localhost",
        user="dorito",
        password="Dorit@Picant3",
        database="db_ventas"
    )

    try:
        db_manager.connect()
        ventas = db_manager.obtener_ventas()

        # Mostrar las ventas
        for venta in ventas:
            print(venta)
    finally:
        db_manager.close()