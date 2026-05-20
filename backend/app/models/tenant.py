"""Tenant — construtora cliente do SaaS."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Tenant(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "tenant"

    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    razao_social: Mapped[str | None] = mapped_column(String(200))
    cnpj: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    plano: Mapped[str] = mapped_column(String(20), default="free", nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
