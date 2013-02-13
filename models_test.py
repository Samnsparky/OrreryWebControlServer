import datetime
import unittest

import api_view
import config
import models


class TestRawStatusModel(unittest.TestCase):

    def setUp(self):
        config.DB_NAME = "test"
        self.conn = models.get_db_connection()
        self.cursor = self.conn.cursor()
        models.initalize_database_raw(self.cursor)
        models.delete_orrery_status_raw(self.cursor)

    def tearDown(self):
        self.cursor.close()
        self.conn.commit()
        models.release_db_connection()

    def test_create_read(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        test_status = models.OrreryStatus(400, 17.5, 100, today, now)
        models.create_orrery_status_raw(self.cursor, test_status)
        
        ret_test_status = models.read_orrery_status_raw(self.cursor)
        self.assertEqual(test_status, ret_test_status)

        models.delete_orrery_status_raw(self.cursor)

    def test_update(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        orig_status = models.OrreryStatus(400, 17.5, 100, today, now)
        new_status = models.OrreryStatus(401, 18.5, 101, today, now)

        models.create_orrery_status_raw(self.cursor, orig_status)
        models.update_orrery_status_raw(self.cursor, new_status)
        
        ret_test_status = models.read_orrery_status_raw(self.cursor)
        self.assertEqual(new_status, ret_test_status)

        models.delete_orrery_status_raw(self.cursor)

    def test_read_consistency(self):
        self.assertEqual(models.read_orrery_status_raw(self.cursor), None)

        today = datetime.date.today()
        now = datetime.datetime.now()
        test_status = models.OrreryStatus(400, 17.5, 100, today, now)
        
        models.create_orrery_status_raw(self.cursor, test_status)
        models.create_orrery_status_raw(self.cursor, test_status)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_status_raw(self.cursor)

        models.delete_orrery_status_raw(self.cursor)

    def test_update_consistency(self):
        self.assertEqual(models.read_orrery_status_raw(self.cursor), None)

        today = datetime.date.today()
        now = datetime.datetime.now()
        orig_status = models.OrreryStatus(400, 17.5, 100, today, now)
        
        models.create_orrery_status_raw(self.cursor, orig_status)
        models.create_orrery_status_raw(self.cursor, orig_status)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_status_raw(self.cursor)

        models.delete_orrery_status_raw(self.cursor)


class TestDecoratedStatusModel(unittest.TestCase):

    def setUp(self):
        config.DB_NAME = "test"
        models.initalize_database()
        models.delete_orrery_status()

    def test_create_read(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        test_status = models.OrreryStatus(400, 17.5, 100, today, now)
        models.create_orrery_status(test_status)
        
        ret_test_status = models.read_orrery_status()
        self.assertEqual(test_status, ret_test_status)

        models.delete_orrery_status()

    def test_update(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        orig_status = models.OrreryStatus(400, 17.5, 100, today, now)
        new_status = models.OrreryStatus(401, 18.5, 101, today, now)

        models.create_orrery_status(orig_status)
        models.update_orrery_status(new_status)
        
        ret_test_status = models.read_orrery_status()
        self.assertEqual(new_status, ret_test_status)

        models.delete_orrery_status()

    def test_read_consistency(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        
        self.assertEqual(models.read_orrery_status(), None)

        test_status = models.OrreryStatus(400, 17.5, 100, today, now)
        
        models.create_orrery_status(test_status)
        models.create_orrery_status(test_status)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_status()

        models.delete_orrery_status()

    def test_update_consistency(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        
        self.assertEqual(models.read_orrery_status(), None)

        orig_status = models.OrreryStatus(400, 17.5, 100, today, now)
        
        models.create_orrery_status(orig_status)
        models.create_orrery_status(orig_status)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_status()

        models.delete_orrery_status()


class TestRawConfigModel(unittest.TestCase):

    def setUp(self):
        config.DB_NAME = "test"
        self.conn = models.get_db_connection()
        self.cursor = self.conn.cursor()
        models.initalize_database_raw(self.cursor)
        models.delete_orrery_config_raw(self.cursor)

    def tearDown(self):
        self.cursor.close()
        self.conn.commit()
        models.release_db_connection()

    def test_create_read(self):
        test_config = models.OrreryConfig(400, True)
        models.create_orrery_config_raw(self.cursor, test_config)
        
        ret_test_config = models.read_orrery_config_raw(self.cursor)
        self.assertEqual(test_config, ret_test_config)

        models.delete_orrery_config_raw(self.cursor)

    def test_update(self):
        orig_config = models.OrreryConfig(400, True)
        new_config = models.OrreryConfig(400, False)

        models.create_orrery_config_raw(self.cursor, orig_config)
        models.update_orrery_config_raw(self.cursor, new_config)
        
        ret_test_config = models.read_orrery_config_raw(self.cursor)
        self.assertEqual(new_config, ret_test_config)

        models.delete_orrery_config_raw(self.cursor)

    def test_read_consistency(self):
        self.assertEqual(models.read_orrery_config_raw(self.cursor), None)

        test_config = models.OrreryConfig(400, True)
        
        models.create_orrery_config_raw(self.cursor, test_config)
        models.create_orrery_config_raw(self.cursor, test_config)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_config_raw(self.cursor)

        models.delete_orrery_config_raw(self.cursor)

    def test_update_consistency(self):
        self.assertEqual(models.read_orrery_config_raw(self.cursor), None)

        orig_config = models.OrreryConfig(400, True)
        
        models.create_orrery_config_raw(self.cursor, orig_config)
        models.create_orrery_config_raw(self.cursor, orig_config)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_config_raw(self.cursor)

        models.delete_orrery_config_raw(self.cursor)


class TestDecoratedConfigModel(unittest.TestCase):

    def setUp(self):
        config.DB_NAME = "test"
        models.initalize_database()
        models.delete_orrery_config()

    def test_create_read(self):
        test_config = models.OrreryConfig(400, True)
        models.create_orrery_config(test_config)
        
        ret_test_config = models.read_orrery_config()
        self.assertEqual(test_config, ret_test_config)

        models.delete_orrery_config()

    def test_update(self):
        orig_config = models.OrreryConfig(400, True)
        new_config = models.OrreryConfig(400, False)

        models.create_orrery_config(orig_config)
        models.update_orrery_config(new_config)
        
        ret_test_config = models.read_orrery_config()
        self.assertEqual(new_config, ret_test_config)

        models.delete_orrery_config()

    def test_read_consistency(self):
        self.assertEqual(models.read_orrery_config(), None)

        test_config = models.OrreryConfig(400, True)
        
        models.create_orrery_config(test_config)
        models.create_orrery_config(test_config)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_config()

        models.delete_orrery_config()

    def test_update_consistency(self):
        self.assertEqual(models.read_orrery_config(), None)

        orig_config = models.OrreryConfig(400, True)
        
        models.create_orrery_config(orig_config)
        models.create_orrery_config(orig_config)
        
        with self.assertRaises(RuntimeError):
            models.read_orrery_config()

        models.delete_orrery_config()


if __name__ == '__main__':
    unittest.main()
