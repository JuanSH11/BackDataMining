import json
import requests
from pandas import json_normalize
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
from datetime import datetime
import config
import os
from database import SessionLocal 
import schemas
import controllers




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
    id_repository = repo_info_list['id']
    name_repository = repo_info_list['name']
    url_repository = repo_info_list['html_url']

    #General information of the repository
    repo_info_data = {
        "id_repository": id_repository,
        "name_repository": name_repository,
        "url_repository": url_repository
    }
    return repo_info_data

def load_repo_info_data(db):
    repo_info_data = repo_info('DeepSpeed', 'microsoft', github_api)
    # Usar la función de controlador para crear un nuevo registro de repositorio en la base de datos
    repo = schemas.RepositoryCreate(**repo_info_data)
    controllers.create_repository(db, repo)

# repos = json_normalize(repo_info('DeepSpeed', 'microsoft', github_api))
# repos.to_csv('data/repos.csv', sep=';')

# Id of the repository
id_general_repo = repo_info('DeepSpeed', 'microsoft', github_api)["id_repository"]
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
            id_commit = commit_data["sha"]
            #Verificar si "author" es None y si contiene "login"
            if commit_data.get("author") is not None and "login" in commit_data["author"]:
                login_user = commit_data["author"]["login"]
            else:
                login_user = "Login Desconocido"
            created_at_commit = commit_data["commit"]["author"]["date"]
            # Verificar si "author" es None y si contiene "id"
            if commit_data.get("author") is not None and "id" in commit_data["author"]:
                id_user = commit_data["author"]["id"]
            else:
                id_user = "ID Desconocido"
            id_repository = id_general_repo

            # Agregar la información a la lista
            commits.append({
                "id_commit": id_commit,
                "login_user": login_user,
                "created_at_commit": created_at_commit,
                "id_user": id_user,
                "id_repository": id_repository
            })

        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits

def load_commits_data(db):
    commits_data = commits_of_repo('DeepSpeed', 'microsoft', github_api)
    
    users_to_insert = []
    commits_to_insert = []
    
    for commit_data in commits_data:
        # Usa la función de controlador para crear un nuevo user en la base de datos
        user_data = {
        "id_user": commit_data["id_user"],
        "login_user": commit_data["login_user"],
        "experience": None,
        "id_repository": commit_data["id_repository"]
        }
        users_to_insert.append(schemas.UserCreate(**user_data))

        # Usa la función de controlador para crear un nuevo commit en la base de datos
        commit_data = {
        "id_commit": commit_data["id_commit"],
        "created_at_commit": commit_data["created_at_commit"],
        "id_user": commit_data["id_user"],
        "id_repository": commit_data["id_repository"]
        }
        commits_to_insert.append(schemas.CommitCreate(**commit_data))

    #Insert users in a batch
    for users in users_to_insert:
        controllers.create_user(db, users)
    #Insert commits in a batch
    for commits in commits_to_insert:
        controllers.create_commit(db, commits)

# commits = json_normalize(commits_of_repo('DeepSpeed', 'microsoft', github_api))
# commits.to_csv('data/commits.csv')

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
            login_user = closed_pull_data["user"]["login"]
            status = closed_pull_data["state"]
            created_at = closed_pull_data["created_at"]
            closed_at = closed_pull_data["closed_at"]
            # Verificar si "merged_at" es None (pull request no fue aceptado)
            # Verificar si pull request fue mergeado a rama principal, sino api de GitHub no tiene en cuenta el commit
            if (
                closed_pull_data.get("merged_at") is not None
                and closed_pull_data["base"]["ref"] == "master"
            ):
                id_commit = closed_pull_data["merge_commit_sha"]
            else:
                id_commit = None
            
            id_repository = id_general_repo

            # Agregar la información a la lista
            closed_pulls.append({
                "id_pull": id_pull,
                "name": name,
                "id_user": id_user,
                "login_user": login_user,
                "status": status,
                "created_at": created_at,
                "closed_at": closed_at,
                "id_commit": id_commit,
                "id_repository": id_repository
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
            login_user = pull_data["user"]["login"]
            status = pull_data["state"]
            created_at = pull_data["created_at"]
            closed_at = pull_data["closed_at"]
            id_commit = None
            id_repository = id_general_repo
            

            # Agregar la información a la lista
            open_pulls.append({
                "id_pull": id_pull,
                "name": name,
                "id_user": id_user,
                "login_user": login_user,
                "status": status,
                "created_at": created_at,
                "closed_at": closed_at,
                "id_commit": id_commit,
                "id_repository": id_repository
            })

        if 'Link' in pull_pg.headers:
            if 'rel="next"' not in pull_pg.headers['Link']:
                next = False
        i = i + 1
    return open_pulls

def load_pulls_data(db):
    pulls_data = closed_pulls_of_repo('DeepSpeed', 'microsoft', github_api) + open_pulls_of_repo('DeepSpeed', 'microsoft', github_api)

    pulls_to_insert = []
    users_to_insert = []

    for pull_data in pulls_data:
        # Usa la función de controlador para crear un nuevo user en la base de datos
        user_data = {
        "id_user": pull_data["id_user"],
        "login_user": pull_data["login_user"],
        "experience": None,
        "id_repository": pull_data["id_repository"]
        }
        users_to_insert.append(schemas.UserCreate(**user_data))
        # Usa la función de controlador para crear un nuevo pull request en la base de datos
        pull_data = {
            "id_pull": pull_data["id_pull"],
            "name": pull_data["name"],
            "created_at": pull_data["created_at"],
            "closed_at": pull_data["closed_at"],
            "status": pull_data["status"],
            "id_user": pull_data["id_user"],
            "id_repository": pull_data["id_repository"],
            "id_commit": pull_data["id_commit"]
        }
        pulls_to_insert.append(schemas.PullRequestCreate(**pull_data))
        
    #Insert users in a batch
    for users in users_to_insert:
        controllers.create_user(db, users)
    #Insert pulls in a batch
    for pulls in pulls_to_insert:
        controllers.create_pull_request(db, pulls)
            

# Combine open_pulls and closed_pulls
# pulls = json_normalize( closed_pulls_of_repo('DeepSpeed', 'microsoft', github_api) + open_pulls_of_repo('DeepSpeed', 'microsoft', github_api))
# pulls.to_csv('data/pulls.csv')


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
            login_user = issue_data["user"]["login"]
            created_at = issue_data["created_at"]
            closed_at = issue_data["closed_at"]
            status = issue_data["state"]
            id_repository = id_general_repo
            id_resolution_commit = None
            resolution_time = None
            

            # Agregar la información a la lista
            issues.append({
                "id_issue": id_issue,
                "name": name,
                "id_user": id_user,
                "login_user": login_user,
                "created_at": created_at,
                "closed_at": closed_at,
                "status": status,
                "id_repository": id_repository,
                "id_resolution_commit": id_resolution_commit,
                "resolution_time": resolution_time
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
            login_user = issue_data["user"]["login"]
            created_at = issue_data["created_at"]
            closed_at = issue_data["closed_at"]
            status = issue_data["state"]
            id_repository = id_general_repo
            id_resolution_commit = None
            #Parse resolution_time in hours
            resolution_time = (datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')).total_seconds() / 3600

            # Agregar la información a la lista
            closed_issues.append({
                "id_issue": id_issue,
                "name": name,
                "id_user": id_user,
                "login_user": login_user,
                "created_at": created_at,
                "closed_at": closed_at,
                "status": status,
                "id_repository": id_repository,
                "id_resolution_commit": id_resolution_commit,
                "resolution_time": resolution_time
            })

        if 'Link' in issue_pg.headers:
            if 'rel="next"' not in issue_pg.headers['Link']:
                next = False
        i = i + 1
    return closed_issues

def load_issues_data(db):
    issues_data = open_issues_of_repo('DeepSpeed', 'microsoft', github_api) + closed_issues_of_repo('DeepSpeed', 'microsoft', github_api)

    issues_to_insert = []
    users_to_insert = []

    for issue_data in issues_data:
         # Usa la función de controlador para crear un nuevo user en la base de datos
        user_data = {
        "id_user": issue_data["id_user"],
        "login_user": issue_data["login_user"],
        "experience": None,
        "id_repository": issue_data["id_repository"]
        }
        users_to_insert.append(schemas.UserCreate(**user_data))
        
        # Usa la función de controlador para crear un nuevo issue en la base de datos
        issue_data = {
            "id_issue": issue_data["id_issue"],
            "name": issue_data["name"],
            "created_at": issue_data["created_at"],
            "closed_at": issue_data["closed_at"],
            "status": issue_data["status"],
            "id_user": issue_data["id_user"],
            "id_repository": issue_data["id_repository"],
            "id_resolution_commit": issue_data["id_resolution_commit"],
            "resolution_time": issue_data["resolution_time"]
        }
        issues_to_insert.append(schemas.IssueCreate(**issue_data))

    #Insert users in a batch
    for users in users_to_insert:
        controllers.create_user(db, users)
    #Insert issues in a batch
    for issues in issues_to_insert:
        controllers.create_issue(db, issues)
        


db = SessionLocal()
load_repo_info_data(db)
load_commits_data(db)
load_pulls_data(db)
load_issues_data(db)
controllers.calculate_experience(db)   

db.close()
#Finish timestamp
finish_time = datetime.now()

# Time elapsed
time_elapsed = finish_time - start_time
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))



