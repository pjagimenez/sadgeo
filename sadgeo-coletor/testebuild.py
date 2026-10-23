# -*- coding: utf-8 -*-

import pkgutil
import importlib
import sidgeo

for m in pkgutil.walk_packages(sidgeo.__path__, 'sidgeo.'):
    print('Importando', m.name)
    importlib.import_module(m.name)
    

print("Todos os imports OK")
