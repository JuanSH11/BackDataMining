from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import controllers, models, schemas
from fastapi.middleware.cors import CORSMiddleware
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origines (no usar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos, se puede especificar: ["GET", "POST"]
    allow_headers=["*"],  
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Repositories functions
@app.get("/repositories/", response_model=List[schemas.Repository])
def read_repositories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repositories = controllers.get_repositories(db, skip=skip, limit=limit)
    return repositories

@app.get("/repositories/{repository_id}", response_model=schemas.Repository)
def read_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository(db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository

@app.post("/repositories/", response_model=schemas.Repository)
def create_repository(repository: schemas.RepositoryCreate, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository_by_name(db, repository_name=repository.name_repository)
    if db_repository:
        raise HTTPException(status_code=400, detail="Repository already registered")
    return controllers.create_repository(db=db, repository=repository)

# Users functions
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = controllers.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = controllers.get_user_by_name(db, user_name=user.name_user)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return controllers.create_user(db=db, user=user)

# Commits functions
@app.get("/commits/", response_model=List[schemas.Commit])
def read_commits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    commits = controllers.get_commits(db, skip=skip, limit=limit)
    return commits

@app.get("/commits/{commit_id}", response_model=schemas.Commit)
def read_commit(commit_id: int, db: Session = Depends(get_db)):
    db_commit = controllers.get_commit(db, commit_id=commit_id)
    if db_commit is None:
        raise HTTPException(status_code=404, detail="Commit not found")
    return db_commit

@app.post("/commits/", response_model=schemas.Commit)
def create_commit(commit: schemas.CommitCreate, db: Session = Depends(get_db)):
    db_commit = controllers.get_commit_by_id(db, commit_id=commit.id_commit)
    if db_commit:
        raise HTTPException(status_code=400, detail="Commit already registered")
    return controllers.create_commit(db=db, commit=commit)

# Pull Requests functions
@app.get("/pull_requests/", response_model=List[schemas.PullRequest])
def read_pull_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pull_requests = controllers.get_pull_requests(db, skip=skip, limit=limit)
    return pull_requests

@app.get("/pull_requests/{pull_request_id}", response_model=schemas.PullRequest)
def read_pull_request(pull_request_id: int, db: Session = Depends(get_db)):
    db_pull_request = controllers.get_pull_request(db, pull_request_id=pull_request_id)
    if db_pull_request is None:
        raise HTTPException(status_code=404, detail="Pull Request not found")
    return db_pull_request

@app.post("/pull_requests/", response_model=schemas.PullRequest)
def create_pull_request(pull_request: schemas.PullRequestCreate, db: Session = Depends(get_db)):
    db_pull_request = controllers.get_pull_request_by_id(db, pull_request_id=pull_request.id_pr)
    if db_pull_request:
        raise HTTPException(status_code=400, detail="Pull Request already registered")
    return controllers.create_pull_request(db=db, pull_request=pull_request)

# Issues functions
@app.get("/issues/", response_model=List[schemas.Issue])
def read_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    issues = controllers.get_issues(db, skip=skip, limit=limit)
    return issues

@app.get("/issues/{issue_id}", response_model=schemas.Issue)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue(db, issue_id=issue_id)
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue

@app.post("/issues/", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue_by_id(db, issue_id=issue.id_issue)
    if db_issue:
        raise HTTPException(status_code=400, detail="Issue already registered")
    return controllers.create_issue(db=db, issue=issue)

# Issues functions
@app.get("/issues/", response_model=schemas.Issue)
def read_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    issues = controllers.get_issues(db, skip=skip, limit=limit)
    return issues

@app.get("/issues/{issue_id}", response_model=schemas.Issue)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue(db, issue_id=issue_id)
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue

@app.post("/issues/", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue_by_id(db, issue_id=issue.id_issue)
    if db_issue:
        raise HTTPException(status_code=400, detail="Issue already registered")
    return controllers.create_issue(db=db, issue=issue)

# Functions for the relationships between tables
@app.get("/users/{user_id}/commits/", response_model=List[schemas.Commit])
def read_commits_by_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.commits

@app.get("/users/{user_id}/pull_requests/", response_model=List[schemas.PullRequest])
def read_pull_requests_by_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.pull_requests

@app.get("/users/{user_id}/issues/", response_model=List[schemas.Issue])
def read_issues_by_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.issues

@app.get("/repositories/{repository_id}/users/", response_model=List[schemas.User])
def read_users_by_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository(db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository.users

@app.get("/repositories/{repository_id}/commits/", response_model=schemas.Commit)
def read_commits_by_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository(db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository.commits

@app.get("/repositories/{repository_id}/pull_requests/", response_model=schemas.PullRequest)
def read_pull_requests_by_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository(db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository.pull_requests

@app.get("/repositories/{repository_id}/issues/", response_model=schemas.Issue)
def read_issues_by_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = controllers.get_repository(db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository.issues

@app.get("/commits/{commit_id}/user/", response_model=schemas.User)
def read_user_by_commit(commit_id: int, db: Session = Depends(get_db)):
    db_commit = controllers.get_commit(db, commit_id=commit_id)
    if db_commit is None:
        raise HTTPException(status_code=404, detail="Commit not found")
    return db_commit.user

@app.get("/commits/{commit_id}/repository/", response_model=schemas.Repository)
def read_repository_by_commit(commit_id: int, db: Session = Depends(get_db)):
    db_commit = controllers.get_commit(db, commit_id=commit_id)
    if db_commit is None:
        raise HTTPException(status_code=404, detail="Commit not found")
    return db_commit.repository

@app.get("/pull_requests/{pull_request_id}/user/", response_model=schemas.User)
def read_user_by_pull_request(pull_request_id: int, db: Session = Depends(get_db)):
    db_pull_request = controllers.get_pull_request(db, pull_request_id=pull_request_id)
    if db_pull_request is None:
        raise HTTPException(status_code=404, detail="Pull Request not found")
    return db_pull_request.user

@app.get("/pull_requests/{pull_request_id}/repository/", response_model=schemas.Repository)
def read_repository_by_pull_request(pull_request_id: int, db: Session = Depends(get_db)):
    db_pull_request = controllers.get_pull_request(db, pull_request_id=pull_request_id)
    if db_pull_request is None:
        raise HTTPException(status_code=404, detail="Pull Request not found")
    return db_pull_request.repository

@app.get("/pull_requests/{pull_request_id}/commit/", response_model=schemas.Commit)
def read_commit_by_pull_request(pull_request_id: int, db: Session = Depends(get_db)):
    db_pull_request = controllers.get_pull_request(db, pull_request_id=pull_request_id)
    if db_pull_request is None:
        raise HTTPException(status_code=404, detail="Pull Request not found")
    return db_pull_request.commit

@app.get("/issues/{issue_id}/user/", response_model=schemas.User)
def read_user_by_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue(db, issue_id=issue_id)
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue.user

@app.get("/issues/{issue_id}/repository/", response_model=schemas.Repository)
def read_repository_by_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue(db, issue_id=issue_id)
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue.repository

@app.get("/issues/{issue_id}/commit/", response_model=schemas.Commit)
def read_commit_by_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = controllers.get_issue(db, issue_id=issue_id)
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue.resolution_commit
