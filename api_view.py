"""
Logic to render output in response to API calls.

@author: Sam Pottinger
@license: GNU GPL v3
"""

import json
import datetime

import math_util
import serialization


def render_orrery_status(record, render_full):
    """
    Render the status of the orrery as a JSON document in a string.

    @param record: The orrery status record to serialize to a JSON string.
    @type record: models.OrreryStatus
    @return: The given record as a JSON document.
    @rtype: str
    """
    orrery_date = math_util.calc_orrery_date(record)

    if render_full:
        return json.dumps(
                {
                    "orrery_date": str(orrery_date),
                    "real_date": str(datetime.date.today()),
                    "motor_speed": record.motor_speed,
                    "motor_draw": record.motor_draw,
                    "rotations": record.rotations,
                    "start_date": str(record.start_date),
                    "update_datetime": str(record.update_datetime)
                }
            )
    else:
        return json.dumps(
            {
                "orrery_date": str(orrery_date),
                "real_date": str(datetime.date.today()),
                "rotations": record.rotations
            }
        )


def render_orrery_config(record):
    """
    Render the status of the orrery configuration settings as a JSON document.

    @param record: The orrery configuration settings to serialize.
    @type record: models.OrreryConfig
    @return: The given record as a JSON document.
    @rtype: str
    """
    return json.dumps(serialization.orrery_config_to_dict(record))
