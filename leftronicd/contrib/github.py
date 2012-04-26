# -*- coding: utf-8 -*-
from leftronicd.helpers import get_page
from twisted.python import log
import base64
import json

def repo_metric(repo, metric, username=None, password=None):
    headers = {}
    if username and password:
        headers['Authorization'] = 'Basic %s' % (base64.b64encode('%s:%s' % (username, password)))
        log.msg('[github.repo_metric] Using authentication')
    else:
        log.msg('[github.repo_metric] No authentication')
    url = 'https://api.github.com/repos/%s' % repo
    log.msg('[github.repo_metric] Sending request to %s' % url)
    def handler(data):
        log.msg('[github.repo_metric] Got response')
        log.msg('[github.repo_metric] Loading data')
        data = json.loads(data)
        log.msg('[github.repo_metric] Returning value')
        return data[metric]
    return get_page(handler, url, headers=headers)
