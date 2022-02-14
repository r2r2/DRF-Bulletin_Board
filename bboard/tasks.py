from datetime import timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from Bullboard_project.settings import DEFAULT_FROM_EMAIL
from bboard.models import Post, User


# Schedule configured in Django Admin panel
def send_mail_about_new_posts():
    """Sending every week emails with links on a Posts"""
    post_list = Post.objects.filter(created__range=[timezone.now() - timedelta(days=7), timezone.now()])
    user_list = User.objects.all()

    for user in user_list:
        html_content = render_to_string(
            'bboard/weekly_email.html',
            {
                'posts': post_list,
                'user': user,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"[Bulletin Board]{user.username} take a look on a new posts",
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
