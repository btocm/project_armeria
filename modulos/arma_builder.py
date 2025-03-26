from .arma import Arma


class ArmaBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._nombre = None
        self._modelo = None
        self._calibre = None
        self._numSerie = None
        self._sistemaDisparo_id = None
        self._materiales = None
        self._peso = None
        self._costo = None

    def set_nombre(self, nombre):
        self._nombre = nombre
        return self

    def set_modelo(self, modelo):
        self._modelo = modelo
        return self

    def set_calibre(self, calibre):
        self._calibre = calibre
        return self

    def set_numSerie(self, numSerie):
        self._numSerie = numSerie
        return self

    def set_sistemaDisparo_id(self, sistemaDisparo_id):
        self._sistemaDisparo_id = sistemaDisparo_id
        return self

    def set_materiales(self, materiales):
        self._materiales = materiales
        return self

    def set_peso(self, peso):
        self._peso = peso
        return self

    def set_costo(self, costo):
        self._costo = costo
        return self

    def build(self):
        return Arma(
            self._nombre,
            self._modelo,
            self._calibre,
            self._numSerie,
            self._sistemaDisparo_id,
            self._materiales,
            self._peso,
            self._costo,
        )


class TiroATiroBuilder(ArmaBuilder):
    def __init__(self):
        super().__init__()
        self.set_sistemaDisparo_id(1)


class SemiautomaticoBuilder(ArmaBuilder):
    def __init__(self):
        super().__init__()
        self.set_sistemaDisparo_id(2)


class AutomaticoBuilder(ArmaBuilder):
    def __init__(self):
        super().__init__()
        self.set_sistemaDisparo_id(3)


class ManualBuilder(ArmaBuilder):
    def __init__(self):
        super().__init__()
        self.set_sistemaDisparo_id(4)
