import json
import requests
from pandas import json_normalize
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
from datetime import datetime
import config
import os 

# API URL
github_api = "https://api.github.com"
github_repo = ""

# Create a session
github_session = requests.Session()
github_session.auth = (config.gh_user, config.gh_token)

# Start Timestamp
start_time = datetime.now()


# Get repository information
def repo_info(repo, owner, api):
    url = api + '/repos/{}/{}'.format(owner, repo)
    repo_info = github_session.get(url=url)
    repo_info_list = repo_info.json()
    # Get id of the repository
    id_repo = repo_info_list['id']
    name_repo = repo_info_list['name']
    url_repo = repo_info_list['html_url']

    #General information of the repository
    generalInfo = [id_repo, name_repo, url_repo ]
    return generalInfo
repos = json_normalize(repo_info('DeepSpeed', 'microsoft', github_api))
repos.to_csv('data/repos.csv', sep=';')

# Id of the repository
id_general_repo = repo_info('DeepSpeed', 'microsoft', github_api)[1]
print(id_general_repo)



# Get the commits
def commits_of_repo(repo, owner, api):
    commits = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
        commit_pg = github_session.get(url=url)
        commit_pg_list = commit_pg.json()

        # Procesar y guardar la información de los commits
        for commit_data in commit_pg_list:
            sha = commit_data["sha"]
            login = commit_data["author"]["login"]
            creation_date = commit_data["commit"]["author"]["date"]
            # Verificar si "author" es None y si contiene "id"
            if commit_data.get("author") is not None and "id" in commit_data["author"]:
                author_id = commit_data["author"]["id"]
            else:
                author_id = "ID Desconocido"
            id_repository = id_general_repo

            # Agregar la información a la lista
            commits.append({
                "SHA del commit": sha,
                "Login": login,
                "Fecha de creación": creation_date,
                "ID del author": author_id,
                "ID repositorio": id_repository
            })

        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits

commits = json_normalize(commits_of_repo('DeepSpeed', 'microsoft', github_api))
commits.to_csv('data/commits.csv')

# Get the closed pulls
def closed_pulls_of_repo(repo, owner, api):
    closed_pulls = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/pulls?state=closed&page={}&per_page=100'.format(owner, repo, i)
        pull_pg = github_session.get(url=url)
        pull_pg_list = pull_pg.json()

        # Procesar y guardar la información de los pulls
        for closed_pull_data in pull_pg_list:
            id_pull = closed_pull_data["id"]
            name = closed_pull_data["title"]
            id_user = closed_pull_data["user"]["id"]
            login = closed_pull_data["user"]["login"]
            status = closed_pull_data["state"]
            created_at = closed_pull_data["created_at"]
            closed_at = closed_pull_data["closed_at"]
            id_commit = closed_pull_data["merge_commit_sha"]
            id_repository = id_general_repo
            

            # Agregar la información a la lista
            closed_pulls.append({
                "ID pull": id_pull,
                "Name": name,
                "ID Usuario": id_user,
                "Login": login,
                "Estado": status,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "ID commit": id_commit,
                "ID repositorio": id_repository
            })

        if 'Link' in pull_pg.headers:
            if 'rel="next"' not in pull_pg.headers['Link']:
                next = False
        i = i + 1
    return closed_pulls

# Get the open pulls
def open_pulls_of_repo(repo, owner, api):
    open_pulls = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/pulls?state=open&page={}&per_page=100'.format(owner, repo, i)
        pull_pg = github_session.get(url=url)
        pull_pg_list = pull_pg.json()

        # Procesar y guardar la información de los pulls
        for pull_data in pull_pg_list:
            id_pull = pull_data["id"]
            name = pull_data["title"]
            id_user = pull_data["user"]["id"]
            login = pull_data["user"]["login"]
            status = pull_data["state"]
            created_at = pull_data["created_at"]
            closed_at = pull_data["closed_at"]
            id_commit = pull_data["merge_commit_sha"]
            id_repository = id_general_repo
            

            # Agregar la información a la lista
            open_pulls.append({
                "ID pull": id_pull,
                "Name": name,
                "ID Usuario": id_user,
                "Login": login,
                "Estado": status,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "ID commit": id_commit,
                "ID repositorio": id_repository
            })

        if 'Link' in pull_pg.headers:
            if 'rel="next"' not in pull_pg.headers['Link']:
                next = False
        i = i + 1
    return open_pulls

# Combine open_pulls and closed_pulls
pulls = json_normalize( closed_pulls_of_repo('DeepSpeed', 'microsoft', github_api) + open_pulls_of_repo('DeepSpeed', 'microsoft', github_api))
pulls.to_csv('data/pulls.csv')


# Get the open_issues
def open_issues_of_repo(repo, owner, api):
    issues = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/issues?page={}&per_page=100'.format(owner, repo, i)
        issue_pg = github_session.get(url=url)
        issue_pg_list = issue_pg.json()

        # Procesar y guardar la información de los issues
        for issue_data in issue_pg_list:

            if "pull_request" in issue_data:
                continue 
             
            id_issue = issue_data["id"]
            name = issue_data["title"]
            id_user = issue_data["user"]["id"]
            login = issue_data["user"]["login"]
            created_at = issue_data["created_at"]
            closed_at = issue_data["closed_at"]
            status = issue_data["state"]
            id_repository = id_general_repo
            resolution_time = None
            

            # Agregar la información a la lista
            issues.append({
                "ID issue": id_issue,
                "Name": name,
                "ID Usuario": id_user,
                "Login": login,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "Estado": status,
                "Tiempo de resolución": resolution_time,
                "ID repositorio": id_repository
            })

        if 'Link' in issue_pg.headers:
            if 'rel="next"' not in issue_pg.headers['Link']:
                next = False
        i = i + 1
    return issues

#Get the closed_issues
def closed_issues_of_repo(repo, owner, api):
    closed_issues = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/issues?state=closed&page={}&per_page=100'.format(owner, repo, i)
        issue_pg = github_session.get(url=url)
        issue_pg_list = issue_pg.json()

        # Procesar y guardar la información de los issues
        for issue_data in issue_pg_list:
            
            if "pull_request" in issue_data:
                continue 

            id_issue = issue_data["id"]
            name = issue_data["title"]
            id_user = issue_data["user"]["id"]
            login = issue_data["user"]["login"]
            created_at = issue_data["created_at"]
            closed_at = issue_data["closed_at"]
            status = issue_data["state"]
            id_repository = id_general_repo
            #Parse resolution_time
            resolution_time = (datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')).total_seconds()

            # Agregar la información a la lista
            closed_issues.append({
                "ID issue": id_issue,
                "Name": name,
                "ID Usuario": id_user,
                "Login": login,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "Estado": status,
                "Tiempo de resolución": resolution_time,
                "ID repositorio": id_repository
            })

        if 'Link' in issue_pg.headers:
            if 'rel="next"' not in issue_pg.headers['Link']:
                next = False
        i = i + 1
    return closed_issues

#Get the issues
issues = json_normalize( open_issues_of_repo('DeepSpeed', 'microsoft', github_api) + closed_issues_of_repo('DeepSpeed', 'microsoft', github_api))
issues.to_csv('data/issues.csv', sep=';')


#Finish timestamp
finish_time = datetime.now()

# Time elapsed
time_elapsed = finish_time - start_time
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))



