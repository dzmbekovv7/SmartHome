from django import forms

class PricePredictionForm(forms.Form):
    area = forms.FloatField(label='Площадь (м²)', min_value=1)
    bedrooms = forms.IntegerField(label='Спальни', min_value=0)
    bathrooms = forms.IntegerField(label='Ванные комнаты', min_value=0)
    floors = forms.IntegerField(label='Этажей', min_value=1)
    has_pool = forms.BooleanField(label='Есть бассейн?', required=False)
    property_type = forms.ChoiceField(
        label='Тип недвижимости', choices=[
            ('Квартира', 'Квартира'),
            ('Дом', 'Дом'),
            ('Вилла', 'Вилла'),
            ('Коттедж', 'Коттедж'),
            ('Участок', 'Участок')
        ]
    )
    region = forms.ChoiceField(
        label='Регион', choices=[
            ('Бишкек', 'Бишкек'),
            ('Иссык-Кульская область', 'Иссык-Кульская область'),
            ('Чуйская область', 'Чуйская область'),
            ('Ошская область', 'Ошская область'),
            ('Джалал-Абадская область', 'Джалал-Абадская область')
        ]
    )
