"""Audit log."""

from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class AuditAcao(StrEnum):
    create = "create"
    update = "update"
    delete = "delete"
    approve = "approve"
    cancel = "cancel"


class AuditLog(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "audit_log"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("user_account.id", ondelete="SET NULL")
    )
    entidade: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entidade_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    acao: Mapped[AuditAcao] = mapped_column(SAEnum(AuditAcao, name="audit_acao"), nullable=False)
    payload_antes: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    payload_depois: Mapped[dict[str, Any] | None] = mapped_column(JSON)
