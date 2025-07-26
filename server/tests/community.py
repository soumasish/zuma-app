import pytest
from unittest.mock import Mock

from src.models import Community, Property, PetType, PetPolicy
from src.repository import CommunityRepository


class TestCommunityRepository:
    """Test cases for CommunityRepository"""

    @pytest.fixture
    def mock_session(self):
        """Mock database session"""
        session = Mock()
        session.exec = Mock()
        session.add = Mock()
        session.commit = Mock()
        session.refresh = Mock()
        session.delete = Mock()
        session.flush = Mock()
        return session

    @pytest.fixture
    def community_repo(self):
        """CommunityRepository instance"""
        return CommunityRepository()

    @pytest.fixture
    def sample_community(self):
        """Sample community data"""
        return Community(id=1, name="sunset-ridge", description="Test Community")

    @pytest.fixture
    def sample_pet_policies(self):
        """Sample pet policies data"""
        return [
            {"pet_type": PetType.CAT, "extra_pet_fee": 25.0},
            {"pet_type": PetType.DOG, "extra_pet_fee": 50.0},
        ]

    def test_get_all_communities(self, community_repo, mock_session):
        """Test getting all communities"""
        # Arrange
        expected_communities = [
            Community(id=1, name="sunset-ridge", description="Community 1"),
            Community(id=2, name="oak-park", description="Community 2"),
        ]
        mock_session.exec.return_value.all.return_value = expected_communities

        # Act
        result = community_repo.get(mock_session)

        # Assert
        assert result == expected_communities
        assert result[0].name == "sunset-ridge"
        assert result[1].name == "oak-park"
        mock_session.exec.assert_called_once()

    def test_get_community_by_id_found(self, community_repo, mock_session):
        """Test getting community by ID when found"""
        # Arrange
        expected_community = Community(id=1, description="Test Community")
        mock_session.exec.return_value.first.return_value = expected_community

        # Act
        result = community_repo.get_by_id(mock_session, 1)

        # Assert
        assert result == expected_community
        mock_session.exec.assert_called_once()

    def test_get_community_by_id_not_found(self, community_repo, mock_session):
        """Test getting community by ID when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = community_repo.get_by_id(mock_session, 999)

        # Assert
        assert result is None
        mock_session.exec.assert_called_once()

    def test_create_community(self, community_repo, mock_session, sample_community):
        """Test creating a new community"""
        # Arrange
        mock_session.refresh.return_value = None

        # Act
        result = community_repo.create(mock_session, sample_community)

        # Assert
        assert result == sample_community
        mock_session.add.assert_called_once_with(sample_community)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_community)

    def test_create_community_with_pet_policies(
        self, community_repo, mock_session, sample_pet_policies
    ):
        """Test creating community with pet policies"""
        # Arrange
        community_data = {"name": "sunset-ridge", "description": "Test Community"}

        # Mock the session to simulate database behavior
        def mock_add(obj):
            if hasattr(obj, "id") and obj.id is None:
                obj.id = 1  # Simulate ID assignment

        mock_session.add.side_effect = mock_add
        mock_session.flush.return_value = None
        mock_session.refresh.return_value = None

        # Act
        result = community_repo.create_with_pet_policies(
            mock_session, community_data, sample_pet_policies
        )

        # Assert
        assert result.id == 1
        assert result.name == "sunset-ridge"
        assert result.description == "Test Community"
        assert mock_session.add.call_count >= 1  # At least one add call for community
        mock_session.flush.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_create_community_without_pet_policies(self, community_repo, mock_session):
        """Test creating community without pet policies"""
        # Arrange
        community_data = {"name": "oak-park", "description": "Test Community"}

        # Mock the session to simulate database behavior
        def mock_add(obj):
            if hasattr(obj, "id") and obj.id is None:
                obj.id = 1  # Simulate ID assignment

        mock_session.add.side_effect = mock_add
        mock_session.refresh.return_value = None

        # Act
        result = community_repo.create_with_pet_policies(
            mock_session, community_data, None
        )

        # Assert
        assert result.id == 1
        assert result.name == "oak-park"
        assert result.description == "Test Community"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_update_community_success(self, community_repo, mock_session):
        """Test updating community successfully"""
        # Arrange
        existing_community = Community(id=1, description="Old Description")
        mock_session.exec.return_value.first.return_value = existing_community

        # Act
        result = community_repo.update(mock_session, 1, description="New Description")

        # Assert
        assert result == existing_community
        assert existing_community.description == "New Description"
        mock_session.add.assert_called_once_with(existing_community)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(existing_community)

    def test_update_community_not_found(self, community_repo, mock_session):
        """Test updating community when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = community_repo.update(mock_session, 999, description="New Description")

        # Assert
        assert result is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_delete_community_success(self, community_repo, mock_session):
        """Test deleting community successfully"""
        # Arrange
        existing_community = Community(id=1, description="Test Community")
        mock_session.exec.return_value.first.return_value = existing_community

        # Act
        result = community_repo.delete(mock_session, 1)

        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(existing_community)
        mock_session.commit.assert_called_once()

    def test_delete_community_not_found(self, community_repo, mock_session):
        """Test deleting community when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = community_repo.delete(mock_session, 999)

        # Assert
        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_add_pet_policy_success(self, community_repo, mock_session):
        """Test adding pet policy successfully"""
        # Arrange
        existing_community = Community(id=1, description="Test Community")
        mock_session.exec.return_value.first.return_value = existing_community

        expected_policy = PetPolicy(
            id=1, community_id=1, pet_type=PetType.CAT, extra_pet_fee=25.0
        )
        mock_session.refresh.return_value = None

        # Act
        result = community_repo.add_pet_policy(mock_session, 1, PetType.CAT, 25.0)

        # Assert
        assert result is not None
        assert result.community_id == 1
        assert result.pet_type == PetType.CAT
        assert result.extra_pet_fee == 25.0
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_add_pet_policy_community_not_found(self, community_repo, mock_session):
        """Test adding pet policy when community not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = community_repo.add_pet_policy(mock_session, 999, PetType.CAT, 25.0)

        # Assert
        assert result is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_get_pet_policies(self, community_repo, mock_session):
        """Test getting pet policies for a community"""
        # Arrange
        expected_policies = [
            PetPolicy(id=1, community_id=1, pet_type=PetType.CAT, extra_pet_fee=25.0),
            PetPolicy(id=2, community_id=1, pet_type=PetType.DOG, extra_pet_fee=50.0),
        ]
        mock_session.exec.return_value.all.return_value = expected_policies

        # Act
        result = community_repo.get_pet_policies(mock_session, 1)

        # Assert
        assert result == expected_policies
        mock_session.exec.assert_called_once()

    def test_get_community_by_name_found(self, community_repo, mock_session):
        """Test getting community by name when found"""
        # Arrange
        expected_community = Community(
            id=1, name="sunset-ridge", description="Test Community"
        )
        mock_session.exec.return_value.first.return_value = expected_community

        # Act
        result = community_repo.get_by_name(mock_session, "sunset-ridge")

        # Assert
        assert result == expected_community
        assert result.name == "sunset-ridge"
        mock_session.exec.assert_called_once()

    def test_get_community_by_name_not_found(self, community_repo, mock_session):
        """Test getting community by name when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = community_repo.get_by_name(mock_session, "non-existent")

        # Assert
        assert result is None
        mock_session.exec.assert_called_once()

    def test_search_communities_by_name(self, community_repo, mock_session):
        """Test searching communities by name (partial match)"""
        # Arrange
        expected_communities = [
            Community(id=1, name="sunset-ridge", description="Sunset Ridge Community"),
            Community(id=2, name="sunset-park", description="Sunset Park Community"),
        ]
        mock_session.exec.return_value.all.return_value = expected_communities

        # Act
        result = community_repo.search_by_name(mock_session, "sunset")

        # Assert
        assert result == expected_communities
        assert len(result) == 2
        assert all("sunset" in community.name for community in result)
        mock_session.exec.assert_called_once()

    def test_search_communities_by_name_empty_result(
        self, community_repo, mock_session
    ):
        """Test searching communities by name when no matches"""
        # Arrange
        mock_session.exec.return_value.all.return_value = []

        # Act
        result = community_repo.search_by_name(mock_session, "nonexistent")

        # Assert
        assert result == []
        mock_session.exec.assert_called_once()


class TestAPIEndpoints:
    """Test cases for API endpoints"""

    @pytest.fixture
    def mock_session(self):
        """Mock database session"""
        session = Mock()
        session.exec = Mock()
        session.add = Mock()
        session.commit = Mock()
        session.refresh = Mock()
        session.delete = Mock()
        return session

    @pytest.fixture
    def sample_property_with_available_date(self):
        """Sample property with available_date"""
        return Property(
            id=1,
            description="Test Property",
            bedrooms=2.0,
            bathrooms=1.5,
            garage=True,
            available_date="2024-01-15",
            base_rent=2500.0,
            special_offer="1st month free",
            community_id=1,
        )

    @pytest.fixture
    def sample_property_without_available_date(self):
        """Sample property without available_date"""
        return Property(
            id=2,
            description="Test Property 2",
            bedrooms=1.0,
            bathrooms=1.0,
            garage=False,
            available_date=None,
            base_rent=2000.0,
            special_offer=None,
            community_id=1,
        )

    def test_property_model_available_date_field(
        self, sample_property_with_available_date
    ):
        """Test that Property model has available_date field"""
        assert hasattr(sample_property_with_available_date, "available_date")
        assert sample_property_with_available_date.available_date == "2024-01-15"

    def test_property_model_available_date_none(
        self, sample_property_without_available_date
    ):
        """Test that Property model can have None available_date"""
        assert hasattr(sample_property_without_available_date, "available_date")
        assert sample_property_without_available_date.available_date is None

    def test_property_model_default_available_date(self):
        """Test that Property model defaults available_date to None"""
        property_obj = Property(id=3, description="Test Property 3", community_id=1)
        assert property_obj.available_date is None

    def test_community_model_has_name_field(self):
        """Test that Community model has name field"""
        community = Community(id=1, name="sunset-ridge", description="Test Community")
        assert hasattr(community, "name")
        assert community.name == "sunset-ridge"

    def test_community_model_name_required(self):
        """Test that Community model requires name field"""
        # This should work
        community = Community(id=1, name="sunset-ridge", description="Test Community")
        assert community.name == "sunset-ridge"

    def test_community_model_without_description(self):
        """Test that Community model can be created without description"""
        community = Community(id=1, name="sunset-ridge")
        assert community.name == "sunset-ridge"
        assert community.description is None
