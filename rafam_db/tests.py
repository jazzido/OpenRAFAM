import unittest
from rafam_db.dataset import EstadoEjecucionGastos
from rafam_db.dataset import EstadoEjecucionRecursos
from rafam_db.dataset import VersionesRafam

from rafam_db.db import init_engine

class DatasetTest(unittest.TestCase):
    def setUp(self):
        self.engine = init_engine('invitado', 'xxxxx', 'xxxxx', 'xxxxx')


class EstadoEjecucionTest(DatasetTest):
    def test2014(self):
        self.scrapeEstadoEjecucionPorAnio(2014)

    def test2015(self):
        self.scrapeEstadoEjecucionPorAnio(2015)

    def scrapeEstadoEjecucionPorAnio(self, year):
        print("\nEstado de Ejecucion {0}".format(year))
        dataset = EstadoEjecucionGastos(self.engine)
        dataset.scrape(year=year, confirmado="N")
        for row in dataset.rows[:10]:
            print(row)

        with open('datasets/estadoejecucion_{0}.csv'.format(year), 'w') as f:
            dataset.toCSV(f)


class VersionesRafamTest(DatasetTest):
    def test(self):
        print("\nVersiones RAFAM")
        dataset = VersionesRafam(self.engine)
        for row in dataset.scrape():
            print(row)

        with open('datasets/versionesrafam.csv', 'w') as f:
            dataset.toCSV(f)


class EstadoEjecucionRecursosTest(DatasetTest):
    def test(self):
        year = 2015
        print("\nEstado de Ejecucion Recursos {0}".format(year))
        dataset = EstadoEjecucionRecursos(self.engine)
        dataset.scrape(year=year)
        for row in dataset.rows[:10]:
            print(row)

        with open('datasets/EstadoEjecucionRecursos_{0}.csv'.format(year), 'w') as f:
            dataset.toCSV(f)

if __name__ == '__main__':
    unittest.main()
