# -*- coding: utf-8 -*-
from importlib import import_module
from twisted.internet.defer import Deferred
from twisted.web.client import getPage

def load(method_path):
    module_name, method_name = method_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, method_name)

def get_page(handler, *args, **kwargs):
    deferred = Deferred()
    def callback(data):
        output = handler(data)
        deferred.callback(output)
    getPage(*args, **kwargs).addCallback(callback)
    return deferred
