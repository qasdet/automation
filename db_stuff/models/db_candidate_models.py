from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    PrimaryKeyConstraint,
    Text,
    Uuid,
    text,
)
from sqlalchemy.orm import declarative_base, mapped_column


Base = declarative_base()


class UserCandidates(Base):
    __tablename__ = 'user_candidates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_candidates_pkey'),
        Index('user_candidates_name_idx', 'name'),
        Index('user_candidates_surname_idx', 'surname'),
        Index('user_candidates_email_idx', 'email'),
        Index('user_candidates_firm_name_idx', 'firm_name'),
        Index('user_candidates_phone_idx', 'phone'),
        Index('user_candidates_comments_idx', 'comments'),
        Index('user_candidates_is_performed_idx', 'is_performed'),
        Index('user_candidates_role_idx', 'role'),
        Index('user_candidates_created_at_idx', 'created_at'),
        Index('user_candidates_deleted_at_idx', 'deleted_at'),
        Index('user_candidates_updated_at_idx', 'updated_at')
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    surname = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    firm_name = mapped_column(Text, nullable=False)
    phone = mapped_column(Text, nullable=False)
    comments = mapped_column(Text, nullable=False)
    is_performed = mapped_column(Boolean, nullable=False, server_default=text('false'))
    role = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    deleted_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
