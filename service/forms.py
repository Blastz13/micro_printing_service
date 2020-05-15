from django import forms
from django.forms.widgets import Select
from django.core.exceptions import ValidationError


CHOICES = [
    ("10x15 Lomond глянец (Германия)", "10x15 Lomond глянец (Германия)"),
    ("10x15 Noname глянец (Китай)", "10x15 Noname глянец (Китай)"),
    ("15x21 Lomond глянец (Германия)", "15x21 Lomond глянец (Германия)"),
    ("15x21 Noname глянец (Китай)", "15x21 Noname глянец (Китай)"),
    ("21x30 Lomond глянец (Германия)", "21x30 Lomond глянец (Германия)"),
    ("21x30 Noname глянец (Китай)", "21x30 Noname глянец (Китай)"),
    ("21x30 Офисная бумага (Россия)", "21x30 Офисная бумага (Россия)"),
    ("30x40 Lomond глянец (Германия)", "30x40 Lomond глянец (Германия)"),
    ("30x40 Noname глянец (Китай)", "30x40 Noname глянец (Китай)"),
    ("30x40 Офисная бумага (Россия)", "30x40 Офисная бумага (Россия)"),

    ("15x21 Lomond матовая (Германия)", "15x21 Lomond матовая (Германия)"),
    ("15x21 Noname матовая (Китай)", "15x21 Noname матовая(Китай)"),
    ("21x30 Lomond матовая (Германия)", "21x30 Lomond матовая (Германия)"),
    ("21x30 Noname матовая (Китай)", "21x30 Noname матовая(Китай)"),
    ("30x40 Lomond матовая (Германия)", "30x40 Lomond матовая (Германия)"),
    ("30x40 Noname матовая (Китай)", "30x40 Noname матовая(Китай)"),
]

CHOICES_ATTRS = [
    ("10x15 Lomond глянец (Германия)", "10x15 Lomond глянец (Германия)", "8"),
    ("10x15 Noname глянец (Китай)", "10x15 Noname глянец (Китай)", "6"),
    ("15x21 Lomond глянец (Германия)", "15x21 Lomond глянец (Германия)", "26"),
    ("15x21 Noname глянец (Китай)", "15x21 Noname глянец (Китай)", "20"),
    ("21x30 Lomond глянец (Германия)", "21x30 Lomond глянец (Германия)", "55"),
    ("21x30 Noname глянец (Китай)", "21x30 Noname глянец (Китай)", "40"),
    ("21x30 Офисная бумага (Россия)", "21x30 Офисная бумага (Россия)", "20"),
    ("30x40 Lomond глянец (Германия)", "30x40 Lomond глянец (Германия)", "180"),
    ("30x40 Noname глянец (Китай)", "30x40 Noname глянец (Китай)", "120"),
    ("30x40 Офисная бумага (Россия)", "30x40 Офисная бумага (Россия)", "50"),

    ("15x21 Lomond матовая (Германия)", "15x21 Lomond матовая (Германия)", "22"),
    ("15x21 Noname матовая (Китай)", "15x21 Noname матовая(Китай)", "18"),
    ("21x30 Lomond матовая (Германия)", "21x30 Lomond матовая (Германия)", "45"),
    ("21x30 Noname матовая (Китай)", "21x30 Noname матовая(Китай)", "35"),
    ("30x40 Lomond матовая (Германия)", "30x40 Lomond матовая (Германия)", "150"),
    ("30x40 Noname матовая (Китай)", "30x40 Noname матовая(Китай)", "100"),
]


class CustomSelectWidget(Select):

    def __init__(self, attrs=None, choices=(), disabled_choices=()):
        super(Select, self).__init__(attrs, choices=choices)
        # disabled_choices is a list of disabled values
        self.disabled_choices = disabled_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(Select, self).create_option(name, value, label, selected, index, subindex, attrs)
        for choices in self.disabled_choices:
            if value in choices:
                option['attrs']['data-price'] = choices[2]
        return option


class CreateOrderForm(forms.Form):
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'field', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'field', 'placeholder': 'Имя'}))
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'field', 'type': 'tel',
                                                        'pattern': '^\+7\d{3}\d{7}$',
                                                        'value': '+7', 'maxlength': '12'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'field', 'min': '1',
                                                                  'step': '1', 'value': '1',
                                                                  'placeholder': 'Количество'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'field', 'style': 'resize: vertical;'}), required=False)
    photos = forms.ImageField(label='Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple', 'class': 'field'}))
    total_price = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))
    accept_conditions = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['size'] = forms.CharField(label='size',  widget=CustomSelectWidget(choices=CHOICES,
                                                                                       disabled_choices=CHOICES_ATTRS,
                                                                                       attrs={'class': 'field'}))

    def clean(self):
        cleaned_data = super(CreateOrderForm, self).clean()

        for choices in CHOICES_ATTRS:
            if (cleaned_data['size'] in choices) and (int(choices[2]) * int(cleaned_data['quantity']) == int(cleaned_data['total_price'])):
                return
        raise ValidationError('Error')
