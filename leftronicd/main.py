# -*- coding: utf-8 -*-
from leftronic import Leftronic
from leftronicd.constants import IDLE, RUNNING
from leftronicd.helpers import get_interval, load
from twisted.internet import task, reactor
from twisted.python import log
from twisted.web.client import getPage
import json
import sys
import yaml


class TwistedLeftronic(Leftronic):
    def postData(self, parameters):
        """ Makes an HTTP POST to the API URL. """
        log.msg('[TwistedLeftronic.postData] Preparing to post %s' % parameters)
        # add the access key
        parameters['accessKey'] = self.accessKey

        if self.cryptoKey:
            self.encryptStreams(parameters)

        # Convert to JSON
        data = json.dumps(parameters)
        log.msg('[TwistedLeftronic.postData] Posting %s to %s' % (data, self.apiUrl))
        deferred = getPage(self.apiUrl, method='POST', postdata=data)
        def log_success(value):
            log.msg('[TwistedLeftronic.postData] Post of %s to %s was successful' % (data, self.apiUrl))
        def log_error(value):
            log.err('[TwistedLeftronic.postData] Post of %s to %s failed' % (data, self.apiUrl))
        deferred.addCallback(log_success)
        deferred.addErrback(log_error)


class Stream(object):
    """
    A leftronic stream
    """
    def __init__(self, daemon, config):
        self.daemon = daemon
        self.interval = get_interval(config.pop('interval'))
        self.method_path = config.pop('method')
        self.method = load(self.method_path)
        self.name = config.pop('name')
        self.verbosename = config.pop('verbosename')
        self.type = config.pop('type')
        self.kwargs = config
        self.state = IDLE

    def get_interval(self):
        return self.interval

    def execute(self):
        log.msg("[Stream(%s).execute]" % self.name)
        if self.state != IDLE:
            log.msg("[Stream(%s).execute] Not idle, ignoring..." % self.name)
            return
        log.msg("[Stream(%s).execute] Calling %s(**%s)" % (self.name, self.method_path, self.kwargs))
        self.state = RUNNING
        self.callback(self.method(**self.kwargs))

    def callback(self, value):
        log.msg("[Stream(%s).callback] Got value: %s" % (self.name, value))
        method = getattr(self.daemon.leftronic, 'push%s' % self.type.capitalize())
        method(self.name, value)
        self.state = IDLE
        log.msg("[Stream(%s).callback] Back to idling..." % self.name)


class LeftronicDaemon(object):
    """
    The daemon
    """
    def __init__(self, config):
        self.leftronic = TwistedLeftronic(config['accesskey'])
        self.loops = []
        self.streams = []
        for streamconf in config['streams']:
            stream = Stream(self, streamconf)
            self.streams.append(stream)
        log.msg("[LeftronicDaemon.run] Initialized with %s streams" % len(self.streams))
    
    def run(self):
        log.msg("[LeftronicDaemon.run] Starting...")
        for stream in self.streams:
            loop = task.LoopingCall(stream.execute)
            loop.start(stream.get_interval())
            self.loops.append(loop)
        reactor.run()

def cli():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', type=argparse.FileType('r'))
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose')
    args = parser.parse_args()
    config = yaml.load(args.configfile)
    if args.verbose:
        log.startLogging(sys.stdout)
    daemon = LeftronicDaemon(config)
    daemon.run()

if __name__ == '__main__':
    cli()
