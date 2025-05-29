# store/validators.py
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_age_18(value):
    today = datetime.date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Вам должно быть не менее 18 лет для регистрации.")