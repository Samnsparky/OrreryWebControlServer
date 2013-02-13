def orrery_status_to_dict(status):
    return {
        "motor_speed": status.motor_speed,
        "motor_draw": status.motor_draw,
        "rotations": status.rotations,
        "start_date": status.start_date,
        "update_datetime": status.update_datetime
    }


def orrery_config_to_dict(status):
    return {
        "motor_speed": status.motor_speed,
        "relay_enabled": status.relay_enabled
    }