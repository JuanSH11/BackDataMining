import os
from fastapi import Depends, FastAPI, HTTPException, Request
import httpx
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import controllers, models, schemas
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/login")

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


# Assets como carpeta estática
app.mount("/static", StaticFiles(directory="assets"), name="static")

templates = Jinja2Templates(directory="templates")

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
def read_commits_by_user(user_id: str, db: Session = Depends(get_db)):
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

# Ruta de vista principal
@app.get("/")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Ruta de autenticacion
@app.get("/github-login")
async def github_login():
    # Redirigir a la página de inicio de sesión de GitHub
    github_auth_url = "https://github.com/login/oauth/authorize?client_id=e9ebb07c3b330ccadf1c&scope=user"
    return RedirectResponse(url=github_auth_url)

# Define la URL de autorización y otros valores
GITHUB_CLIENT_ID = "e9ebb07c3b330ccadf1c"
GITHUB_CLIENT_SECRET = "31292aaab1032c10d9f6e8874c1e8764417bf844"
GITHUB_REDIRECT_URI = "http://localhost:8000/callback"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_INFO_URL = "https://api.github.com/user"

@app.get("/callback")
async def github_callback(request: Request):
    # Obtiene el código de autorización de la URL de redirección
    code = request.query_params.get("code")
    
    if not code:
        raise HTTPException(status_code=400, detail="Código de autorización no encontrado")

    # Configura los datos que se enviarán en la solicitud POST para obtener el token de acceso
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI,
    }

    # Realiza la solicitud POST a la URL de autorización de GitHub
    async with httpx.AsyncClient() as client:
        response = await client.post(GITHUB_ACCESS_TOKEN_URL, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="No se pudo obtener el token de acceso")

    # La respuesta de GitHub contendrá el token de acceso
    token_data = response.text
    access_token = token_data.split("&")[0].split("=")[1]

    # Guardar login del usuario
    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_USER_INFO_URL, headers={"Authorization": f"token {access_token}"})
    user_data = response.json()

    # Guardar login y token del usuario 
    token_data = {"gh_user": user_data["login"], "gh_token": access_token}

    with open("config.json", "w") as json_file:
        json.dump(token_data, json_file)

    # Redirigir a una página de éxito 
    return RedirectResponse(url="/repo-info")

@app.post("/success")
async def form_data(request: Request):
    form = await request.form()
    owner = form["owner"]
    name = form["name"]

    print(owner)


    # Verificar que los campos "owner" y "name" no estén vacíos 
    if owner.strip() != "" and name.strip() != "":
        # Los campos son válidos, proceder a guardarlos en un archivo JSON (puedes utilizar el código que mencionaste antes)
        # Leer el archivo JSON existente, si lo hay
        existing_data = {}
        if os.path.isfile("config.json"):
            with open("config.json", "r") as json_file:
                existing_data = json.load(json_file)

        # Agregar los nuevos datos
        existing_data["owner"] = owner
        existing_data["name"] = name

        # Guardar el archivo JSON con los datos existentes y nuevos
        with open("config.json", "w") as json_file:
            json.dump(existing_data, json_file)
        print(existing_data)
        return RedirectResponse(url="/progress", status_code=302)
    else:
        raise HTTPException(status_code=400, detail="Los campos 'owner' y 'name' son inválidos")


# Ruta de vista formulario
@app.get("/repo-info")
async def form(request: Request):
    return templates.TemplateResponse("repo-info.html", {"request": request})


def get_gh_token():
    # Get credentials
    with open('config.json', 'r') as file:
        token_data = json.load(file)

    gh_token = token_data['gh_token']

    if gh_token:
        return gh_token
    else:
        raise HTTPException(status_code=401, detail="No se ha autenticado con GitHub")

@app.get("/ruta_protegida")
async def ruta_protegida(token: str = Depends(get_gh_token)):
    # Lógica de la ruta protegida
    return {"message": "Ruta protegida. Acceso autorizado."}

@app.get("/progress")
async def progress(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})

@app.get("/get-progress")
async def get_progress(db: Session = Depends(get_db)):
    progress = controllers.get_latest_progress(db)
    return {"progress": progress.percentage, "message": progress.message}

