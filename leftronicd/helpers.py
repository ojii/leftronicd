# -*- coding: utf-8 -*-
from importlib import import_module

def load(method_path):
    module_name, method_name = method_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, method_name)

def get_interval(name):
    return {
        'daily': 24 * 60 * 60,
        'hourly': 60 * 60,
        'minutely': 60,
    }.get(name, int(name))
