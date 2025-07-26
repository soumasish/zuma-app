from langchain_core.tools import tool
from src.repository import PropertyRepository, CommunityRepository
from src.session import get_session
from src.models import PetType
import json


@tool
def check_availability(community_name: str, bedrooms: float) -> str:
    """Check availability of units in a community with specified number of bedrooms"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Tool called with community_name={community_name}, bedrooms={bedrooms}")
    
    try:
        # Get database session using context manager
        session_gen = get_session()
        with next(session_gen) as session:
            # First check if the community exists by name
            community_repo = CommunityRepository()
            community = community_repo.get_by_name(session, community_name)

            if not community:
                return json.dumps(
                    {
                        "available": False,
                        "error": f"Community '{community_name}' does not exist",
                    }
                )

           
            repo = PropertyRepository()
            properties = repo.get_by_community(session, community.id)
            logger.info(f"Found {len(properties)} properties for community {community_name}")

            # Filter by bedrooms and availability (using available_date instead of available)
            available_units = [
                prop
                for prop in properties
                if prop.bedrooms == bedrooms and prop.available_date is not None
            ]
            logger.info(f"Found {len(available_units)} available units with {bedrooms} bedrooms")

            if not available_units:
                return json.dumps(
                    {
                        "available": False,
                        "message": f"No {bedrooms} bedroom units available in community '{community_name}'",
                    }
                )

            # Format the first available unit
            unit = available_units[0]
            result = {
                "available": True,
                "unit_id": str(unit.id),
                "description": f"{unit.bedrooms} bed {unit.bathrooms} bath",
                "garage": unit.garage,
                "available_date": unit.available_date,
                "community_name": community.name,
            }

            logger.info(f"Tool returning result: {result}")
            return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def check_pet_policy(community_id: int, pet_type: str) -> str:
    """Check pet policy for a specific pet type in a community"""
    try:
        # Get database session using context manager
        session_gen = get_session()
        with next(session_gen) as session:
            # First check if the community exists
            community_repo = CommunityRepository()
            community = community_repo.get_by_id(session, community_id)

            if not community:
                return json.dumps({"error": f"Community {community_id} does not exist"})

            # Get pet policies directly from the community
            pet_policies = community_repo.get_pet_policies(session, community_id)

            # Find policy for the specified pet type
            pet_type_enum = PetType(pet_type.lower())
            matching_policy = None

            for policy in pet_policies:
                if policy.pet_type == pet_type_enum:
                    matching_policy = policy
                    break

            if matching_policy:
                result = {
                    "allowed": True,
                    "fee": matching_policy.extra_pet_fee,
                    "notes": f"Pet fee: ${matching_policy.extra_pet_fee}",
                }
            else:
                result = {
                    "allowed": False,
                    "fee": 0.0,
                    "notes": f"{pet_type.title()}s not allowed in this community",
                }

            return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_pricing(community_id: int, unit_id: str, move_in_date: str) -> str:
    """Get pricing information for a specific unit"""
    try:
        session_gen = get_session()
        with next(session_gen) as session:
            # Use repository to get the specific property
            property_repo = PropertyRepository()
            property_obj = property_repo.get_by_id(session, int(unit_id))

            if not property_obj:
                return json.dumps({"error": f"Unit {unit_id} not found"})

            if property_obj.community_id != community_id:
                return json.dumps(
                    {
                        "error": f"Unit {unit_id} does not belong to community {community_id}"
                    }
                )

            community_repo = CommunityRepository()
            pet_policies = community_repo.get_pet_policies(session, community_id)
            pet_friendly = len(pet_policies) > 0

            result = {
                "rent": property_obj.base_rent,
                "special": property_obj.special_offer or "No special offers available",
                "unit_description": f"{property_obj.bedrooms} bed {property_obj.bathrooms} bath",
                "garage_included": property_obj.garage,
                "pet_friendly": pet_friendly,
                "move_in_date": move_in_date,
            }

            return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def propose_tour(lead_name: str, community_name: str, unit_description: str, available_date: str) -> str:
    """Propose a tour when you have enough information to suggest a specific time slot"""
    result = {
        "action": "propose_tour",
        "message": f"Hi {lead_name}! I'd love to show you the {unit_description} at {community_name}. It's available from {available_date}. Would you like to schedule a tour? I have openings this Saturday at 11 am or 2 pm.",
        "tour_slots": ["11:00 AM", "2:00 PM"],
        "unit_info": {
            "community": community_name,
            "description": unit_description,
            "available_date": available_date
        }
    }
    return json.dumps(result, indent=2)


@tool
def ask_clarification(lead_name: str, missing_info: str) -> str:
    """Ask for clarification when the lead's request is ambiguous or missing key details"""
    result = {
        "action": "ask_clarification",
        "message": f"Hi {lead_name}! I'd be happy to help you find the perfect place. To better assist you, could you please clarify: {missing_info}",
        "missing_info": missing_info
    }
    return json.dumps(result, indent=2)


@tool
def handoff_human(lead_name: str, reason: str) -> str:
    """Hand off to a human agent when the request cannot be fulfilled automatically"""
    result = {
        "action": "handoff_human",
        "message": f"Hi {lead_name}! I'd like to connect you with one of our leasing specialists who can better assist you with your request. {reason} They'll be in touch within the next hour.",
        "reason": reason,
        "escalation": True
    }
    return json.dumps(result, indent=2)
