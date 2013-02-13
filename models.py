import collections
import threading

import psycopg2 as psycopq

import config
import serialization
import sql_statements


class PersistDbConnectionHolder:

    def __init__(self):
        self.persist_db_connection = None
        self.persist_db_connection_lock = threading.Lock()

    def flush_db_connection(self):
        db_config_vals = (config.DB_URI, config.DB_NAME)
        self.persist_db_connection = psycopq.connect(
            "host='%s' dbname='%s'" % db_config_vals
        )

    # TODO: This could be expensive... should pool.
    def get_db_connection(self):
        if self.persist_db_connection == None:
            self.flush_db_connection()
        return self.persist_db_connection

    def return_db(self):
        pass

persist_db_connection_holder = PersistDbConnectionHolder()


OrreryStatus = collections.namedtuple(
    "OrreryStatus",
    [
        "motor_speed",
        "motor_draw",
        "rotations",
        "start_date",
        "update_datetime"
    ]
)


OrreryConfig = collections.namedtuple(
    "OrreryConfig",
    [
        "motor_speed",
        "relay_enabled"
    ]
)


def get_db_connection():
    return persist_db_connection_holder.get_db_connection()


def release_db_connection():
    persist_db_connection_holder.return_db()


def get_num_orrery_status_entries_raw(cursor):
    cursor.execute(sql_statements.COUNT_ORRERY_STATUS_SQL)
    return cursor.fetchall()[0][0]


def check_orrery_status_table_raw(cursor):
    num_entries = get_num_orrery_status_entries_raw(cursor)

    if num_entries == 0:
        return False
    if num_entries > 1:
        raise RuntimeError("Many orrery status entries.")

    return True


def create_orrery_status_raw(cursor, new_status):
    new_status_dict = serialization.orrery_status_to_dict(new_status)
    cursor.execute(sql_statements.INSERT_ORRERY_STATUS_SQL, new_status_dict)


def read_orrery_status_raw(cursor):
    if not check_orrery_status_table_raw(cursor):
        return None
    cursor.execute(sql_statements.READ_ORRERY_STATUS_SQL)
    entries = cursor.fetchall()
    return OrreryStatus(*entries[0])


def update_orrery_status_raw(cursor, new_status):
    if not check_orrery_status_table_raw(cursor):
        return None
    new_status_dict = serialization.orrery_status_to_dict(new_status)
    cursor.execute(sql_statements.UPDATE_ORRERY_STATUS_SQL, new_status_dict)


def delete_orrery_status_raw(cursor):
    cursor.execute(sql_statements.DELETE_ORRERY_STATUS_SQL)


def get_num_orrery_config_entries_raw(cursor):
    cursor.execute(sql_statements.COUNT_ORRERY_CONFIG_SQL)
    return cursor.fetchall()[0][0]


def check_orrery_config_table_raw(cursor):
    num_entries = get_num_orrery_config_entries_raw(cursor)

    if num_entries == 0:
        return False
    if num_entries > 1:
        raise RuntimeError("Many orrery config entries.")

    return True


def create_orrery_config_raw(cursor, new_status):
    new_status_dict = serialization.orrery_config_to_dict(new_status)
    cursor.execute(sql_statements.INSERT_ORRERY_CONFIG_SQL, new_status_dict)


def read_orrery_config_raw(cursor):
    if not check_orrery_config_table_raw(cursor):
        return None
    cursor.execute(sql_statements.READ_ORRERY_CONFIG_SQL)
    entries = cursor.fetchall()
    return OrreryConfig(*entries[0])


def update_orrery_config_raw(cursor, new_status):
    if not check_orrery_config_table_raw(cursor):
        return None
    new_status_dict = serialization.orrery_config_to_dict(new_status)
    cursor.execute(sql_statements.UPDATE_ORRERY_CONFIG_SQL, new_status_dict)


def delete_orrery_config_raw(cursor):
    cursor.execute(sql_statements.DELETE_ORRERY_CONFIG_SQL)


def initalize_database_raw(cursor):
    cursor.execute(sql_statements.CREATE_ORRERY_STATUS_TABLE_SQL)
    cursor.execute(sql_statements.CREATE_ORRERY_CONFIG_TABLE_SQL)

    if get_num_orrery_config_entries_raw(cursor) == 0:
        default_config = OrreryConfig(
            config.DEFAULT_ORRERY_CONFIG_SPEED,
            config.DEFAULT_RELAY_STATUS
        )
        create_orrery_config_raw(cursor, default_config)


def get_orrery_config_and_status_raw(cursor):
    return (
        read_orrery_config_raw(cursor),
        read_orrery_status_raw(cursor)
    )


def run_on_app_db(func, args, retry=True):
    try:
        conn = persist_db_connection_holder.get_db_connection()
        cursor = conn.cursor()
        ret_val = func(cursor, *args)
        conn.commit()
    except psycopq.OperationalError as e:
        persist_db_connection_holder.flush_db_connection()
        if retry:
            ret_val = run_on_app_db(func, args, retry=False)
        else:
            release_db_connection()
            raise OperationalError(str(e))

    release_db_connection()
    return ret_val


def check_orrery_table_status(*args):
    return run_on_app_db(check_orrery_table_status_raw, args)


def create_orrery_status(*args):
    return run_on_app_db(create_orrery_status_raw, args)


def read_orrery_status(*args):
    return run_on_app_db(read_orrery_status_raw, args)


def update_orrery_status(*args):
    return run_on_app_db(update_orrery_status_raw, args)


def delete_orrery_status(*args):
    return run_on_app_db(delete_orrery_status_raw, args)


def check_orrery_config_table(*args):
    return run_on_app_db(check_orrery_config_table_raw, args)


def create_orrery_config(*args):
    return run_on_app_db(create_orrery_config_raw, args)


def read_orrery_config(*args):
    return run_on_app_db(read_orrery_config_raw, args)


def update_orrery_config(*args):
    return run_on_app_db(update_orrery_config_raw, args)


def delete_orrery_config(*args):
    return run_on_app_db(delete_orrery_config_raw, args)


def initalize_database(*args):
    return run_on_app_db(initalize_database_raw, args)


def get_orrery_config_and_status(*args):
    return run_on_app_db(get_orrery_config_and_status_raw, args)
