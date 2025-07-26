import pytest
import json
from unittest.mock import Mock, patch

from src.models import Community, Property


class TestTools:
    """Test cases for tools"""

    @pytest.fixture
    def mock_session(self):
        """Mock database session"""
        session = Mock()
        session.exec = Mock()
        session.add = Mock()
        session.commit = Mock()
        session.refresh = Mock()
        session.delete = Mock()
        session.close = Mock()
        # Make session a context manager
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)
        return session

    @pytest.fixture
    def sample_community(self):
        """Sample community data"""
        return Community(id=1, name="sunset-ridge", description="Test Community")

    @pytest.fixture
    def sample_properties(self):
        """Sample properties data"""
        return [
            Property(
                id=1,
                description="2-bedroom apartment",
                bedrooms=2.0,
                bathrooms=1.5,
                garage=False,
                available_date="2024-01-15",
                base_rent=1800.0,
                special_offer="1st month free",
                community_id=1,
            ),
            Property(
                id=2,
                description="3-bedroom townhouse",
                bedrooms=3.0,
                bathrooms=2.5,
                garage=True,
                available_date="2024-02-01",
                base_rent=2400.0,
                special_offer="No deposit required",
                community_id=1,
            ),
            Property(
                id=3,
                description="1-bedroom studio",
                bedrooms=1.0,
                bathrooms=1.0,
                garage=False,
                available_date=None,  # Not available
                base_rent=1600.0,
                special_offer=None,
                community_id=1,
            ),
        ]

    def test_check_availability_community_found_with_available_units(
        self, mock_session, sample_community, sample_properties
    ):
        """Test check_availability when community exists and has available units"""
        from src.tools import check_availability

        # Mock the session generator
        with patch("src.tools.get_session") as mock_get_session:
            mock_get_session.return_value = iter([mock_session])

            # Mock the repository calls directly
            with patch("src.tools.CommunityRepository") as mock_community_repo_class:
                with patch("src.tools.PropertyRepository") as mock_property_repo_class:
                    # Setup community repository mock
                    mock_community_repo = Mock()
                    mock_community_repo.get_by_name.return_value = sample_community
                    mock_community_repo_class.return_value = mock_community_repo

                    # Setup property repository mock
                    mock_property_repo = Mock()
                    mock_property_repo.get_by_community.return_value = sample_properties
                    mock_property_repo_class.return_value = mock_property_repo

                    # Act - call the underlying function directly
                    result = check_availability.func("sunset-ridge", 2.0)

                    # Assert
                    result_dict = json.loads(result)
                    assert result_dict["available"] is True
                    assert result_dict["unit_id"] == "1"
                    assert result_dict["description"] == "2.0 bed 1.5 bath"
                    assert result_dict["garage"] is False
                    assert result_dict["available_date"] == "2024-01-15"
                    assert result_dict["community_name"] == "sunset-ridge"

                    # Verify repository methods were called
                    mock_community_repo.get_by_name.assert_called_once_with(
                        mock_session, "sunset-ridge"
                    )
                    mock_property_repo.get_by_community.assert_called_once_with(
                        mock_session, 1
                    )

    def test_check_availability_community_not_found(self, mock_session):
        """Test check_availability when community doesn't exist"""
        from src.tools import check_availability

        # Mock the session generator
        with patch("src.tools.get_session") as mock_get_session:
            mock_get_session.return_value = iter([mock_session])

            # Mock the repository calls directly
            with patch("src.tools.CommunityRepository") as mock_community_repo_class:
                # Setup community repository mock - not found
                mock_community_repo = Mock()
                mock_community_repo.get_by_name.return_value = None
                mock_community_repo_class.return_value = mock_community_repo

                # Act - call the underlying function directly
                result = check_availability.func("non-existent", 2.0)

                # Assert
                result_dict = json.loads(result)
                assert result_dict["available"] is False
                assert "Community 'non-existent' does not exist" in result_dict["error"]

                # Verify repository method was called
                mock_community_repo.get_by_name.assert_called_once_with(
                    mock_session, "non-existent"
                )

    def test_check_availability_no_units_available(
        self, mock_session, sample_community, sample_properties
    ):
        """Test check_availability when no units match the criteria"""
        from src.tools import check_availability

        # Mock the session generator
        with patch("src.tools.get_session") as mock_get_session:
            mock_get_session.return_value = iter([mock_session])

            # Mock the repository calls directly
            with patch("src.tools.CommunityRepository") as mock_community_repo_class:
                with patch("src.tools.PropertyRepository") as mock_property_repo_class:
                    # Setup community repository mock
                    mock_community_repo = Mock()
                    mock_community_repo.get_by_name.return_value = sample_community
                    mock_community_repo_class.return_value = mock_community_repo

                    # Setup property repository mock
                    mock_property_repo = Mock()
                    mock_property_repo.get_by_community.return_value = sample_properties
                    mock_property_repo_class.return_value = mock_property_repo

                    # Act - request 4 bedrooms (none available)
                    result = check_availability.func("sunset-ridge", 4.0)

                    # Assert
                    result_dict = json.loads(result)
                    assert result_dict["available"] is False
                    assert (
                        "No 4.0 bedroom units available in community 'sunset-ridge'"
                        in result_dict["message"]
                    )

                    # Verify repository methods were called
                    mock_community_repo.get_by_name.assert_called_once_with(
                        mock_session, "sunset-ridge"
                    )
                    mock_property_repo.get_by_community.assert_called_once_with(
                        mock_session, 1
                    )

    def test_check_availability_no_available_date_units(
        self, mock_session, sample_community
    ):
        """Test check_availability when units exist but have no available_date"""
        from src.tools import check_availability

        # Create properties with no available_date
        properties_no_date = [
            Property(
                id=1,
                description="2-bedroom apartment",
                bedrooms=2.0,
                bathrooms=1.5,
                garage=False,
                available_date=None,  # Not available
                base_rent=1800.0,
                special_offer="1st month free",
                community_id=1,
            )
        ]

        # Mock the session generator
        with patch("src.tools.get_session") as mock_get_session:
            mock_get_session.return_value = iter([mock_session])

            # Mock the repository calls directly
            with patch("src.tools.CommunityRepository") as mock_community_repo_class:
                with patch("src.tools.PropertyRepository") as mock_property_repo_class:
                    # Setup community repository mock
                    mock_community_repo = Mock()
                    mock_community_repo.get_by_name.return_value = sample_community
                    mock_community_repo_class.return_value = mock_community_repo

                    # Setup property repository mock
                    mock_property_repo = Mock()
                    mock_property_repo.get_by_community.return_value = (
                        properties_no_date
                    )
                    mock_property_repo_class.return_value = mock_property_repo

                    # Act - call the underlying function directly
                    result = check_availability.func("sunset-ridge", 2.0)

                    # Assert
                    result_dict = json.loads(result)
                    assert result_dict["available"] is False
                    assert (
                        "No 2.0 bedroom units available in community 'sunset-ridge'"
                        in result_dict["message"]
                    )

                    # Verify repository methods were called
                    mock_community_repo.get_by_name.assert_called_once_with(
                        mock_session, "sunset-ridge"
                    )
                    mock_property_repo.get_by_community.assert_called_once_with(
                        mock_session, 1
                    )

    def test_check_availability_exception_handling(self, mock_session):
        """Test check_availability handles exceptions gracefully"""
        from src.tools import check_availability

        # Mock the session generator to raise an exception
        with patch("src.tools.get_session") as mock_get_session:
            mock_get_session.side_effect = Exception("Database connection failed")

            # Act - call the underlying function directly
            result = check_availability.func("sunset-ridge", 2.0)

            # Assert
            result_dict = json.loads(result)
            assert "error" in result_dict
            assert "Database connection failed" in result_dict["error"]
