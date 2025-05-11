from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from  django.conf import settings

# utils function to send verification email to the user
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    current_site = get_current_site(request)

    verification_url = f'http://{current_site.domain}/accounts/verify/{uid}/{token}/'

    subject = 'OneStopShop: Verify your email address'

    email_body = render_to_string('verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })

    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.content_subtype = 'html'
    email.send()