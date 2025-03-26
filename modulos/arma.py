class Arma:
    def __init__(self, nombre, modelo, calibre, numSerie, sistemaDisparo_id, materiales, peso, costo):
        self.__nombre = nombre
        self.__modelo = modelo
        self.__calibre = calibre
        self.__numSerie = numSerie
        self.__sistemaDisparo_id = sistemaDisparo_id
        self.__materiales = materiales
        self.__peso = peso
        self.__costo = costo

    def get_nombre(self):
        return self.__nombre

    def get_modelo(self):
        return self.__modelo

    def get_calibre(self):
        return self.__calibre

    def get_numSerie(self):
        return self.__numSerie

    def get_sistemaDisparo_id(self):
        return self.__sistemaDisparo_id

    def get_materiales(self):
        return self.__materiales

    def get_peso(self):
        return self.__peso

    def get_costo(self):
        return self.__costo
