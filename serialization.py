"""
Routines to serialize data models to dictionaries.

@author: Sam Pottinger
@license: GNU GPL v3
"""

def orrery_status_to_dict(status):
    """
    Serialize an orrery status entry to a dictionary.

    @param status: The status entry to serialize.
    @type status: models.OrreryStatus
    @return: Serialized version of status as dictionary.
    @rtype: dict
    """
    return {
        "motor_speed": status.motor_speed,
        "motor_draw": status.motor_draw,
        "rotations": status.rotations,
        "start_date": status.start_date,
        "update_datetime": status.update_datetime
    }


def orrery_config_to_dict(status):
    """
    Serialize an orrery config entry to a dictionary.

    @param status: The status entry to serialize.
    @type status: models.OrreryConfig
    @return: Serialized version of status as dictionary.
    @rtype: dict
    """
    return {
        "motor_speed": status.motor_speed,
        "relay_enabled": status.relay_enabled
    }
