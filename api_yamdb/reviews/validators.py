from django.utils import timezone
from rest_framework.serializers import ValidationError


def validate_year(year):
    """Метод для валидации года при создании произведения."""
    if year > timezone.now().year:
        raise ValidationError(f'Неверный год: {year}: Нельзя добавлять '
                              f'произведения, которые еще не вышли')
