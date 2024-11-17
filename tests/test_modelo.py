from importlib.resources import files
import os
import unittest
from inspect import signature, getmembers, isclass
import app.modelo as model_module
from app.errores import DestinoInalcanzableError


def has_class(module, class_name):
    return class_name in [name for name, _ in getmembers(module) if isclass(_)]


class TestTransporte(unittest.TestCase):
    def setUp(self):
        if has_class(model_module, "Transporte"):
            class TransporteSubclass(model_module.Transporte):
                def estimar_tiempo_entrega(self, distancia_total: float) -> float:
                    return 0.0
            try:
                self.transporte_object = TransporteSubclass("id", 100, "Bogotá")
            except TypeError:
                self.transporte_object = None

        if self._testMethodDoc:
            self._testMethodDoc = self._testMethodDoc.strip()

    def test_class_is_abstract(self):
        """Clase Transporte es abstracta"""
        if not has_class(model_module, "Transporte"):
            self.fail("Clase Transporte no definida")
        else:
            try:
                self.assertTrue(hasattr(model_module.Transporte, "__abstractmethods__"))
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar si la clase Transporte es abstracta: {e}")

    def test_class_has_attributes(self):
        """Clase Transporte tiene los atributos esperados"""
        attributes = ["id_transporte", "capacidad_maxima", "ubicacion_actual"]
        for attr in attributes:
            with self.subTest(attr=attr):
                if not has_class(model_module, "Transporte"):
                    self.fail("Clase Transporte no definida")
                else:
                    try:
                        self.assertTrue(hasattr(self.transporte_object, attr))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al verificar el atributo {attr}: {e}")

    def test_class_init_method_initializes_attributes(self):
        """Clase Transporte inicializa los atributos correctamente"""
        if not has_class(model_module, "Transporte"):
            self.fail("Clase Transporte no definida")
        else:
            try:
                self.assertEqual("id", self.transporte_object.id_transporte)
                self.assertEqual(100, self.transporte_object.capacidad_maxima)
                self.assertEqual("Bogotá", self.transporte_object.ubicacion_actual)
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al inicializar los atributos: {e}")

    def test_class_has_methods_signatures_well_defined(self):
        """Clase Transporte tiene los métodos bien definidos"""
        methods = [
            [("calcular_ruta", '(destinos: list[str]) -> dict'), ("calcular_ruta", '(destinos: List[str]) -> Dict')],
            [("estimar_tiempo_entrega", '(distancia_total: float) -> float'), None],
            [("generar_reporte", '(ruta: dict, archivo: str)'),
             ("generar_reporte", '(ruta: dict, archivo: str) -> None')]
        ]
        for method in methods:
            with self.subTest(method=method):
                if not has_class(model_module, "Transporte"):
                    self.fail("Clase Transporte no definida")
                else:
                    try:
                        if method[1] is None:
                            method_name, signature_str = method[0]
                            callable_method = getattr(self.transporte_object, method_name)
                            self.assertTrue(callable(callable_method))
                            self.assertEqual(signature_str, str(signature(callable_method)))
                        else:
                            callable_method = getattr(self.transporte_object, method[0][0])
                            self.assertTrue(callable(callable_method))
                            self.assertTrue(str(signature(callable_method)) == method[0][1] or
                                            str(signature(callable_method)) == method[1][1])
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al verificar el método {method}: {e}")

    def test_class_has_abstract_method(self):
        """Clase Transporte tiene el método abstracto estimar_tiempo_entrega"""
        if not has_class(model_module, "Transporte"):
            self.fail("Clase Transporte no definida")
        else:
            try:
                self.assertTrue(hasattr(model_module.Transporte, "__abstractmethods__"))
                self.assertIn("estimar_tiempo_entrega", model_module.Transporte.__abstractmethods__)
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar el método abstracto estimar_tiempo_entrega: {e}")

    def test_calcular_ruta_method_returns_correct_dict(self):
        """Método calcular_ruta de la clase Transporte retorna un diccionario con los valores correctos"""
        cases = [
            (["Cali", "Medellín", "Cartagena"],
             {"ruta": ["Bogotá", "Cali", "Medellín", "Cartagena"], "distancia_total": 1505}),
            (["Cali", "Barranquilla", "Bucaramanga"],
             {"ruta": ["Bogotá", "Cali", "Barranquilla", "Bucaramanga"], "distancia_total": 2090}),
            (["Bogotá", "Medellín", "Santa Marta"],
             {"ruta": ["Bogotá", "Medellín", "Santa Marta"], "distancia_total": 1085}),
        ]
        for destinos, expected in cases:
            with self.subTest(destinos=destinos, expected=expected):
                if not has_class(model_module, "Transporte"):
                    self.fail("Clase Transporte no definida")
                else:
                    try:
                        self.assertEqual(expected, self.transporte_object.calcular_ruta(destinos))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al calcular la ruta: {e}")

    def test_calcular_ruta_method_raises_exception(self):
        """Método calcular_ruta de la clase Transporte lanza una excepción DestinoInalcanzableError"""
        cases = [
            ["Santa Marta", "Villavicencio", "Bogotá"],
            ["Cali", "Santa Marta", "Manizales"],
            ["Villavicencio", "Santa Marta", "Bogotá", "Cali", "Medellín"],
        ]
        for destinos in cases:
            with self.subTest(destinos=destinos):
                if not has_class(model_module, "Transporte"):
                    self.fail("Clase Transporte no definida")
                else:
                    try:
                        self.transporte_object.ubicacion_actual = "Medellín"
                        with self.assertRaises(DestinoInalcanzableError):
                            self.transporte_object.calcular_ruta(destinos)
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al calcular la ruta: {e}")

    def test_generar_reporte_method_writes_file(self):
        """Método generar_reporte de la clase Transporte escribe un archivo con los datos esperados"""
        casos = [
            ({"ruta": ["Bogotá", "Cali", "Medellín", "Cartagena"], "distancia_total": 1505},
             ("Reporte de Transporte\n"
              "----------------------\n"
              "ID del Transporte: id\n"
              "Capacidad Máxima: 100 kg\n"
              "Ubicación Actual: Bogotá\n"
              "Ruta Calculada: Bogotá -> Cali -> Medellín -> Cartagena\n"
              "Distancia Total: 1505 km")),
            ({"ruta": ["Cali", "Barranquilla", "Bucaramanga"], "distancia_total": 2090},
             ("Reporte de Transporte\n"
              "----------------------\n"
              "ID del Transporte: id\n"
              "Capacidad Máxima: 100 kg\n"
              "Ubicación Actual: Bogotá\n"
              "Ruta Calculada: Cali -> Barranquilla -> Bucaramanga\n"
              "Distancia Total: 2090 km")),
            ({"ruta": ["Bogotá", "Medellín", "Santa Marta"], "distancia_total": 1085},
             ("Reporte de Transporte\n"
              "----------------------\n"
              "ID del Transporte: id\n"
              "Capacidad Máxima: 100 kg\n"
              "Ubicación Actual: Bogotá\n"
              "Ruta Calculada: Bogotá -> Medellín -> Santa Marta\n"
              "Distancia Total: 1085 km")),
        ]
        for ruta, expected in casos:
            with self.subTest(ruta=ruta, expected=expected):
                if not has_class(model_module, "Transporte"):
                    self.fail("Clase Transporte no definida")
                else:
                    try:
                        self.transporte_object.ubicacion_actual = "Bogotá"
                        report_file = str(files("tests").joinpath("reporte.txt"))
                        os.remove(report_file) if os.path.exists(report_file) else None
                        self.transporte_object.generar_reporte(ruta, report_file)
                        with open(report_file, "r", encoding='utf8') as file:
                            content = file.read()
                        self.assertEqual(expected, content)
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al generar el reporte: {e}")


class TestCamion(unittest.TestCase):
    def setUp(self):
        if has_class(model_module, "Camion"):
            try:
                self.camion = model_module.Camion("id", 100, "Bogotá", 50, 3)
            except TypeError:
                self.camion = None

        if self._testMethodDoc:
            self._testMethodDoc = self._testMethodDoc.strip()
    
    def test_class_inherits_from_transporte(self):
        """Clase Camion hereda de Transporte"""
        if not has_class(model_module, "Camion") or not has_class(model_module, "Transporte"):
            self.fail("Clase Camion o Transporte no definida")
        else:
            try:
                self.assertTrue(issubclass(model_module.Camion, model_module.Transporte))
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar si la clase Camion hereda de Transporte: {e}")
    
    def test_class_has_attributes(self):
        """Clase Camion tiene los atributos esperados"""
        attributes = ["id_transporte", "capacidad_maxima", "ubicacion_actual", "velocidad_promedio", "peajes"]
        for attr in attributes:
            with self.subTest(attr=attr):
                if not has_class(model_module, "Camion"):
                    self.fail("Clase Camion no definida")
                else:
                    try:
                        self.assertTrue(hasattr(self.camion, attr))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al verificar el atributo {attr}: {e}")
    
    def test_class_init_method_initializes_attributes(self):
        """Clase Camion inicializa los atributos correctamente"""
        if not has_class(model_module, "Camion"):
            self.fail("Clase Camion no definida")
        else:
            try:
                self.assertEqual("id", self.camion.id_transporte)
                self.assertEqual(100, self.camion.capacidad_maxima)
                self.assertEqual("Bogotá", self.camion.ubicacion_actual)
                self.assertEqual(50, self.camion.velocidad_promedio)
                self.assertEqual(3, self.camion.peajes)
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al inicializar los atributos: {e}")

    def test_class_has_estimar_tiempo_entrega_method_signature_well_defined(self):
        """Método estimar_tiempo_entrega de la clase Camion está implementado y tiene la firma esperada"""
        if not has_class(model_module, "Camion"):
            self.fail("Clase Camion no definida")
        else:
            try:
                callable_method = getattr(self.camion, "estimar_tiempo_entrega")
                self.assertTrue(callable(callable_method))
                self.assertTrue(callable_method.__func__ is not model_module.Transporte.estimar_tiempo_entrega)
                self.assertEqual("(distancia_total: float) -> float", str(signature(callable_method)))
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar el método estimar_tiempo_entrega: {e}")

    def test_estimar_tiempo_entrega_method_returns_correct_value(self):
        """Método estimar_tiempo_entrega de la clase Camion retorna el valor correcto"""
        cases_distancia_total = [
            (150, 3.5),
            (300, 6.5),
            (450, 9.5),
        ]
        for distancia_total, expected in cases_distancia_total:
            with self.subTest(distancia_total=distancia_total, expected=expected):
                if not has_class(model_module, "Camion"):
                    self.fail("Clase Camion no definida")
                else:
                    try:
                        self.assertEqual(expected, self.camion.estimar_tiempo_entrega(distancia_total))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al calcular el tiempo de entrega: {e}")


class TestAvion(unittest.TestCase):
    def setUp(self):
        if has_class(model_module, "Avion"):
            try:
                self.avion = model_module.Avion("id", 100, "Bogotá", 300, 10)
            except TypeError:
                self.avion = None

        if self._testMethodDoc:
            self._testMethodDoc = self._testMethodDoc.strip()
    
    def test_class_inherits_from_transporte(self):
        """Clase Avion hereda de Transporte"""
        if not has_class(model_module, "Avion") or not has_class(model_module, "Transporte"):
            self.fail("Clase Avion o Transporte no definida")
        else:
            try:
                self.assertTrue(issubclass(model_module.Avion, model_module.Transporte))
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar si la clase Avion hereda de Transporte: {e}")
    
    def test_class_has_attributes(self):
        """Clase Avion tiene los atributos esperados"""
        attributes = ["id_transporte", "capacidad_maxima", "ubicacion_actual", "velocidad_promedio", "horas_descanso"]
        for attr in attributes:
            with self.subTest(attr=attr):
                if not has_class(model_module, "Avion"):
                    self.fail("Clase Avion no definida")
                else:
                    try:
                        self.assertTrue(hasattr(self.avion, attr))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al verificar el atributo {attr}: {e}")
    
    def test_class_init_method_initializes_attributes(self):
        """Clase Avion inicializa los atributos correctamente"""
        if not has_class(model_module, "Avion"):
            self.fail("Clase Avion no definida")
        else:
            try:
                self.assertEqual("id", self.avion.id_transporte)
                self.assertEqual(100, self.avion.capacidad_maxima)
                self.assertEqual("Bogotá", self.avion.ubicacion_actual)
                self.assertEqual(300, self.avion.velocidad_promedio)
                self.assertEqual(10, self.avion.horas_descanso)
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al inicializar los atributos: {e}")

    def test_class_has_estimar_tiempo_entrega_method_signature_well_defined(self):
        """Método estimar_tiempo_entrega de la clase Avion está implementado y tiene la firma esperada"""
        if not has_class(model_module, "Avion"):
            self.fail("Clase Avion no definida")
        else:
            try:
                callable_method = getattr(self.avion, "estimar_tiempo_entrega")
                self.assertTrue(callable(callable_method))
                self.assertTrue(callable_method.__func__ is not model_module.Transporte.estimar_tiempo_entrega)
                self.assertEqual("(distancia_total: float) -> float", str(signature(self.avion.estimar_tiempo_entrega)))
            except (AttributeError, TypeError) as e:
                self.fail(f"Error al verificar el método estimar_tiempo_entrega: {e}")

    def test_estimar_tiempo_entrega_method_returns_correct_value(self):
        """Método estimar_tiempo_entrega de la clase Avion retorna el valor correcto"""
        cases_distancia_total = [
            (150, 0.5),
            (300, 1),
            (450, 1.5),
        ]
        for distancia_total, expected in cases_distancia_total:
            with self.subTest(distancia_total=distancia_total, expected=expected):
                if not has_class(model_module, "Avion"):
                    self.fail("Clase Avion no definida")
                else:
                    try:
                        self.assertEqual(expected, self.avion.estimar_tiempo_entrega(distancia_total))
                    except (AttributeError, TypeError) as e:
                        self.fail(f"Error al calcular el tiempo de entrega: {e}")
