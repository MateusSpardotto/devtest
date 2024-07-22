from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

from elevators.api.elevator_api import create_demand
from elevators.models.demand_model import DemandModel


class TestElevatorApi(unittest.TestCase):

    @patch('elevators.infra.infra_database.SessionLocal')
    def test_create_demand_with_success(self, MockSessionLocal):
        # Mock the database session
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        
        # Mock the add, commit, and refresh methods
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        
        date = datetime.now
        # Create a sample demand data
        demand_data = {
            "DemandRequest": date,
            "DemandedFloor": "5",
            "RequisitedFloor": "3",
            "RestingFloor": "1"
        }
        
        # Convert to DemandModel
        demand_model = DemandModel(**demand_data)
        
        # Mock the response from the database
        mock_demand = MagicMock()
        mock_demand.dict.return_value = demand_data
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = mock_demand
        
        # Perform the API call
        response = create_demand(demand_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), demand_data)
        
        # Assert the database operations were called correctly
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        
        