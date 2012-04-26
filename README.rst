##########
Leftronicd
##########

A script to periodically post information to leftronic.com


************
Installation
************

* Make a virtualenv
* ``pip install leftronicd``


*************
Configuration
*************

Configuration is done in yaml.

accesskey
=========

Your leftronic API access key.

streams
=======

A list of stream configurations.

Each stream requires following values:

* ``method``: The method that generates the value
* ``type``: The type of value (eg ``number`` or ``leaderboard``)
* ``name``: Name of the stream
* ``verbosename``: Verbose name of the stream
* ``interval``: Interval in seconds when the method should be called.

Any other key-value pairs will be passed into the method.

Example:: 

    accesskey: SECRET
    streams:
        - method: leftronicd.contrib.github.repo_metric
          verbosename: django CMS Watchers
          name: django-cms-watchers
          type: number
          interval: 86400
          repo: divio/django-cms
          metric: watchers
        - method: leftronicd.contrib.github.repo_metric
          verbosename: django CMS Forks
          type: number
          interval: 86400
          name: django-cms-forks
          repo: divio/django-cms
          metric: forks


****************
Built-in methods
****************


``leftronicd.contrib.github.repo_metric``
=========================================

Reports a metric from a github repository.

Configuration:

* ``repo``: The repo name, eg ``ojii/leftronicd``
* ``metric``: Which value to grab from the repo, eg ``forks``

Optional configuration:

* ``username``: The username (for private repos)
* ``password``: The password (for private repos)


*******
Running
*******

``leftronicd <configfile> [-v]``


**************
Custom methods
**************

Custom data collecting methods can be any Python callable that returns a
`Twisted Deferred`_ which calls attached callbacks with the value to be posted
to leftronic.com.

The Python callable is called with all additional configuration parameters
given for a stream.

Example
=======

This example will show the amount of GitHub followers a user has.

Python code (let's assume it's in a module called 'custom')::

    from leftronicd.helpers import get_page
    import json
    
    def github_followers(username):
        def handler(data):
            return json.loads(data)['followers']
        return get_page(handler, 'https://api.github.com/users/%s' % username)

As you can see, we use the ``leftronicd.helpers.get_page`` helper here, for
details, see below.

Stream configuration::

    accesskey: SECRET
    streams:
        - method: custom.github_followers
          verbosename: Github Followers
          name: my-github-followers
          type: number
          interval: 300
          username: ojii


*******
Helpers
*******

``leftronicd.helpers.get_page``
===============================

A wrapper around ``twisted.web.client.getPage``. Takes a handler function as
first argument which is called with the content of the page if the page is
loaded successful. The handler function should then return the value to be
passed to leftronic. ``get_page`` returns a deferred which can be returned from
your custom methods.

All arguments after the handler argument are the same as in
``twisted.web.client.getPage``.


.. _Twisted Deferred: http://twistedmatrix.com/documents/current/core/howto/defer.html
