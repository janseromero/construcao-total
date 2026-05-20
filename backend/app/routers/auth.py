"""Auth endpoints: signup, login, me."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, MeResponse, SignupRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse:
    cnpj_clean = "".join(c for c in payload.cnpj if c.isdigit())
    if db.scalar(select(Tenant).where(Tenant.cnpj == cnpj_clean)):
        raise HTTPException(status.HTTP_409_CONFLICT, "CNPJ já cadastrado")

    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")

    tenant = Tenant(nome=payload.construtora_nome, cnpj=cnpj_clean)
    db.add(tenant)
    db.flush()

    user = User(
        tenant_id=tenant.id,
        email=payload.email,
        nome=payload.user_nome,
        senha_hash=hash_password(payload.password),
        role=UserRole.proprietario,
        ativo=True,
    )
    db.add(user)
    db.commit()

    token = create_access_token(str(user.id), {"tenant_id": str(tenant.id), "role": user.role.value})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
    if not user.ativo:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuário inativo")
    token = create_access_token(
        str(user.id), {"tenant_id": str(user.tenant_id), "role": user.role.value}
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MeResponse:
    tenant = db.get(Tenant, user.tenant_id)
    return MeResponse(user=UserOut.model_validate(user), tenant_nome=tenant.nome if tenant else "")
