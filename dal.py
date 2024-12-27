import mysql.connector
from datetime import date
from dataclasses import dataclass
from model_venta import Venta

class VentaDBManager:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establece la conexión con la base de datos."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()

    def obtener_ventas(self) -> list[Venta]:
        """Consulta la tabla ventas y devuelve una lista de objetos Venta."""
        ventas = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, cliente, producto, cantidad, precio, fecha FROM ventas"
            cursor.execute(query)

            for row in cursor.fetchall():
                venta = Venta(
                    id=row['id'],
                    cliente=row['cliente'],
                    producto=row['producto'],
                    cantidad=row['cantidad'],
                    precio=float(row['precio']),
                    fecha=row['fecha']
                )
                ventas.append(venta)
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
        finally:
            cursor.close()

        return ventas