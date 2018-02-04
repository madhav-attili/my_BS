Pfizer Site Module
==================

This module is named after your site subscription name.  IMPORTANT: this module is required, and is your ticket to a full functioning site.

* Add all modules required for your site as dependencies
* Create a hook_update and .install file to enable any newly required modules
* Use this as your base feature, including the default services endpoint

Default Services Endpoint
=========================

This is extremely important!  We have included the default services endpoint that lives at site.com/wf

You must keep this services endpoint defined here or else WF Tools will not function!

Also you must update this with additional resources that your site requires.  You can do this by going to admin/structure/services/list/wf_endpoint/resources and adding additional resources that pertain to your site.
Once you've updated these, you need to re-export the feature using drush fu [pfizer_site_module].  This is the preferred method.
