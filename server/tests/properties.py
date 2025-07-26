import pytest
from unittest.mock import Mock

from src.models import Property
from src.repository import PropertyRepository


class TestPropertyRepository:
    """Test cases for PropertyRepository"""

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
    def property_repo(self):
        """PropertyRepository instance"""
        return PropertyRepository()

    @pytest.fixture
    def sample_property(self):
        """Sample property data"""
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

    def test_get_all_properties(self, property_repo, mock_session):
        """Test getting all properties"""
        # Arrange
        expected_properties = [
            Property(id=1, description="Property 1", community_id=1),
            Property(id=2, description="Property 2", community_id=1),
        ]
        mock_session.exec.return_value.all.return_value = expected_properties

        # Act
        result = property_repo.get(mock_session)

        # Assert
        assert result == expected_properties
        mock_session.exec.assert_called_once()

    def test_get_property_by_id_found(self, property_repo, mock_session):
        """Test getting property by ID when found"""
        # Arrange
        expected_property = Property(id=1, description="Test Property", community_id=1)
        mock_session.exec.return_value.first.return_value = expected_property

        # Act
        result = property_repo.get_by_id(mock_session, 1)

        # Assert
        assert result == expected_property
        mock_session.exec.assert_called_once()

    def test_get_property_by_id_not_found(self, property_repo, mock_session):
        """Test getting property by ID when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = property_repo.get_by_id(mock_session, 999)

        # Assert
        assert result is None
        mock_session.exec.assert_called_once()

    def test_get_properties_by_community(self, property_repo, mock_session):
        """Test getting properties by community ID"""
        # Arrange
        expected_properties = [
            Property(id=1, description="Property 1", community_id=1),
            Property(id=2, description="Property 2", community_id=1),
        ]
        mock_session.exec.return_value.all.return_value = expected_properties

        # Act
        result = property_repo.get_by_community(mock_session, 1)

        # Assert
        assert result == expected_properties
        mock_session.exec.assert_called_once()

    def test_create_property_simple(self, property_repo, mock_session, sample_property):
        """Test creating property"""
        # Arrange
        mock_session.refresh.return_value = None

        # Act
        result = property_repo.create(mock_session, sample_property)

        # Assert
        assert result == sample_property
        mock_session.add.assert_called_once_with(sample_property)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_property)

    def test_update_property_success(self, property_repo, mock_session):
        """Test updating property successfully"""
        # Arrange
        existing_property = Property(
            id=1, description="Old Description", community_id=1
        )
        mock_session.exec.return_value.first.return_value = existing_property

        # Act
        result = property_repo.update(mock_session, 1, description="New Description")

        # Assert
        assert result == existing_property
        assert existing_property.description == "New Description"
        mock_session.add.assert_called_once_with(existing_property)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(existing_property)

    def test_update_property_not_found(self, property_repo, mock_session):
        """Test updating property when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = property_repo.update(mock_session, 999, description="New Description")

        # Assert
        assert result is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_delete_property_success(self, property_repo, mock_session):
        """Test deleting property successfully"""
        # Arrange
        existing_property = Property(id=1, description="Test Property", community_id=1)
        mock_session.exec.return_value.first.return_value = existing_property

        # Act
        result = property_repo.delete(mock_session, 1)

        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(existing_property)
        mock_session.commit.assert_called_once()

    def test_delete_property_not_found(self, property_repo, mock_session):
        """Test deleting property when not found"""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = property_repo.delete(mock_session, 999)

        # Assert
        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_get_available_by_date(self, property_repo, mock_session):
        """Test getting properties available by date"""
        # Arrange
        expected_properties = [
            Property(
                id=1,
                description="Property 1",
                available_date="2024-01-01",
                community_id=1,
            ),
            Property(
                id=2,
                description="Property 2",
                available_date="2024-01-15",
                community_id=1,
            ),
            Property(
                id=3, description="Property 3", available_date=None, community_id=1
            ),
        ]
        mock_session.exec.return_value.all.return_value = expected_properties

        # Act
        result = property_repo.get_available_by_date(mock_session, "2024-01-20")

        # Assert
        assert result == expected_properties
        mock_session.exec.assert_called_once()

    def test_get_available_properties(self, property_repo, mock_session):
        """Test getting all properties with available dates"""
        # Arrange
        expected_properties = [
            Property(
                id=1,
                description="Property 1",
                available_date="2024-01-01",
                community_id=1,
            ),
            Property(
                id=2,
                description="Property 2",
                available_date="2024-01-15",
                community_id=1,
            ),
        ]
        mock_session.exec.return_value.all.return_value = expected_properties

        # Act
        result = property_repo.get_available_properties(mock_session)

        # Assert
        assert result == expected_properties
        mock_session.exec.assert_called_once()

    def test_get_available_by_date_empty_result(self, property_repo, mock_session):
        """Test getting properties available by date when no matches"""
        # Arrange
        mock_session.exec.return_value.all.return_value = []

        # Act
        result = property_repo.get_available_by_date(mock_session, "2023-12-01")

        # Assert
        assert result == []
        mock_session.exec.assert_called_once()

    def test_get_available_properties_empty_result(self, property_repo, mock_session):
        """Test getting available properties when none have dates set"""
        # Arrange
        mock_session.exec.return_value.all.return_value = []

        # Act
        result = property_repo.get_available_properties(mock_session)

        # Assert
        assert result == []
        mock_session.exec.assert_called_once()
