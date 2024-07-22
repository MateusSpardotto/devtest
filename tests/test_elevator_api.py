from datetime import datetime
import json
import unittest
from unittest.mock import MagicMock, patch

from elevators.api.elevator_api import create_demand, get_demands, get_demands_ranged
from elevators.models.demand_model import DemandModel
from elevators.sql_documents.demand import Demand

class TestCreateDemand(unittest.TestCase):

    @patch("elevators.infra.infra_database.get_db")
    def test_create_demand_with_success(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])
        
        date = datetime.now() 
        demand = DemandModel(DemandRequest = date,
                                   DemandedFloor = "5",
                                   RequisitedFloor = "G",
                                   RestingFloor = "T")

        demand_data = {
            "DemandRequest": date.strftime("%m-%d-%Y %H:%M:%S"),
            "DemandedFloor": "5",
            "RequisitedFloor": "G",
            "RestingFloor": "T"
        }

        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = demand_data
        
        
        response = create_demand(demand)
        

        response_str = response.body.decode('utf-8')
        response_dict = json.loads(response_str)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get("DataInserted"), demand_data)

    @patch("elevators.infra.infra_database.get_db")
    def test_create_demand_with_exception(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        mock_db.add.side_effect = Exception("Database error")
        
        date = datetime.now() 
        demand = DemandModel(DemandRequest = date,
                                   DemandedFloor = "5",
                                   RequisitedFloor = "G",
                                   RestingFloor = "T")


        with self.assertRaises(Exception):
            create_demand(demand)
    
    @patch("elevators.infra.infra_database.get_db")
    def test_get_demands_with_success(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        mock_demand = Demand(
            DemandRequest=datetime.strptime("07-22-2024 12:11:55", "%m-%d-%Y %H:%M:%S"),
            DemandedFloor="5",
            RequisitedFloor="G",
            RestingFloor="T"
        )

        mock_db.query.return_value.all.return_value = [mock_demand]

        expected_response = [
            {
                "DemandRequest": "07-22-2024 12:11:55",
                "RequisitedFloor": "G",
                "DemandedFloor": "5",
                "RestingFloor": "T"
            }
        ]

        response = get_demands()

        response_str = response.body.decode('utf-8')
        response_dict = json.loads(response_str)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get("Demands"), expected_response)

    @patch("elevators.infra.infra_database.get_db")
    def test_get_demands_with_exception(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        mock_db.query.side_effect = Exception("Database error")

        
        with self.assertRaises(Exception):
            get_demands()

    @patch("elevators.infra.infra_database.get_db")
    def test_get_demands_ranged_with_success(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        start_date = datetime.strptime("07-01-2024 00:00:00", "%m-%d-%Y %H:%M:%S")
        end_date = datetime.strptime("07-31-2024 23:59:59", "%m-%d-%Y %H:%M:%S")

        mock_demand = Demand(
            DemandRequest=datetime.strptime("07-15-2024 12:11:55", "%m-%d-%Y %H:%M:%S"),
            DemandedFloor="5",
            RequisitedFloor="G",
            RestingFloor="T"
        )

        mock_db.query.return_value.filter.return_value.all.return_value = [mock_demand]

        expected_response = {
            "DemandRange": f"{start_date} - {end_date}",
            "Demands": [
                {
                    "DemandRequest": "07-15-2024 12:11:55",
                    "RequisitedFloor": "G",
                    "DemandedFloor": "5",
                    "RestingFloor": "T"
                }
            ]
        }

        response = get_demands_ranged(start_date, end_date)

        response_str = response.body.decode('utf-8')
        response_dict = json.loads(response_str)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict, expected_response)

    @patch("elevators.infra.infra_database.get_db")
    def test_get_demands_ranged_with_exception(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        mock_db.query.side_effect = Exception("Database error")
        
        start_date = datetime.strptime("07-01-2024 00:00:00", "%m-%d-%Y %H:%M:%S")
        end_date = datetime.strptime("07-31-2024 23:59:59", "%m-%d-%Y %H:%M:%S")

        with self.assertRaises(Exception):
            get_demands_ranged(start_date, end_date)