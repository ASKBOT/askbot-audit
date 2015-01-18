from askbot.models import Post
from askbot.models import Thread
from askbot.models import User
from askbot.models.signals import post_revision_published
from django.conf import settings as django_settings
from django.db import models
import datetime


class AdminTag(models.Model):
    name = models.CharField(max_length=128)


class AuditedThread(models.Model):
    thread = models.ForeignKey(Thread, related_name='thread_audit_flags')
    timestamp = models.DateTimeField(auto_now_add=True)


class AuditedPost(models.Model):
    post = models.ForeignKey(Post, related_name='post_audit_flags')
    author = models.ForeignKey(User, related_name='post_audit_flags'
    admin_tags = models.ManyToManyField(AdminTag, related_name='post_audit_flags')
    language_code = models.CharField(
                            choices=django_settings.LANGUAGES,
                            default=django_settings.LANGUAGE_CODE,
                            max_length=16,
                        )
    audited_thread = models.ForeignKey(
                                AuditedThread,
                                related_name='post_audit_flags' 
                            )
    timestamp = models.DateTimeField(auto_now_add=True)


def add_item_to_queue(sender, revision, **kwargs):
    if not post.is_qa_content():
        return

    now = datetime.datetime.now()

    post = revision.post
    thread = post.thread
    at, created = AuditedThread.objects.get_or_create(thread=thread)
    at.timestamp = now
    at.save()
    ap, created = AuditedPost.objects.get_or_create(
                                                audited_thread=at,
                                                post=post
                                            )
    ap.author = revision.author
    ap.language_code = post.language_code
    ap.timestamp = now
    ap.save()


post_revision_published.connect(add_item_to_queue)
