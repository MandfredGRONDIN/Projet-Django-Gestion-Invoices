import re
from django.core.exceptions import ValidationError

def validate_french_phone_number(value):
    pattern = r'^(?:(?:\+33|0)[1-9](?:[ .-]?[0-9]{2}){4})$'
    if not re.match(pattern, value):
        raise ValidationError(f'{value} n\'est pas un numéro de téléphone valide en France. '
                              'Un exemple de numéro valide est : 01 23 45 67 89.')