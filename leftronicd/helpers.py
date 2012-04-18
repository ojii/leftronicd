# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

def load(method_path):
    module_name, method_name = method_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, method_name)

def td2s(td):
    return (td.days * 24 * 3600) + td.seconds

def intervalify(name):
    return {
        'daily': datetime.timedelta(days=1),
        'hourly': datetime.timedelta(hours=1),
    }[name]

def get_interval(name):
    return td2s(intervalify(name))
