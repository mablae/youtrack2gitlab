# Skeleton of a CLI

import click
import gitlab
import youtrack2gitlab
import requests
from bs4 import BeautifulSoup

def getIssues(s):
	r = s.get(youtrack2gitlab.youtrack.get('host')+'/rest/export/'+youtrack2gitlab.youtrack.get('project')+'/issues?max=500')

	bs = BeautifulSoup(r.text) 
	issues = []

	for issue in bs.findAll("issue"):
		gitlab_issue = {}
		for field in issue.findAll("field"): 	
			gitlab_issue[field['name']] =  field.value.text
			
		issues.append(gitlab_issue)
		print(gitlab_issue['reporterName'])
	return issues

def getComments(s, issue_id):
	r = s.get(youtrack2gitlab.youtrack.get('host')+'/rest/issue/'+issue_id+'/comment')
	bs = BeautifulSoup(r.text) 
	comments = []

	for comment in bs.findAll("comment"):
		print(comment['author'])
		gl_note = { 'body' : comment['text'], 'author' : comment['author'] }
		comments.append(gl_note)
	return comments

def getGitlabUserIdByYoutrackUser(username):
	return youtrack2gitlab.config["user_mapping"][username]

@click.command('y2g_migrate')
def cli():
	git = gitlab.Gitlab(youtrack2gitlab.config["gitlab"]["host"])
	git.login(youtrack2gitlab.config["gitlab"]["username"], )

	s = requests.session()
	payload = {
		'login' : youtrack2gitlab.config["youtrack"]["user"],
		'password' : youtrack2gitlab.config["gitlab"]["password"]
	}
	r = s.post(youtrack2gitlab.config["youtrack"]["host"]+'/rest/user/login', data=payload)
	   

	issues = getIssues(s)
	issue_count = 0
	for issue in issues:
		if ((issue['State'] != 'Behoben') & (issue['State'] != 'Verifiziert')):

			gl_issue = {}
			gl_issue['id'] =  youtrack2gitlab.config["gitlab"]["project_id"]
			gl_issue['title'] = issue['summary']
			if 'description' in issue:
				gl_issue['description'] = issue['description']
			else:
				gl_issue['description'] = ""
	  
			git.setsudo(getGitlabUserIdByYoutrackUser(issue['reporterName']))
			new_issue = git.createissue(gl_issue['id'], gl_issue['title'], description = gl_issue['description'])
			
			comments = getComments(s, youtrack2gitlab.config["youtrack"]["project"] + '-' + str(issue['numberInProject']))
			for comment in comments:
				git.setsudo(getGitlabUserIdByYoutrackUser(comment['author']))
				git.createissuewallnote(gl_issue['id'], new_issue['id'], comment['body'])

			issue_count += 1
	print("Migrated "+ str(issue_count) + " issues...")