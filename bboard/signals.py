from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Post


@receiver(signal=post_save, sender=Comment)
def notify_about_comment(sender, instance, **kwargs):
    """Send mail to Post owner about new comment"""
    # If comment accepted == False
    if not instance.accepted:
        post_owner = Post.objects.get(comment=instance).owner
        send_mail(
            subject=f'{post_owner.username} you have new comment',
            message=f'{instance}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f'{post_owner.email}'],
            fail_silently=False
        )


@receiver(signal=post_save, sender=Comment)
def notify_about_comment(sender, instance, **kwargs):
    """Send mail to Comment owner that it's accepted"""
    if instance.accepted:
        comment_owner = Comment.objects.get(owner=instance.owner).owner
        send_mail(
            subject=f'{comment_owner.username} your comment accepted',
            message=f'Your comment:{instance.text} to post: {instance.post.text} was accepted',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f'{comment_owner.email}'],
            fail_silently=False
        )
