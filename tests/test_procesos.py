import unittest
from time import sleep
from pathlib import Path

from jutils.procesos import Proceso, Paso


class Paso1(Paso):
    def _run(self, a) -> dict:
        super()._run()
        print("Haciendo algo pesado")
        sleep(10)
        print("Terminando de hacer algo pesado")
        return {"paso1": a * 4}


class Paso2(Paso):
    def _run(self, paso1) -> dict:
        super()._run()
        print("Haciendo algo pesado")
        sleep(10)
        print("Terminando de hacer algo pesado")
        return {"paso2": paso1 + 6}


class Paso3(Paso):
    def _run(self, paso2) -> dict:
        super()._run()
        print("Haciendo algo pesado")
        sleep(10)
        print("Terminando de hacer algo pesado")
        return {"paso3": paso2 ** 2}


class Paso4(Paso):
    def _run(self, paso3) -> dict:
        super()._run()
        print("Haciendo algo pesado")
        sleep(10)
        print("Terminando de hacer algo pesado")
        return {"paso4": paso3 - 10}


class Procesamiento(Proceso):
    def __init__(self, cache, cache_path, a, force_execution: dict):
        super().__init__(cache, cache_path)
        self._a = a
        self._paso1 = Paso1("Paso1")
        self._paso2 = Paso2("Paso2", self._paso1)
        self._paso3 = Paso3("Paso3", self._paso2)
        self._paso4 = Paso4("Paso4", self._paso3)
        self._force_execution = force_execution

    def paso1(self, force_execution=None):
        if force_execution is None:
            force_execution = {}
        r = self._paso1.run(a=self._a, force_execution=force_execution.setdefault("paso1", False))
        self.save_cache()
        return r

    def paso2(self, force_execution=None):
        if force_execution is None:
            force_execution = {}
        r = self._paso2.run(a=self._a, force_execution=force_execution.setdefault("paso2", False))
        self.save_cache()
        return r

    def paso3(self, force_execution=None):
        if force_execution is None:
            force_execution = {}
        r = self._paso3.run(a=self._a, force_execution=force_execution.setdefault("paso3", False))
        self.save_cache()
        return r

    def paso4(self, force_execution=None):
        if force_execution is None:
            force_execution = {}
        r = self._paso4.run(a=self._a, force_execution=force_execution.setdefault("paso4", False))
        self.save_cache()
        return r


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._path = Path(r'cache/procesamiento.pkl').resolve().absolute()
        self._a = 5
        self._paso1 = self._a * 4
        self._paso2 = self._paso1 + 6
        self._paso3 = self._paso2 ** 2
        self._paso4 = self._paso3 - 10
        self._force_execution = {'paso4': False, 'paso1': False}

    def test1_paso1_cache(self):
        procesamiento_def = Procesamiento(cache=True, cache_path=self._path, a=self._a,
                                          force_execution=self._force_execution)
        procesamiento = Procesamiento.from_cache(procesamiento_def, True, self._path)
        self.assertEqual(procesamiento.paso1(self._force_execution)['paso1'], self._paso1)

    def test2_paso2_cache(self):
        procesamiento_def = Procesamiento(cache=True, cache_path=self._path, a=self._a,
                                          force_execution=self._force_execution)
        procesamiento = Procesamiento.from_cache(procesamiento_def, True, self._path)
        self.assertEqual(procesamiento.paso2(self._force_execution)['paso2'], self._paso2)

    def test3_paso4_cache(self):
        procesamiento_def = Procesamiento(cache=True, cache_path=self._path, a=self._a,
                                          force_execution=self._force_execution)
        procesamiento = Procesamiento.from_cache(procesamiento_def, True, self._path)
        self.assertEqual(procesamiento.paso4(self._force_execution)['paso4'], self._paso4)

    def test4_paso3_cache(self):
        procesamiento_def = Procesamiento(cache=True, cache_path=self._path, a=self._a,
                                          force_execution=self._force_execution)
        procesamiento = Procesamiento.from_cache(procesamiento_def, True, self._path)
        self.assertEqual(procesamiento.paso3(self._force_execution)['paso3'], self._paso3)


if __name__ == '__main__':
    unittest.main()
