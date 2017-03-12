from django.forms import Widget
from django.forms.utils import flatatt
from django.forms.widgets import boolean_check
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import format_html


class DaysOfWeekInput(Widget):
    DAYS_OF_WEEK = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su']

    def __init__(self, attrs=None, check_test=None):
        super(DaysOfWeekInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        days = []
        for x in range(len(self.DAYS_OF_WEEK)):
            current_attrs = self.build_attrs(attrs, type='checkbox', name=name)
            current_attrs['id'] = '{}_{}'.format(current_attrs['id'], x)
            current_attrs['name'] = '{}_{}'.format(current_attrs['name'], x)
            if value and  str(x) in value:
                current_attrs['checked'] = 'checked'
            days.append(format_html(' <span>{}:<input{} /></span>',  self.DAYS_OF_WEEK[x], flatatt(current_attrs)))
        return format_html(''.join(days))

    def value_from_datadict(self, data, files, name):
        days = []
        for x in range(len(self.DAYS_OF_WEEK)):
            current_name = '{}_{}'.format(name, x)
            if current_name not in data:
                # A missing value means False because HTML form submission does not
                # send results for unselected checkboxes.
                continue
            value = data.get(current_name)
            # Translate true and false strings to boolean values.
            values = {'true': True, 'false': False}
            if isinstance(value, six.string_types):
                value = values.get(value.lower(), value)
            if bool(value):
                print('Value is true for day {}: {}'.format(x, value))
                days.append(str(x))
        return ','.join(days)
