from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Repository schemas
class RepositoryBase(BaseModel):
    name_repository: str
    url_repository: str

class RepositoryCreate(RepositoryBase):
    pass

class Repository(RepositoryBase):
    id_repository: int

    class Config:
        orm_mode = True

# User schemas
class UserBase(BaseModel):
    name_user: str
    experience: str
    id_repository: int
    id_user: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    
    class Config:
        orm_mode = True

# Commit schemas
class CommitBase(BaseModel):
    id_commit: int
    created_at_commit: datetime
    id_user: int
    id_repository: int

class CommitCreate(CommitBase):
    pass

class Commit(CommitBase):
    class Config:
        orm_mode = True

# Issue schemas
class IssueBase(BaseModel):
    name_issue: str
    created_at_issue: datetime
    updated_at_issue: datetime
    resolution_time: int
    id_user: int
    id_resolution_commit: int
    id_repository: int

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    id_issue: int

    class Config:
        orm_mode = True

# PullRequest schemas
class PullRequestBase(BaseModel):
    name_pr: str
    created_at_pr: datetime
    status: str
    id_user: int
    id_repository: int
    id_commit: int

class PullRequestCreate(PullRequestBase):
    pass

class PullRequest(PullRequestBase):
    id_pr: int

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

