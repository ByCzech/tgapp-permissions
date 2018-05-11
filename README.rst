.. image:: https://travis-ci.org/axant/tgapp-permissions.svg?branch=master
   :target: https://travis-ci.org/axant/tgapp-permissions
.. image:: https://coveralls.io/repos/github/axant/tgapp-permissions/badge.svg?branch=master
   :target: https://coveralls.io/github/axant/tgapp-permissions?branch=master

About tgapp-permissions
-------------------------

tgapp-permissions is a Pluggable application for TurboGears2.
tgapp-userprofile allows admins of your application to assign the users of your application to
groups, and since groups are bound to permissions to assign permissions to your users

Installing
-------------------------------

tgapp-permissions can be installed both from pypi or from github::

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

other special options that can be used with tgapppermissions are:

- **exclusive_permissions** (default False): only a group can be assigned to a user
- **query_groups**: function that is called by the template, must return a ``list of tuples`` where
  each entry is composed of the `_id` of the group and it's `display_name`. you can customize this
  function to filter or and sort groups if you don't want to show every group in your database
