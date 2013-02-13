import json
import unittest

import config
import controllers
import models


class TestAPI(unittest.TestCase):

    def setUp(self):
        config.DB_NAME = "test"
        models.initalize_database()
        self.app = controllers.app.test_client()

    def tearDown(self):
        models.delete_orrery_status()
        models.delete_orrery_config()

    def status_dicts_equal(self, dict1, dict2):
        same = True
        same = same and dict1["motor_speed"] == dict2["motor_speed"]
        same = same and dict1["motor_draw"] == dict2["motor_draw"]
        same = same and dict1["rotations"] == dict2["rotations"]
        return same

    def config_dicts_equal(self, dict1, dict2):
        same = True
        same = same and dict1["motor_speed"] == dict2["motor_speed"]
        same = same and dict1["relay_enabled"] == dict2["relay_enabled"]
        return same

    def test_status(self):
        # Create initial entry
        initial_entry_data = {
            "motor_speed": 200,
            "motor_draw": 100,
            "rotations": 300
        }
        ret_val = self.app.post("/api/status.json", data=initial_entry_data)
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.status_dicts_equal(ret_dict, initial_entry_data))

        # Test initial entry
        # TODO: Test datetime
        ret_val = self.app.get("/api/status.json")
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.status_dicts_equal(ret_dict, initial_entry_data))

        # Update entry
        updated_entry_data = {
            "motor_speed": 200,
            "motor_draw": 100,
            "rotations": 400
        }
        ret_val = self.app.post("/api/status.json", data=updated_entry_data)
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.status_dicts_equal(ret_dict, updated_entry_data))

        # Test updated entry
        # TODO: Test datetime
        ret_val = self.app.get("/api/status.json")
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.status_dicts_equal(ret_dict, updated_entry_data))

    def test_concise_status(self):
        # Create initial entry
        initial_entry_data = {
            "motor_speed": 200,
            "motor_draw": 100,
            "rotations": 300
        }
        ret_val = self.app.post("/api/status.json", data=initial_entry_data)
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.status_dicts_equal(ret_dict, initial_entry_data))

        # Test concise display
        # TODO: More rigorous test
        ret_val = self.app.get("/api/concise_status.json")
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertEqual(ret_dict["rotations"], initial_entry_data["rotations"])

    def test_config(self):
        # Create initial config
        initial_entry_data = {
            "motor_speed": 200,
            "relay_enabled": False
        }
        ret_val = self.app.post("/api/config.json", data=initial_entry_data)
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.config_dicts_equal(ret_dict, initial_entry_data))

        # Test initial config
        # TODO: Test datetime
        ret_val = self.app.get("/api/config.json")
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.config_dicts_equal(ret_dict, initial_entry_data))

        # Update config
        updated_entry_data = {
            "motor_speed": 300,
            "relay_enabled": True
        }
        ret_val = self.app.post("/api/config.json", data=updated_entry_data)
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.config_dicts_equal(ret_dict, updated_entry_data))

        # Test updated config
        # TODO: Test datetime
        ret_val = self.app.get("/api/config.json")
        ret_str = ret_val.data
        ret_dict = json.loads(ret_str)
        self.assertTrue(self.config_dicts_equal(ret_dict, updated_entry_data))


if __name__ == '__main__':
    unittest.main()