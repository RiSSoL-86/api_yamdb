from django.core.mail import send_mail


def send_mail_confirmation_code(user, confirmation_code):
    """Отправка кода подтверждения пользователю на почту."""
    send_mail(
        subject='Код подтверждения для доступа к API.',
        message=(
            f'Доброе время суток, {user.username}.\n'
            f'Код подтверждения для доступа к API: {confirmation_code}'
        ),
        recipient_list=[user.email],
        from_email='test@mail.ru',
        fail_silently=True,
    )
