"""User."""

from enum import StrEnum
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class UserRole(StrEnum):
    proprietario = "proprietario"
    operacional = "operacional"


class User(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "user_account"
    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),)

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.operacional
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tenant = relationship("Tenant", back_populates="users")
