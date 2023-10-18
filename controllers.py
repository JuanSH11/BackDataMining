from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import or_
import datetime

# Repositories functions
def get_repository(db: Session, repository_id: int):
    return db.query(models.Repository).filter(models.Repository.id_repository == repository_id).first()

def get_repository_by_id(db: Session, repository_name: str):
    return db.query(models.Repository).filter(models.Repository.name_repository == repository_name).first()

def get_repository_by_name(db: Session, repository_name: str):
    return db.query(models.Repository).filter(models.Repository.name_repository == repository_name).first()

def get_repositories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Repository).offset(skip).limit(limit).all()

def create_repository(db: Session, repository: schemas.RepositoryCreate):
    db_repository = models.Repository(id_repository=repository.id_repository, name_repository=repository.name_repository, url_repository=repository.url_repository)
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

# Users functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id_user == user_id).first()

def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name_user == user_name).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id_user == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id_user= user.id_user, name_user=user.name_user, experience=user.experience, id_repository=user.id_repository)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Commits functions
def get_commit(db: Session, commit_id: int):
    return db.query(models.Commit).filter(models.Commit.id_commit == commit_id).first()

def get_commit_by_id(db: Session, commit_id: int):
    return db.query(models.Commit).filter(models.Commit.id_commit == commit_id).first()

def get_commits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Commit).offset(skip).limit(limit).all()

def create_commit(db: Session, commit: schemas.CommitCreate):
    db_commit = models.Commit(id_commit=commit.id_commit ,created_at_commit=commit.created_at_commit, id_user=commit.id_user, id_repository=commit.id_repository)
    db.add(db_commit)
    db.commit()
    db.refresh(db_commit)
    return db_commit

# Pull Requests functions
def get_pull_request(db: Session, pull_request_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_pr == pull_request_id).first()

def get_pull_request_by_id(db: Session, pull_request_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_pr == pull_request_id).first()

def get_pull_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PullRequest).offset(skip).limit(limit).all()

def create_pull_request(db: Session, pull_request: schemas.PullRequestCreate):
    db_pull_request = models.PullRequest(name_pr=pull_request.name_pr, created_at_pr=pull_request.created_at_pr, status=pull_request.status, id_user=pull_request.id_user, id_repository=pull_request.id_repository, id_commit=pull_request.id_commit)
    db.add(db_pull_request)
    db.commit()
    db.refresh(db_pull_request)
    return db_pull_request

# Issues functions
def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id_issue == issue_id).first()

def get_issue_by_id(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id_issue == issue_id).first()

def get_issues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Issue).offset(skip).limit(limit).all()

def create_issue(db: Session, issue: schemas.IssueCreate):
    db_issue = models.Issue(name_issue=issue.name_issue, created_at_issue=issue.created_at_issue, updated_at_issue=issue.updated_at_issue, resolution_time=issue.resolution_time, id_user=issue.id_user, id_resolution_commit=issue.id_resolution_commit, id_repository=issue.id_repository)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

# Functions for the relationships between tables
def get_commits_by_user(db: Session, user_id: int):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id).all()

def get_pull_requests_by_user(db: Session, user_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_user == user_id).all()

def get_issues_by_user(db: Session, user_id: int):
    return db.query(models.Issue).filter(models.Issue.id_user == user_id).all()

def get_commits_by_repository(db: Session, repository_id: int):
    return db.query(models.Commit).filter(models.Commit.id_repository == repository_id).all()

def get_pull_requests_by_repository(db: Session, repository_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_repository == repository_id).all()

def get_issues_by_repository(db: Session, repository_id: int):
    return db.query(models.Issue).filter(models.Issue.id_repository == repository_id).all()

def get_commits_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id, models.Commit.id_repository == repository_id).all()

def get_pull_requests_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_user == user_id, models.PullRequest.id_repository == repository_id).all()

def get_issues_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.Issue).filter(models.Issue.id_user == user_id, models.Issue.id_repository == repository_id).all()

def get_commits_by_user_and_repository_and_date(db: Session, user_id: int, repository_id: int, date: datetime):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id, models.Commit.id_repository == repository_id, models.Commit.created_at_commit >= date).all()

