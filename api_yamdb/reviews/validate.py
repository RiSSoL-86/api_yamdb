from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидация даты выхода Произведения."""
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'Внимание: дата выхода Произведения - {value}',
            f'не может превышать - {now}!!!'
        )
