from random import randint

from django.core.mail import send_mail


def send_mail_confirmation_code(data):
    """Отправка кода подтверждения пользователю на почту."""
    send_mail(
        subject=data['email_subject'],
        message=data['email_message'],
        recipient_list=[data['to_email']],
        from_email='test@mail.ru',
        fail_silently=True,
    )


def generation_confirmation_code():
    """Генератор кода подтверждения."""
    confirmation_code = randint(111111, 999999)
    return confirmation_code
