from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc


class Slack_Dialog_Submissions:

    def __init__(self, data, channel, team_id):
        self.data       = data
        self.submission = Misc.get_value(data,'submission')
        self.channel    = channel
        self.team_id    = team_id

    def send_message(self,message):
        if self.channel:
            slack_message(message, [], self.channel, self.team_id)
        return message

    def handle(self):
        if self.data and self.submission:
            action  = self.data.get('callback_id')
            try:
                target = getattr(self,action)
            except:
                return self.send_message(':red_circle: Sorry, action not recognized : {0}'.format(action))
            try:
                response = target()
                return self.send_message(':point_right: {0}'.format(response))
            except Exception as error:
                return self.send_message(':red_circle: Sorry, there was an error executing the requested action: {0}'.format(error))
        return "no data : {0}".format(self.data)

    def jira_create_issue(self):
        project     = self.submission.get('project')
        issue_type  = self.submission.get('issue_type')
        summary     = self.submission.get('summary')
        description = self.submission.get('description')
        if summary    : summary     = summary.replace('+', ' ')
        if description: description = description.replace('+', ' ')
        else          : description = ''

        if project and issue_type and summary:
            self.send_message('Creating new `{0}` issue on project `{1}` with summary `{2}` and description `{3}`'.format(issue_type, project, summary,description))

            from osbot_jira.api.jira_server.API_Jira import API_Jira
            try:
                result = API_Jira().issue_create(project, summary, description, issue_type)
                new_issue_id = "{0}".format(result)
                self.submission['issue_id'] = new_issue_id
                self.show_issue_screnshot()
                jira_link = "https://jira.photobox.com/browse/{0}".format(new_issue_id)
                return 'Created issue: <{0}|{1}>'.format(jira_link,new_issue_id)
            except Exception as error:
                return ':red_circle: Error creating issue: {0}'.format(error)
        return ':red_circle: Error in Slack_Dialog_Submissions.jira_create_issue. Missing required values from submission data: `{0}`'.format(self.submission)

        #slack_message('Creating issue: {0}'.format(self.submission), [], self.channel, self.team_id)

    def show_issue_screnshot(self):
        issue_id = self.submission.get('issue_id')
        if issue_id:
            payload = {'params': [issue_id], 'channel': self.channel, 'team_id': self.team_id}
            Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)
            return ':point_right: Screenshot of `{0}` send to channel `{1}`'.format(issue_id, self.channel)
        else:
            return ':red_circle: in Slack_Dialog_Submissions.show_issue_screnshot, no `issue_id` was provided'