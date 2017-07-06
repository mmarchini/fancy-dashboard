import arrow
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest
from pybitbucket.repository import Repository
from pybitbucket.auth import BasicAuthenticator
from django.views.generic import DetailView
from braces.views import JSONResponseMixin

from fancy_dashboard.bitbucket.models import BitbucketClient


def get_user_for_activity(activity):
    for value in activity.values():
        if 'user' in value:
            return value['user']
        elif 'author' in value:
            return value['author']


def get_pullrequests(username, password, email):
    bitbucket = Client(
        BasicAuthenticator(
            username,  # Username
            password,  # Password/API Key
            email,  # E-mail
        )
    )

    repositories = [repo.slug for repo in Repository.find_repositories_by_owner_and_role(role='owner', client=bitbucket)]

    pull_requests = []
    for repo in repositories:
        for pr in PullRequest.find_pullrequests_for_repository_by_state(repo, client=bitbucket):
            if type(pr) == dict:
                continue
            pull_request = {}
            activity = list(pr.activity())

            # Get approvals
            approvals = filter(lambda a: 'approval' in a, activity)

            pull_request['approvals'] = [
                {
                    'display_name': a['approval']['user']['display_name'],
                    'avatar': a['approval']['user']['links']['avatar']
                } for a in approvals
            ]

            # Get last update
            pull_request['updated_on'] = arrow.get(pr.updated_on).datetime
            pull_request['updated_by'] = get_user_for_activity(activity[0])['display_name']

            # Get author
            pull_request['author'] = pr.author.display_name

            #
            pull_request['key'] = "{repo}-{pr_id}".format(repo=repo.upper(), pr_id=pr.id)

            # Get task count
            pull_request['task_count'] = pr.task_count

            # Get last build
            statuses = list(pr.statuses())
            if 'pagelen' in statuses[0]:
                statuses.pop()
            statuses = sorted(statuses, key=lambda s: arrow.get(s['updated_on']).datetime, reverse=True)
            print("Build count:", len(statuses))
            pull_request['build_count'] = len(statuses)
            pull_request['last_build'] = None
            if len(statuses):
                pull_request['last_build'] = statuses[0]['state']
            pull_requests.append(pull_request)

    return pull_requests


class PullRequestDashboardView(JSONResponseMixin, DetailView):
    model = BitbucketClient

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context_dict = {
            "pull_requests": get_pullrequests(
                self.object.username,
                self.object.password,
                self.object.email,
            )
        }

        return self.render_json_response(context_dict)
