# -*- coding: utf-8 -*-
from twisted.python import log
import json
import requests

def repo_metric(repo, metric, username=None, password=None):
    auth = None
    if username and password:
        auth = (username, password)
        log.msg('[github.repo_metric] Using authentication')
    else:
        log.msg('[github.repo_metric] No authentication')
    url = 'https://api.github.com/repos/%s' % repo
    log.msg('[github.repo_metric] Sending request to %s' % url)
    response = requests.get(url, auth=auth)
    log.msg('[github.repo_metric] Got response: %s' % response.status_code)
    response.raise_for_status()
    log.msg('[github.repo_metric] Loading data')
    data = json.loads(response.content)
    log.msg('[github.repo_metric] Returning value')
    return data[metric]
