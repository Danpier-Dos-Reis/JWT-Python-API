from dataclasses import dataclass
from datetime import date

@dataclass
class Venta:
    Id: int
    Cliente: str
    Producto: str
    Cantidad: int
    Precio: float
    Fecha: date

    def __init__(self, id, cliente, producto, cantidad, precio, fecha):
        self.Id = id
        self.Cliente = cliente
        self.Producto = producto
        self.Cantidad = cantidad
        self.Precio = precio
        self.Fecha = fecha

    def calcular_total(self) -> float:
        """
        Calcula el total de la venta.
        """
        return self.cantidad * self.precio