#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.

from django.utils.safestring import mark_safe
from django.forms import widgets
from political_profiles.models import *

class AutoCompleter(widgets.TextInput):
    CLIENT_CODE = """
        <script type="text/javascript">
             jQuery(document).ready(function(){
                jQuery('#%(id)s').autocomplete("Hello, %(data)s".split(', '), {max: %(limit)d});
             });
        </script>
    """

    def __init__(self, model, field, *args, **kwargs):
        super(AutoCompleter, self).__init__(*args, **kwargs)
        self.items = model.objects.values_list(field, flat=True).order_by(field)
        

    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        data = ", ".join(self.items)
        limit = 15
        
        result = super(AutoCompleter, self).render(*args, **kwargs)

        return result + mark_safe(self.CLIENT_CODE % dict(id=html_id, data=data, limit=limit))