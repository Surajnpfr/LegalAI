from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False)
    document_type = Column(String(100), nullable=False)
    language = Column(String(20), default="ne")
    source_url = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sections = relationship(
        "LegalSection",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class LegalSection(Base):
    __tablename__ = "legal_sections"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    section_number = Column(String(100), nullable=True)
    chapter = Column(String(500), nullable=True)
    heading = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="sections")