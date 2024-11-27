from http import HTTPStatus

from fastapi import FastAPI

from fastapi.responses import FileResponse

import os

from fastapi.staticfiles import StaticFiles

from fast_zero.schemas import Message, UserDB, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)
    return user_with_id


# Verifica se o diretório de cobertura existe
if os.path.exists("htmlcov"):
    app.mount("/coverage", StaticFiles(directory="htmlcov"), name="coverage")
else:
    print(
        "Diretório htmlcov não encontrado. Execute `task test` para gerar o relatório."
    )


@app.get("/coverage/{file_path:path}")
async def serve_coverage_files(file_path: str):
    """
    Serve arquivos estáticos do diretório htmlcov.
    """
    base_path = "htmlcov"
    file_location = os.path.join(base_path, file_path)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    return {"error": "File not found"}
