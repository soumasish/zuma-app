#!/usr/bin/env python3

import logging
from typing import List
from src.models import PetType
from src.repository import CommunityRepository, PropertyRepository
from src.session import get_session
from sqlalchemy import text
from main import init_logger
from sqlmodel import SQLModel
from src.session import engine
from src.models import Property

logger = logging.getLogger(__name__)

"""
Database seeding script for Zuma App
Creates sample communities and properties with pet policies at community level
"""


def create_sample_communities() -> List[dict]:
    """Create sample community data"""
    return [
        {
            "name": "sunset-ridge",
            "description": "Sunset Gardens - A peaceful community with beautiful gardens and walking trails",
        },
        {
            "name": "riverside-heights",
            "description": "Riverside Heights - Modern apartments with river views and luxury amenities",
        },
        {
            "name": "oakwood-village",
            "description": "Oakwood Village - Family-friendly neighborhood with parks and schools nearby",
        },
        {
            "name": "downtown-lofts",
            "description": "Downtown Lofts - Urban living in the heart of the city with easy access to everything",
        },
        {
            "name": "mountain-view-estates",
            "description": "Mountain View Estates - Premium properties with stunning mountain vistas",
        },
    ]


def create_sample_community_pet_policies() -> List[dict]:
    """Create sample pet policies for communities"""
    return [
        # Pet policies for Sunset Gardens (community_id: 1)
        {
            "community_id": 1,
            "pet_policies": [
                {"pet_type": PetType.CAT, "extra_pet_fee": 25.0},
                {"pet_type": PetType.DOG, "extra_pet_fee": 50.0},
            ],
        },
        # Pet policies for Riverside Heights (community_id: 2)
        {
            "community_id": 2,
            "pet_policies": [
                {"pet_type": PetType.CAT, "extra_pet_fee": 35.0},
                {"pet_type": PetType.DOG, "extra_pet_fee": 75.0},
            ],
        },
        # Pet policies for Oakwood Village (community_id: 3)
        {
            "community_id": 3,
            "pet_policies": [
                {"pet_type": PetType.CAT, "extra_pet_fee": 20.0},
                {"pet_type": PetType.DOG, "extra_pet_fee": 45.0},
            ],
        },
        # Pet policies for Downtown Lofts (community_id: 4)
        {
            "community_id": 4,
            "pet_policies": [
                {"pet_type": PetType.CAT, "extra_pet_fee": 30.0},
                {"pet_type": PetType.DOG, "extra_pet_fee": 60.0},
            ],
        },
        # Pet policies for Mountain View Estates (community_id: 5)
        {
            "community_id": 5,
            "pet_policies": [
                {"pet_type": PetType.CAT, "extra_pet_fee": 50.0},
                {"pet_type": PetType.DOG, "extra_pet_fee": 100.0},
            ],
        },
    ]


def create_sample_properties() -> List[dict]:
    """Create sample property data with pricing"""
    return [
        # Properties for Sunset Gardens (community_id: 1)
        {
            "description": "Cozy 2-bedroom apartment with garden view",
            "bedrooms": 2.0,
            "bathrooms": 1.5,
            "garage": False,
            "available_date": "2024-01-15",
            "base_rent": 1800.0,
            "special_offer": "1st month free",
            "community_id": 1,
        },
        {
            "description": "Spacious 3-bedroom townhouse with private patio",
            "bedrooms": 3.0,
            "bathrooms": 2.5,
            "garage": True,
            "available_date": "2024-02-01",
            "base_rent": 2400.0,
            "special_offer": "No deposit required",
            "community_id": 1,
        },
        # Properties for Riverside Heights (community_id: 2)
        {
            "description": "Luxury 1-bedroom apartment with riverfront balcony",
            "bedrooms": 1.0,
            "bathrooms": 1.0,
            "garage": True,
            "available_date": "2024-01-20",
            "base_rent": 2200.0,
            "special_offer": "2 months free",
            "community_id": 2,
        },
        {
            "description": "Premium 2-bedroom penthouse with panoramic views",
            "bedrooms": 2.0,
            "bathrooms": 2.0,
            "garage": True,
            "available_date": None,  # Not available yet
            "base_rent": 3500.0,
            "special_offer": "Concierge service included",
            "community_id": 2,
        },
        # Properties for Oakwood Village (community_id: 3)
        {
            "description": "Family 4-bedroom house with large backyard",
            "bedrooms": 4.0,
            "bathrooms": 3.0,
            "garage": True,
            "available_date": "2024-03-01",
            "base_rent": 3200.0,
            "special_offer": "Utilities included",
            "community_id": 3,
        },
        {
            "description": "Charming 3-bedroom cottage near the park",
            "bedrooms": 3.0,
            "bathrooms": 2.0,
            "garage": False,
            "available_date": "2024-01-10",
            "base_rent": 2100.0,
            "special_offer": "Pet-friendly community",
            "community_id": 3,
        },
        # Properties for Downtown Lofts (community_id: 4)
        {
            "description": "Modern studio loft in the arts district",
            "bedrooms": 0.0,
            "bathrooms": 1.0,
            "garage": False,
            "available_date": "2024-01-25",
            "base_rent": 1600.0,
            "special_offer": "Artist discount available",
            "community_id": 4,
        },
        {
            "description": "Industrial 2-bedroom loft with exposed brick",
            "bedrooms": 2.0,
            "bathrooms": 1.5,
            "garage": True,
            "available_date": "2024-02-15",
            "base_rent": 2800.0,
            "special_offer": "Free parking included",
            "community_id": 4,
        },
        # Properties for Mountain View Estates (community_id: 5)
        {
            "description": "Luxury 5-bedroom estate with mountain views",
            "bedrooms": 5.0,
            "bathrooms": 4.5,
            "garage": True,
            "available_date": "2024-04-01",
            "base_rent": 5500.0,
            "special_offer": "Private chef service available",
            "community_id": 5,
        },
        {
            "description": "Elegant 3-bedroom villa with private pool",
            "bedrooms": 3.0,
            "bathrooms": 3.0,
            "garage": True,
            "available_date": None,  # Not available yet
            "base_rent": 4200.0,
            "special_offer": "Pool maintenance included",
            "community_id": 5,
        },
    ]


def seed_database():
    """Seed the database with sample data"""
    logger.info("Starting database seeding")

    logger.info("Creating database tables")
    SQLModel.metadata.create_all(engine)

    # Get database session
    session = next(get_session())

    try:
        # Create repositories
        community_repo = CommunityRepository()
        property_repo = PropertyRepository()

        # Clear existing data (optional - comment out if you want to preserve existing data)
        logger.info("Clearing existing data")
        session.exec(text("DELETE FROM petpolicy"))
        session.exec(text("DELETE FROM property"))
        session.exec(text("DELETE FROM community"))
        session.commit()

        # Seed communities with pet policies
        logger.info("Creating communities with pet policies")
        communities_data = create_sample_communities()
        community_pet_policies = create_sample_community_pet_policies()
        created_communities = []

        for i, community_data in enumerate(communities_data, 1):
            # Get pet policies for this community
            pet_policies_data = next(
                (
                    cp["pet_policies"]
                    for cp in community_pet_policies
                    if cp["community_id"] == i
                ),
                [],
            )

            # Create community with pet policies
            created_community = community_repo.create_with_pet_policies(
                session, community_data, pet_policies_data
            )
            created_communities.append(created_community)

            logger.info(
                "Created community",
                extra={
                    "community_id": created_community.id,
                    "community_name": created_community.name,
                    "description": created_community.description,
                    "pet_policies_count": len(pet_policies_data),
                },
            )

            # Log pet policy details
            for policy_data in pet_policies_data:
                logger.debug(
                    "Pet policy created",
                    extra={
                        "community_id": created_community.id,
                        "pet_type": policy_data["pet_type"].value,
                        "extra_fee": policy_data["extra_pet_fee"],
                    },
                )

        # Seed properties
        logger.info("Creating properties")
        properties_data = create_sample_properties()

        for property_data in properties_data:
            # Create property (no pet policies - they're at community level now)
            created_property = property_repo.create(session, Property(**property_data))

            logger.info(
                "Created property",
                extra={
                    "property_id": created_property.id,
                    "description": created_property.description,
                    "bedrooms": created_property.bedrooms,
                    "bathrooms": created_property.bathrooms,
                    "available_date": created_property.available_date,
                    "base_rent": created_property.base_rent,
                    "special_offer": created_property.special_offer,
                    "community_id": created_property.community_id,
                },
            )

        logger.info(
            "Database seeding completed successfully",
            extra={
                "communities_created": len(created_communities),
                "properties_created": len(properties_data),
            },
        )

        # Log summary
        for i, community in enumerate(created_communities, 1):
            properties_in_community = [
                p for p in properties_data if p.get("community_id") == i
            ]
            pet_policies_count = len(
                next(
                    (
                        cp["pet_policies"]
                        for cp in community_pet_policies
                        if cp["community_id"] == i
                    ),
                    [],
                )
            )
            logger.info(
                "Community summary",
                extra={
                    "community_id": community.id,
                    "community_name": community.name,
                    "description": community.description,
                    "properties_count": len(properties_in_community),
                    "pet_policies_count": pet_policies_count,
                },
            )

    except Exception as e:
        logger.error("Error during seeding", extra={"error": str(e)})
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_logger(log_level="INFO", enable_json=True)
    seed_database()
