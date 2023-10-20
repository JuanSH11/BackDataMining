from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Repository schemas
class RepositoryBase(BaseModel):
    name_repository: str
    url_repository: str
    id_repository: str

class RepositoryCreate(RepositoryBase):
    pass

class Repository(RepositoryBase):
    
    class Config:
        orm_mode = True

# User schemas
class UserBase(BaseModel):
    id_user: str
    login_user: str
    experience: Optional[str] = None
    id_repository: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    
    class Config:
        orm_mode = True

# Commit schemas
class CommitBase(BaseModel):
    id_commit: str
    created_at_commit: datetime
    id_user: str
    id_repository: str

class CommitCreate(CommitBase):
    pass

class Commit(CommitBase):
    class Config:
        orm_mode = True

# Issue schemas
class IssueBase(BaseModel):
    id_issue: str
    name_issue: str
    created_at_issue: datetime
    updated_at_issue: datetime
    resolution_time: int
    id_user: str
    id_resolution_commit: str
    id_repository: str

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    class Config:
        orm_mode = True

# PullRequest schemas
class PullRequestBase(BaseModel):
    id_pull: str
    name: str
    created_at: datetime
    closed_at: Optional[datetime] = None
    status: str
    id_user: str
    id_repository: str
    id_commit: Optional[str] = None

class PullRequestCreate(PullRequestBase):
    pass

class PullRequest(PullRequestBase):
    class Config:
        orm_mode = True

# User-PullRequest association schemas
# class UserPullRequestAssociationBase(BaseModel):
#     id_user: int
#     id_pr: int

# class UserPullRequestAssociationCreate(UserPullRequestAssociationBase):
#     pass

# class UserPullRequestAssociation(UserPullRequestAssociationBase):
#     pass

#     class Config:
#         orm_mode = True

