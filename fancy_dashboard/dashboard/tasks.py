# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from fancy_dashboard.bitbucket.models.client import BitbucketClient
from fancy_dashboard.jira.models import JiraClient
from .utils.pullrequest import get_pullrequests
from .utils.release import get_releases
from .utils.sprint import get_sprint_issues


@shared_task
def load_pullrequests():
    for client in BitbucketClient.objects.all():
        get_pullrequests(
            client,
        )


@shared_task
def load_releases():
    for client in JiraClient.objects.all():
        get_releases(
            client,
        )


@shared_task
def load_sprint_issues():
    for client in JiraClient.objects.all():
        get_sprint_issues(
            client,
        )
