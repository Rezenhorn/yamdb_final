from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.serializers import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    """Запрет на username "me" и проверка на допустимые символы."""
    regex = r'^[\w.@+-]+\Z'

    def __call__(self, value):
        regex_matches = self.regex.search(str(value))
        invalid_input = (
            regex_matches if self.inverse_match else not regex_matches)
        if invalid_input:
            raise ValidationError('Недопустимые символы в username.'
                                  'Допустимы только буквы, цифры и @/./+/-/_')
        elif (value.lower() == 'me'):
            raise ValidationError('Username "me" запрещен.')
        return value
