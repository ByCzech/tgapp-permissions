.. image:: https://travis-ci.org/axant/tgapp-permissions.svg?branch=master
   :target: https://travis-ci.org/axant/tgapp-permissions
.. image:: https://coveralls.io/repos/github/axant/tgapp-permissions/badge.svg?branch=master
   :target: https://coveralls.io/github/axant/tgapp-permissions?branch=master

About tgapp-permissions
-------------------------

tgapp-permissions is a Pluggable application for TurboGears2.

Installing
-------------------------------

tgapp-permissions can be installed both from pypi or from bitbucket::

    pip install tgapppermissions

should just work for most of the users

Plugging tgapp-permissions
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with tgapppermissions::

    plug(base_config, 'tgapppermissions')

You will be able to access the plugged application at
*http://localhost:8080/tgapppermissions*.

Available Hooks
----------------------

tgapp-permissions makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

tgapp-permissions exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

