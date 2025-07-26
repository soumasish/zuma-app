from typing import Optional, Annotated, List
from sqlmodel import Session, select
from src.models import Community, Property, PetPolicy, PetType, Message, MessageType
from src.session import get_session
from fastapi import Depends


class CommunityRepository:
    def get(self, session: Annotated[Session, Depends(get_session)]) -> List[Community]:
        statement = select(Community)
        return session.exec(statement).all()

    def get_by_id(
        self, session: Annotated[Session, Depends(get_session)], community_id: int
    ) -> Optional[Community]:
        statement = select(Community).where(Community.id == community_id)
        return session.exec(statement).first()

    def get_by_name(
        self, session: Annotated[Session, Depends(get_session)], name: str
    ) -> Optional[Community]:
        """Get community by name (useful for API endpoints using string identifiers)"""
        statement = select(Community).where(Community.name == name)
        return session.exec(statement).first()

    def search_by_name(
        self, session: Annotated[Session, Depends(get_session)], name: str
    ) -> List[Community]:
        """Search communities by name (partial match)"""
        statement = select(Community).where(Community.name.contains(name))
        return session.exec(statement).all()

    def create(
        self, session: Annotated[Session, Depends(get_session)], community: Community
    ) -> Community:
        session.add(community)
        session.commit()
        session.refresh(community)
        return community

    def update(
        self,
        session: Annotated[Session, Depends(get_session)],
        community_id: int,
        **kwargs,
    ) -> Optional[Community]:
        community = self.get_by_id(session, community_id)
        if community:
            for key, value in kwargs.items():
                if hasattr(community, key):
                    setattr(community, key, value)
            session.add(community)
            session.commit()
            session.refresh(community)
        return community

    def delete(
        self, session: Annotated[Session, Depends(get_session)], community_id: int
    ) -> bool:
        community = self.get_by_id(session, community_id)
        if community:
            session.delete(community)
            session.commit()
            return True
        return False

    def add_pet_policy(
        self,
        session: Annotated[Session, Depends(get_session)],
        community_id: int,
        pet_type: PetType,
        extra_pet_fee: float = 0.0,
    ) -> Optional[PetPolicy]:
        """Add a pet policy to an existing community"""
        community = self.get_by_id(session, community_id)
        if not community:
            return None

        pet_policy = PetPolicy(
            community_id=community_id, pet_type=pet_type, extra_pet_fee=extra_pet_fee
        )
        session.add(pet_policy)
        session.commit()
        session.refresh(pet_policy)
        return pet_policy

    def get_pet_policies(
        self, session: Annotated[Session, Depends(get_session)], community_id: int
    ) -> List[PetPolicy]:
        """Get all pet policies for a community"""
        statement = select(PetPolicy).where(PetPolicy.community_id == community_id)
        return session.exec(statement).all()

    def create_with_pet_policies(
        self,
        session: Annotated[Session, Depends(get_session)],
        community_data: dict,
        pet_policies_data: List[dict] = None,
    ) -> Community:
        """
        Create a community with associated pet policies

        Args:
            community_data: Dictionary containing community fields
            pet_policies_data: List of dictionaries containing pet policy data
                              Each dict should have 'pet_type' and 'extra_pet_fee'
        """
        community_obj = Community(**community_data)
        session.add(community_obj)
        session.flush()

        if pet_policies_data:
            for policy_data in pet_policies_data:
                pet_policy = PetPolicy(
                    community_id=community_obj.id,
                    pet_type=policy_data.get("pet_type"),
                    extra_pet_fee=policy_data.get("extra_pet_fee", 0.0),
                )
                session.add(pet_policy)

        session.commit()
        session.refresh(community_obj)
        return community_obj


class PropertyRepository:
    def get(self, session: Annotated[Session, Depends(get_session)]) -> List[Property]:
        statement = select(Property)
        return session.exec(statement).all()

    def get_by_id(
        self, session: Annotated[Session, Depends(get_session)], property_id: int
    ) -> Optional[Property]:
        statement = select(Property).where(Property.id == property_id)
        return session.exec(statement).first()

    def get_by_community(
        self, session: Annotated[Session, Depends(get_session)], community_id: int
    ) -> List[Property]:
        statement = select(Property).where(Property.community_id == community_id)
        return session.exec(statement).all()

    def get_available_by_date(
        self, session: Annotated[Session, Depends(get_session)], available_date: str
    ) -> List[Property]:
        """Get properties available on or before a specific date"""
        statement = select(Property).where(
            (Property.available_date <= available_date)
            | (Property.available_date.is_(None))
        )
        return session.exec(statement).all()

    def get_available_properties(
        self, session: Annotated[Session, Depends(get_session)]
    ) -> List[Property]:
        """Get all properties that have an available date set"""
        statement = select(Property).where(Property.available_date.is_not(None))
        return session.exec(statement).all()

    def create(
        self, session: Annotated[Session, Depends(get_session)], property_obj: Property
    ) -> Property:
        """Create a property"""
        session.add(property_obj)
        session.commit()
        session.refresh(property_obj)
        return property_obj

    def update(
        self,
        session: Annotated[Session, Depends(get_session)],
        property_id: int,
        **kwargs,
    ) -> Optional[Property]:
        property_obj = self.get_by_id(session, property_id)
        if property_obj:
            for key, value in kwargs.items():
                if hasattr(property_obj, key):
                    setattr(property_obj, key, value)
            session.add(property_obj)
            session.commit()
            session.refresh(property_obj)
        return property_obj

    def delete(
        self, session: Annotated[Session, Depends(get_session)], property_id: int
    ) -> bool:
        property_obj = self.get_by_id(session, property_id)
        if property_obj:
            session.delete(property_obj)
            session.commit()
            return True
        return False


class MessageRepository:
    def create(
        self, session: Annotated[Session, Depends(get_session)], message: Message
    ) -> Message:
        """Create a message"""
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def create_human_message(
        self, session: Annotated[Session, Depends(get_session)], content: str
    ) -> Message:
        """Create a human message"""
        return self.create_message(session, content, MessageType.HUMAN)

    def create_ai_message(
        self, session: Annotated[Session, Depends(get_session)], content: str
    ) -> Message:
        """Create an AI message"""
        return self.create_message(session, content, MessageType.AI)

    def create_message(
        self,
        session: Annotated[Session, Depends(get_session)],
        content: str,
        message_type: MessageType,
    ) -> Message:
        """Create a message with content and type"""
        message = Message(content=content, type=message_type)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_message_history(
        self, session: Annotated[Session, Depends(get_session)], limit: int = 20
    ) -> List[Message]:
        """Get recent message history ordered by timestamp"""
        statement = select(Message).order_by(Message.timestamp.desc()).limit(limit)
        return session.exec(statement).all()
