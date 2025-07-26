from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.models import Community
from src.repository import CommunityRepository, PropertyRepository
from src.seralizers import AgentResponse, HumanMessageRequest
from src.session import get_session
from src.services import process_human_message

router = APIRouter(prefix="/api")


@router.get("/communities", status_code=200)
def fetch_communities(
    community_id: Optional[int] = None,
    session: Session = Depends(get_session),
) -> List[Community] | Community:
    """
    Retrieve all communities or a specific community by ID
    """
    repository = CommunityRepository()

    if community_id:
        # Get specific community by ID
        community = repository.get_by_id(session, community_id)
        if not community:
            raise HTTPException(status_code=404, detail="Community not found")
        return community
    else:
        # Get all communities
        return repository.get(session)


@router.get("/communities/{community_id}", status_code=200)
def fetch_community_by_id(
    community_id: int,
    session: Session = Depends(get_session),
) -> Community:
    """
    Retrieve a specific community by ID
    """
    repository = CommunityRepository()
    community = repository.get_by_id(session, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


@router.get("/communities/name/{community_name}", status_code=200)
def fetch_community_by_name(
    community_name: str,
    session: Session = Depends(get_session),
) -> Community:
    """
    Retrieve a specific community by name (e.g., 'sunset-ridge')
    """
    repository = CommunityRepository()
    community = repository.get_by_name(session, community_name)
    if not community:
        raise HTTPException(
            status_code=404, detail=f"Community '{community_name}' not found"
        )
    return community


@router.get("/communities/{community_id}/pet-policies", status_code=200)
def fetch_community_pet_policies(
    community_id: int,
    session: Session = Depends(get_session),
):
    """
    Retrieve all pet policies for a specific community
    """
    community_repo = CommunityRepository()

    # Check if community exists
    community = community_repo.get_by_id(session, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    pet_policies = community_repo.get_pet_policies(session, community_id)

    return [
        {
            "id": policy.id,
            "pet_type": policy.pet_type.value,
            "extra_pet_fee": policy.extra_pet_fee,
        }
        for policy in pet_policies
    ]


@router.get("/properties/{community_id}", status_code=200)
def fetch_properties(
    community_id: int,
    session: Session = Depends(get_session),
):
    """
    Retrieve all properties in a specific community by ID
    """
    property_repo = PropertyRepository()
    community_repo = CommunityRepository()

    # Check if community exists
    community = community_repo.get_by_id(session, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    properties = property_repo.get_by_community(session, community_id)

    if not properties:
        raise HTTPException(
            status_code=404, detail=f"No properties found for community {community_id}"
        )

    # Get community pet policies
    pet_policies = community_repo.get_pet_policies(session, community_id)

    result = []
    for property in properties:
        property_dict = {
            "id": property.id,
            "description": property.description,
            "bedrooms": property.bedrooms,
            "bathrooms": property.bathrooms,
            "garage": property.garage,
            "available_date": property.available_date,
            "base_rent": property.base_rent,
            "special_offer": property.special_offer,
            "community_id": property.community_id,
            "community_name": community.name,
            "community_pet_policies": [
                {
                    "id": policy.id,
                    "pet_type": policy.pet_type.value,
                    "extra_pet_fee": policy.extra_pet_fee,
                }
                for policy in pet_policies
            ],
        }
        result.append(property_dict)

    return result


@router.get("/properties/community/{community_name}", status_code=200)
def fetch_properties_by_community_name(
    community_name: str,
    session: Session = Depends(get_session),
):
    """
    Retrieve all properties in a specific community by name (e.g., 'sunset-ridge')
    """
    property_repo = PropertyRepository()
    community_repo = CommunityRepository()

    # Check if community exists by name
    community = community_repo.get_by_name(session, community_name)
    if not community:
        raise HTTPException(
            status_code=404, detail=f"Community '{community_name}' not found"
        )

    properties = property_repo.get_by_community(session, community.id)

    if not properties:
        raise HTTPException(
            status_code=404,
            detail=f"No properties found for community '{community_name}'",
        )

    # Get community pet policies
    pet_policies = community_repo.get_pet_policies(session, community.id)

    result = []
    for property in properties:
        property_dict = {
            "id": property.id,
            "description": property.description,
            "bedrooms": property.bedrooms,
            "bathrooms": property.bathrooms,
            "garage": property.garage,
            "available_date": property.available_date,
            "base_rent": property.base_rent,
            "special_offer": property.special_offer,
            "community_id": property.community_id,
            "community_name": community.name,
            "community_pet_policies": [
                {
                    "id": policy.id,
                    "pet_type": policy.pet_type.value,
                    "extra_pet_fee": policy.extra_pet_fee,
                }
                for policy in pet_policies
            ],
        }
        result.append(property_dict)

    return result


@router.get("/pricing/{community_id}/{unit_id}", status_code=200)
def get_property_pricing(
    community_id: int,
    unit_id: int,
    move_in_date: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """
    Get pricing information for a specific property
    """
    property_repo = PropertyRepository()
    property_obj = property_repo.get_by_id(session, unit_id)

    if not property_obj:
        raise HTTPException(status_code=404, detail=f"Property {unit_id} not found")

    if property_obj.community_id != community_id:
        raise HTTPException(
            status_code=400,
            detail=f"Property {unit_id} does not belong to community {community_id}",
        )

    # Get community pet policies to determine if pet-friendly
    community_repo = CommunityRepository()
    pet_policies = community_repo.get_pet_policies(session, community_id)
    pet_friendly = len(pet_policies) > 0

    return {
        "rent": property_obj.base_rent,
        "special": property_obj.special_offer or "No special offers available",
        "unit_description": f"{property_obj.bedrooms} bed {property_obj.bathrooms} bath",
        "garage_included": property_obj.garage,
        "pet_friendly": pet_friendly,
        "move_in_date": move_in_date,
        "unit_id": unit_id,
        "community_id": community_id,
    }


@router.post("/reply", status_code=200, response_model=AgentResponse)
def reply(request: HumanMessageRequest):
    """
    Process a human message through the agent and return the response
    
    This endpoint takes a lead inquiry with structured data and processes it through the AI agent
    which can use tools to check property availability, pet policies, and pricing.
    """
    try:
        request_data = {
            "lead": {
                "name": request.lead.name,
                "email": request.lead.email
            },
            "message": request.message,
            "preferences": {
                "bedrooms": request.preferences.bedrooms,
                "move_in": request.preferences.move_in
            },
            "community_id": request.community_id
        }
        
        result = process_human_message(request_data)
        return AgentResponse(**result)
    except Exception as e:
        return AgentResponse(
            reply="I'm sorry, I encountered an error while processing your request. Please try again.",
            action="",
            proposed_time=""
        )
