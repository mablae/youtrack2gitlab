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

def getGitlabIdByYoutrackUser(username):
	map = { 
		'loe' : 2,
		'mbl' : 4,
		'mkr' : 11,
		'mma' : 6,
		'root' : 1,
		'sja' : 3,
		'Julian_Knauer' : 10
	}
	return map[username]

@click.command('y2g_import')
def cli():
	"""Echo a value `N` number of times"""

	git = gitlab.Gitlab(youtrack2gitlab.gitlab.get('host'))
	git.login('mbl', '45zf!')

	s = requests.session()
	payload = {
	'login' : youtrack2gitlab.youtrack.get('user'),
		'password' : youtrack2gitlab.youtrack.get('password')
	}
	r = s.post(youtrack2gitlab.youtrack.get('host')+'/rest/user/login', data=payload)
	   
	#click.echo(r.text)
	
	issues = getIssues(s)
	issue_count = 0
	for issue in issues:
		if ((issue['State'] != 'Behoben') & (issue['State'] != 'Verifiziert')):
			issue_count += 1
			
			gl_issue = {}
			gl_issue['id'] =  youtrack2gitlab.gitlab.get('project_id')
			gl_issue['title'] = issue['summary']
			if 'description' in issue:
				gl_issue['description'] = issue['description']
			else:
				gl_issue['description'] = ""
	  
			git.setsudo(getGitlabIdByYoutrackUser(issue['reporterName']))
			new_issue = git.createissue(gl_issue['id'], gl_issue['title'], description = gl_issue['description'])
			
			comments = getComments(s, 'SHOP-'+str(issue['numberInProject']))
			for comment in comments:
				git.setsudo(getGitlabIdByYoutrackUser(comment['author']))
				git.createissuewallnote(gl_issue['id'], new_issue['id'], comment['body'])
			
			#print("...")	
			#print(new_issue)	
			#new_issue['description'] = gl_issue['description'] 
			#git.editissue(**new_issue)

			print("Counting "+ str(issue_count) + " issues...")
