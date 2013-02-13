"""
Data modeling and management routines for the orrery web control web service.

@author: Sam Pottinger
@license: GNU GPL v3
"""

import collections

import psycopg2 as psycopq

import config
import serialization
import sql_statements


class PersistDbConnectionHolder:
    """Wrapper that mantains access to a process-wide db connection."""

    def __init__(self):
        """Create a new DB connection holder."""
        self.persist_db_connection = None

    def flush_db_connection(self):
        """Force reset the process db connection."""
        try:
            if self.persist_db_connection:
                self.persist_db_connection.close()
        except:
            pass
        db_config_vals = (config.DB_URI, config.DB_NAME)
        self.persist_db_connection = psycopq.connect(
            "host='%s' dbname='%s'" % db_config_vals
        )

    # TODO: This could be expensive... should pool.
    def get_db_connection(self):
        """
        Get this process' db connection.

        @return: The process-wide db connection.
        @rtype: psycopg2.Connection
        """
        if self.persist_db_connection == None:
            self.flush_db_connection()
        return self.persist_db_connection

    def return_db(self):
        """Indicate that the current thread has finished db operations."""
        pass


# Process-wide db connection holder
persist_db_connection_holder = PersistDbConnectionHolder()


# Named tuple to model the status of the orrery as persisted to the database.
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


# Named tuple to model the user configuration settings for the orrery as
# persisted to the database.
OrreryConfig = collections.namedtuple(
    "OrreryConfig",
    [
        "motor_speed",
        "relay_enabled"
    ]
)


def get_db_connection():
    """
    Get this process' shared DB connection instance.

    @return: This process' DB connection.
    @rtype: psycopg2.Connection
    """
    return persist_db_connection_holder.get_db_connection()


def release_db_connection():
    """Indicate that the current thread has finished DB operations."""
    persist_db_connection_holder.return_db()


def get_num_orrery_status_entries_raw(cursor):
    """
    Get the number of system status entries currently in the database.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: Number of system status entries in the given cursor's database.
    @rtype: int
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    cursor.execute(sql_statements.COUNT_ORRERY_STATUS_SQL)
    return cursor.fetchall()[0][0]


def check_orrery_status_table_raw(cursor):
    """
    Check that the database table for system status is in an expected state.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: True if an entry exists. False if no entries exist.
    @rtype: bool
    @raises RuntimeError: Raised if more than one system status entry exists in
        the database.
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    num_entries = get_num_orrery_status_entries_raw(cursor)

    if num_entries == 0:
        return False
    if num_entries > 1:
        raise RuntimeError("Many orrery status entries.")

    return True


def create_orrery_status_raw(cursor, new_status):
    """
    Create a new orrery status entry.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @param new_status: Record of the system's status.
    @type new_status: OrreryStatus
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    new_status_dict = serialization.orrery_status_to_dict(new_status)
    cursor.execute(sql_statements.INSERT_ORRERY_STATUS_SQL, new_status_dict)


def read_orrery_status_raw(cursor):
    """
    Get the status of the orrery.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: Record of the orrery system status.
    @rtype: OrreryStatus instance
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    if not check_orrery_status_table_raw(cursor):
        return None
    cursor.execute(sql_statements.READ_ORRERY_STATUS_SQL)
    entries = cursor.fetchall()
    return OrreryStatus(*entries[0])


def update_orrery_status_raw(cursor, new_status):
    """
    Update the orrery system status.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @param new_status: Record of the system's status to persist.
    @type new_status: OrreryStatus
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    if not check_orrery_status_table_raw(cursor):
        return None
    new_status_dict = serialization.orrery_status_to_dict(new_status)
    cursor.execute(sql_statements.UPDATE_ORRERY_STATUS_SQL, new_status_dict)


def delete_orrery_status_raw(cursor):
    """
    Delete all orrery system status entries.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    cursor.execute(sql_statements.DELETE_ORRERY_STATUS_SQL)


def get_num_orrery_config_entries_raw(cursor):
    """
    Get the number of user config entries currently in the database.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: Number of user config entries in the given cursor's database.
    @rtype: int
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    cursor.execute(sql_statements.COUNT_ORRERY_CONFIG_SQL)
    return cursor.fetchall()[0][0]


def check_orrery_config_table_raw(cursor):
    """
    Check that the database table for user configuration is in an expected state.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: True if an entry exists. False if no entries exist.
    @rtype: bool
    @raises RuntimeError: Raised if more than one user configuration entry
        exists in the database.
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    num_entries = get_num_orrery_config_entries_raw(cursor)

    if num_entries == 0:
        return False
    if num_entries > 1:
        raise RuntimeError("Many orrery config entries.")

    return True


def create_orrery_config_raw(cursor, new_status):
    """
    Create a new orrery user configuration entry.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @param new_status: Record of the system's status.
    @type new_status: OrreryConfig
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    new_status_dict = serialization.orrery_config_to_dict(new_status)
    cursor.execute(sql_statements.INSERT_ORRERY_CONFIG_SQL, new_status_dict)


def read_orrery_config_raw(cursor):
    """
    Get the current user configuration of the orrery.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: Record of the orrery system user configuration.
    @rtype: OrreryConfig instance
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    if not check_orrery_config_table_raw(cursor):
        return None
    cursor.execute(sql_statements.READ_ORRERY_CONFIG_SQL)
    entries = cursor.fetchall()
    return OrreryConfig(*entries[0])


def update_orrery_config_raw(cursor, new_status):
    """
    Update the orrery system user configuration.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @param new_status: Record of the system's status to persist.
    @type new_status: OrreryConfig
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    if not check_orrery_config_table_raw(cursor):
        return None
    new_status_dict = serialization.orrery_config_to_dict(new_status)
    cursor.execute(sql_statements.UPDATE_ORRERY_CONFIG_SQL, new_status_dict)


def delete_orrery_config_raw(cursor):
    """
    Delete all orrery system user configuration entries.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    cursor.execute(sql_statements.DELETE_ORRERY_CONFIG_SQL)


def initalize_database_raw(cursor):
    """
    Sets up database tables if they do not exist and sets initial entries.

    Sets up the database tables if they do not exist and adds a default user
    configuration entry if none currently exists.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @note: Does not try to commit changes or manage database connection in any
        way.
    """
    cursor.execute(sql_statements.CREATE_ORRERY_STATUS_TABLE_SQL)
    cursor.execute(sql_statements.CREATE_ORRERY_CONFIG_TABLE_SQL)

    if get_num_orrery_config_entries_raw(cursor) == 0:
        default_config = OrreryConfig(
            config.DEFAULT_ORRERY_CONFIG_SPEED,
            config.DEFAULT_RELAY_STATUS
        )
        create_orrery_config_raw(cursor, default_config)


def get_orrery_config_and_status_raw(cursor):
    """
    Get the orrery user configuration and system status entries together.

    @param cursor: The databse cursor to use to execute the request.
    @type cursor: psycopg2.Cursor
    @return: Tuple of orrery user configuration and orrery system status
        entries.
    @rtype: tuple
    """
    return (
        read_orrery_config_raw(cursor),
        read_orrery_status_raw(cursor)
    )


def run_on_app_db(func, args, retry=True):
    """
    Run a function using the system database as configured by the environment.

    Runs a function using the system database as configured by the environment,
    committing changes after the opreation completes.

    @param func: The function to execute with the system database.
    @type func: function
    @param args: The arguments to execute the function with after having added
        a database cursor.
    @type args: list or tuple
    @return: Return value from passed function.
    """
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
    """
    Check that the database table for system status is in an expected state.

    @return: True if an entry exists. False if no entries exist.
    @rtype: bool
    @raises RuntimeError: Raised if more than one status entry exists.
    """
    return run_on_app_db(check_orrery_table_status_raw, args)


def create_orrery_status(*args):
    """
    Create a new orrery status entry.

    @param new_status: Record of the system's status.
    @type new_status: OrreryStatus
    @note: Commits after operation completes.
    """
    return run_on_app_db(create_orrery_status_raw, args)


def read_orrery_status(*args):
    """
    Get the status of the orrery.

    @return: Record of the orrery system status.
    @rtype: OrreryStatus instance
    """
    return run_on_app_db(read_orrery_status_raw, args)


def update_orrery_status(*args):
    """
    Update the orrery system status.

    @param new_status: Record of the system's status to persist.
    @type new_status: OrreryStatus
    @note: Commits after operation completes.
    """
    return run_on_app_db(update_orrery_status_raw, args)


def delete_orrery_status(*args):
    """
    Delete orrery system status entries.

    @note: Commits after operation completes.
    """
    return run_on_app_db(delete_orrery_status_raw, args)


def check_orrery_config_table(*args):
    """
    Check the database table for user configuration is in an expected state.

    @return: True if an entry exists. False if no entries exist.
    @rtype: bool
    @raises RuntimeError: Raised if multiple user configuration entries exist.
    """
    return run_on_app_db(check_orrery_config_table_raw, args)


def create_orrery_config(*args):
    """
    Create a new orrery user configuration entry.

    @param new_status: New record of the system's user configuration.
    @type new_status: OrreryStatus
    @note: Commits after operation completes.
    """
    return run_on_app_db(create_orrery_config_raw, args)


def read_orrery_config(*args):
    """
    Get the current user configuration of the orrery.

    @return: Record of the orrery system status.
    @rtype: OrreryStatus instance
    """
    return run_on_app_db(read_orrery_config_raw, args)


def update_orrery_config(*args):
    """
    Update the orrery's user configuration.

    @param new_status: New record of the system's user configuration.
    @type new_status: OrreryConfig
    @note: Commits after operation completes.
    """
    return run_on_app_db(update_orrery_config_raw, args)


def delete_orrery_config(*args):
    """
    Delete orrery system user configuration entries.

    @note: Commits after operation completes.
    """
    return run_on_app_db(delete_orrery_config_raw, args)


def initalize_database(*args):
    """
    Initialize the database with default tables and entries.

    Create system database tables if they are not present and add default user
    configuration entry if no user configuration entry exists.
    """
    return run_on_app_db(initalize_database_raw, args)


def get_orrery_config_and_status(*args):
    """
    Get the orrery user configuration and system status entries together.

    @return: Tuple of orrery user configuration and orrery system status
        entries.
    @rtype: tuple
    """
    return run_on_app_db(get_orrery_config_and_status_raw, args)
