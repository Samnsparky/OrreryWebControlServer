"""
Collection of SQL statements for orrery web control database operations.

@author: Sam Pottinger
@license: GNU GPL v3
"""

COUNT_ORRERY_STATUS_SQL = "SELECT COUNT(*) FROM system_state"

INSERT_ORRERY_STATUS_SQL = "INSERT INTO system_state (motor_speed, "\
    "motor_draw, rotations, start_date, update_datetime) VALUES "\
    "(%(motor_speed)s, %(motor_draw)s, %(rotations)s, %(start_date)s, "\
    "%(update_datetime)s)"

READ_ORRERY_STATUS_SQL = "SELECT motor_speed, motor_draw, rotations, "\
    "start_date, update_datetime FROM system_state"

UPDATE_ORRERY_STATUS_SQL = "UPDATE system_state SET "\
    "motor_speed=%(motor_speed)s, motor_draw=%(motor_draw)s, "\
    "rotations=%(rotations)s, start_date=%(start_date)s, "\
    "update_datetime=%(update_datetime)s"

DELETE_ORRERY_STATUS_SQL = "DELETE FROM system_state"

CREATE_ORRERY_STATUS_TABLE_SQL = "CREATE TABLE IF NOT EXISTS system_state "\
    "(motor_speed real, motor_draw real, rotations real, start_date date, "\
    "update_datetime timestamp);"


COUNT_ORRERY_CONFIG_SQL = "SELECT COUNT(*) FROM system_config"

INSERT_ORRERY_CONFIG_SQL = "INSERT INTO system_config (motor_speed, "\
    "relay_enabled) VALUES (%(motor_speed)s, %(relay_enabled)s)"

READ_ORRERY_CONFIG_SQL = "SELECT motor_speed, relay_enabled FROM system_config"

UPDATE_ORRERY_CONFIG_SQL = "UPDATE system_config SET "\
    "motor_speed=%(motor_speed)s, relay_enabled=%(relay_enabled)s"

DELETE_ORRERY_CONFIG_SQL = "DELETE FROM system_config"

CREATE_ORRERY_CONFIG_TABLE_SQL = "CREATE TABLE IF NOT EXISTS system_config "\
    "(motor_speed real, relay_enabled bool);"
