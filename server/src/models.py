from enum import Enum
from typing import Optional, List
from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field


class Community(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    description: Optional[str] = None

    properties: List["Property"] = Relationship(back_populates="community")

    pet_policies: List["PetPolicy"] = Relationship(back_populates="community")


class Property(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    description: str | None
    bedrooms: float = 1.0
    bathrooms: float = 1.0
    garage: bool = False
    available_date: Optional[str] = None
    base_rent: float = 0.0
    special_offer: Optional[str] = None
    community_id: int = Field(foreign_key="community.id")
    community: Community = Relationship(back_populates="properties")


class PetType(Enum):
    CAT = "cat"
    DOG = "dog"


class PetPolicy(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    community_id: int = Field(foreign_key="community.id")
    pet_type: PetType
    extra_pet_fee: float = 0.0
    community: Community = Relationship(back_populates="pet_policies")


class MessageType(Enum):
    AI = "ai"
    HUMAN = "human"


class Message(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    timestamp: datetime = Field(default_factory=datetime.now)
    content: str
    type: MessageType
