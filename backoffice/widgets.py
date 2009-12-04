#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.

from django.utils.safestring import mark_safe
from django.forms import widgets
from political_profiles.models import *

class AutoCompleter(widgets.TextInput):
    CLIENT_CODE = """
        <input type="text" name="%(id)s_text" id="%(id)s_text"/>
        <input type="hidden" name="%(id)s" id="%(id)s" value="" />
        <script type="text/javascript">
             jQuery(document).ready(function(){
                autocomplete('#%(id)s_text', "%(data)s", '#%(id)s', %(limit)d, '');
             });
        </script>
    """

    def __init__(self, model, field, *args, **kwargs):
        super(AutoCompleter, self).__init__(*args, **kwargs)
        modelObj = globals()[model] #self.model is now an object of the class 'model'
        self.items = modelObj.objects.values_list(field, flat=True).order_by(field)
        

    def render(self, name, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', name)
        data = ", ".join(self.items)
        limit = 15

        return mark_safe(self.CLIENT_CODE % dict(id=html_id, data=data, limit=limit))