"""
Mathematical routines for the orrery web control web service.

@author: Sam Pottinger
@license: GNU GPL v3
"""

import datetime

def calc_days_for_rotations(rotations):
    return rotations * 90.4

def calc_orrery_date(status_entry):
    delta_days = calc_days_for_rotations(status_entry.rotations)
    return status_entry.start_date + datetime.timedelta(days=delta_days)
