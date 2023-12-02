from datetime import datetime
from typing import Tuple
from pydantic import Field

from pydantic import BaseModel


class User(BaseModel):
    email: str = Field(description="The email of the user", example="123@asd.com", min_length=3, max_length=50,
                       regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str | None = None
    disabled: bool | None = None



# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/?h=header#update-the-dependencies