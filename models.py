from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table

Base = declarative_base()

class Repository(Base):
    __tablename__ = 'repositories'

    id_repository = Column(Integer, primary_key=True)
    name_repository = Column(String)
    url_repository = Column(String)

    # Relaciones
    pull_requests = relationship('PullRequest', back_populates='repository')
    users = relationship('User', back_populates='repository')
    commits = relationship('Commit', back_populates='repository')
    issues = relationship('Issue', back_populates='repository')

class Issue(Base):
    __tablename__ = 'issues'

    id_issue = Column(Integer, primary_key=True, index=True)
    name_issue = Column(String, index=True)
    created_at_issue = Column(DateTime, index=True)
    updated_at_issue = Column(DateTime, index=True)
    resolution_time = Column(Integer)
    id_user = Column(Integer, ForeignKey('users.id_user'), index=True)
    id_resolution_commit = Column(Integer, ForeignKey('commits.id_commit'), index=True)
    id_repository = Column(Integer, ForeignKey('repositories.id_repository'), index=True)

    # Relaciones
    user = relationship('User', back_populates='issues')
    resolution_commit = relationship('Commit', back_populates='resolved_issue')
    repository = relationship('Repository', back_populates='issues')

class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True)
    name_user = Column(String, index=True)
    experience = Column(String)
    id_repository = Column(Integer, ForeignKey('repositories.id_repository'), index=True)

    # Relaciones
    repository = relationship('Repository', back_populates='users')
    pull_requests = relationship('PullRequest', secondary='user_pull_request_association', back_populates='users')
    commits = relationship('Commit', back_populates='user')
    issues = relationship('Issue', back_populates='user')

class Commit(Base):
    __tablename__ = 'commits'

    id_commit = Column(Integer, primary_key=True, index=True)
    created_at_commit = Column(DateTime, index=True)
    id_user = Column(Integer, ForeignKey('users.id_user'), index=True)
    id_repository = Column(Integer, ForeignKey('repositories.id_repository'), index=True)

    # Relaciones
    user = relationship('User', back_populates='commits')
    repository = relationship('Repository', back_populates='commits')
    resolved_issue = relationship('Issue', back_populates='resolution_commit')
    pull_request = relationship('PullRequest', back_populates='commit', uselist = False)

class PullRequest(Base):
    __tablename__ = 'pull_requests'

    id_pr = Column(Integer, primary_key=True, index=True)
    name_pr = Column(String, index=True)
    created_at_pr = Column(DateTime, index=True)
    status = Column(String, index=True)
    id_user = Column(Integer, ForeignKey('users.id_user'), index=True)
    id_repository = Column(Integer, ForeignKey('repositories.id_repository'), index=True)
    id_commit = Column(Integer, ForeignKey('commits.id_commit'), index=True)

    # Relaciones
    repository = relationship('Repository', back_populates='pull_requests')
    users = relationship('User', secondary='user_pull_request_association', back_populates='pull_requests')
    commit = relationship('Commit', back_populates='pull_request')

# Tabla de asociación para la relación muchos a muchos entre User y PullRequest
user_pull_request_association = Table('user_pull_request_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id_user')),
    Column('pull_request_id', Integer, ForeignKey('pull_requests.id_pr'))
)
