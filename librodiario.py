import logging
from datetime import datetime
from typing import List, Dict

#Configuración de loggin
logging.basicConfig (
    filename="log_contable.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s '
)
class MontoInvalidoError(Exception):
    pass
class LibroDiario:
   
    """Gestión contable básica de ingresos y egresos."""

    def __init__(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción al libro diario."""
        tipo = tipo.lower()
        if tipo not in ("ingreso", "egreso"):
            mensaje = f"Tipo de transacción inválido({tipo}). Use 'ingreso' o 'egreso'."
            logging.error(mensaje)
            raise ValueError (mensaje)
        try:
            obj_fecha= datetime.strptime(fecha, "%d/%m/%Y")
        except Exception as e:
            mensaje = f"Formato de fecha inválido({fecha}). Use 'dd/mm//yyyy'."
            logging.error(mensaje)
            raise ValueError (mensaje)
        if monto < 0:
            mensaje = f"Monto inválido ({monto}). El monto debe ser mayor a 0"
            logging.error(mensaje)
            raise ValueError(mensaje)
        transaccion = {
            "fecha": obj_fecha,
            "descripcion": descripcion,
            "monto": monto,
            "tipo": tipo
        }
        self.transacciones.append(transaccion)
        logging.info(f"Transacción (${fecha} - ${monto}) exitosa")

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen
   
    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        #...
        try:
            with open(path, "r") as f:
                for linea in f:
                    datos = linea.strip().split(";")
                    if len(datos) != 4:
                        logging.error(f"Linea inválida(formato) {linea}")
                        continue
                    fecha, descripcion, valor, tipo = datos
                    try:
                        monto = float(valor)
                    except ValueError as e:
                        continue
                    try:
                        self.agregar_transaccion(
                        self.convertir_fecha(fecha),
                        descripcion,
                        monto,
                        tipo
                        )
                    except (ValueError, MontoInvalidoError) as e:
                        continue
                    except ValueError as e:
                        logging.error(f"Monto no se puede convertir a float ({valor})")
                        continue
                   
                   
                    except (ValueError, MontoInvalidoError) as e:
                        continue
        except FileNotFoundError as e:
            logging.critical(f"El archivo {path} no existe")
    def convertir_fecha(self,fecha: str) -> str:
        dato = fecha.split ("-") #Fecha= 2025-06-01
        return f"{dato[2]}/{dato[1]/{dato[0]}}"