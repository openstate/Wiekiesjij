from django import forms

class TemplateForm(object):
    """
    Mixin to render forms from a predefined template
    
    Give the form a _template_name property for the name of the template_name to use
    
    Example template:
    
    ``utils/forms/_form.html``:
        {% if form.errors or form.non_field_errors %}
        <tr>
            <td colspan="2" class="error">
                <div class="form-errors">
                    <span class="cross"></span>
                    <div>
                        <h1>Error</h1>
                        <ul>
                        {% for error in form.non_field_errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                        {% for field in form %}{% for error in field.errors %}
                            <li>{{ field.label }}: {{ error }}</li>
                        {% endfor %}{% endfor %}
                        </ul>        
                    </div>
                </div>
            </td>
        </tr>
        {% endif %}
        {% for field in form %}
            {% include "utils/forms/_form_field.html" %}
        {% endfor %}
    
    ``utils/forms/_form_field.html``:
        <tr {% if field.errors %}class="error"{% endif %}>
            <th {% if field.field.required %}class="required"{% endif %}>
                <label for="{{ field.auto_id }}">{{ field.label.title }}</label>
            </th>
            <td class="input">
                {{ field }}
                <div class="help">
                    {{ field.help_text }}
                </div>
            </td>
        </tr>
    """
    
    @property
    def form_class_name(self):
        return '.'.join([self.__module__, self.__class__.__name__.lower()])

    def as_template(self):
        """
        Renders a form from a template
        """
        
        template_name = getattr(self, '_template_name', 'utils/forms/form.html')            
        self.tpl = loader.get_template(template_name)

        context_dict = dict(
            non_field_errors=self.non_field_errors(),
            fields=[ forms.forms.BoundField(self, field, name) for name, field in self.fields.iteritems()],
            errors=self.errors,
            data=self.data,
            form=self,
        )

        if getattr(self, 'initial', None):
            context_dict.update(dict(initial=self.initial))
        if getattr(self, 'instance', None):
            context_dict.update(dict(instance=self.instance))
        if getattr(self, 'cleaned_data', None):
            context_dict.update(dict(cleaned_data=self.cleaned_data))

        return self.tpl.render(
            Context(context_dict)
        )