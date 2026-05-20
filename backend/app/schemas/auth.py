"""Auth schemas."""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole
from app.schemas.common import ORMModel


class SignupRequest(BaseModel):
    construtora_nome: str = Field(min_length=2, max_length=200)
    cnpj: str = Field(min_length=11, max_length=20)
    user_nome: str = Field(min_length=2, max_length=200)
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(ORMModel):
    id: UUID
    tenant_id: UUID
    email: str
    nome: str
    role: UserRole
    ativo: bool


class MeResponse(BaseModel):
    user: UserOut
    tenant_nome: str
