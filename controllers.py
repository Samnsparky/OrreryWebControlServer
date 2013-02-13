import datetime
import json
import os

import flask

import api_view
import math_util
import models
import serialization


app = flask.Flask(__name__)
app.debug = True


@app.route("/api/concise_status.json")
def api_simple_status():
    orrery_status = models.read_orrery_status()
    return api_view.render_orrery_status(orrery_status, False)


@app.route("/api/status.json", methods=["GET", "POST"])
def api_full_status():
    if flask.request.method == "GET":
        orrery_status = models.read_orrery_status()
        return api_view.render_orrery_status(orrery_status, True)

    else:
        old_status_entry = models.read_orrery_status()
    
        motor_speed = float(flask.request.form["motor_speed"])
        motor_draw = float(flask.request.form["motor_draw"])
        rotations = float(flask.request.form["rotations"])

        status_entry_exists = old_status_entry != None

        if status_entry_exists:
            start_date = old_status_entry.start_date
        else:
            start_date = datetime.date.today()
        
        new_status_entry = models.OrreryStatus(
            motor_speed,
            motor_draw,
            rotations,
            start_date,
            datetime.datetime.now()
        )

        if status_entry_exists:
            models.update_orrery_status(new_status_entry)
        else:
            models.create_orrery_status(new_status_entry)

        return api_view.render_orrery_status(new_status_entry, True)


@app.route("/api/config.json", methods=["GET", "POST"])
def api_set_config():

    if flask.request.method == "GET":
        config_entry = models.read_orrery_config()
        return api_view.render_orrery_config(config_entry)

    else:
        old_config_entry = models.read_orrery_config()

        new_motor_speed = flask.request.form.get("motor_speed", None)
        if new_motor_speed == None:
            new_motor_speed = old_config_entry.motor_speed
        else:
            new_motor_speed = float(new_motor_speed)

        new_relay_enabled = flask.request.form.get("relay_enabled", None)
        if new_relay_enabled == None:
            new_relay_enabled = old_config_entry.relay_enabled
        else:
            new_relay_enabled = new_relay_enabled.lower() == "true"

        new_config_entry = models.OrreryConfig(
            new_motor_speed,
            new_relay_enabled
        )
        models.update_orrery_config(new_config_entry)

        return api_view.render_orrery_config(new_config_entry)


@app.route("/human/system_status")
def system_status():
    (config_entry, status_entry) = models.get_orrery_config_and_status()
    config_entry_dict = serialization.orrery_config_to_dict(config_entry)
    status_entry_dict = serialization.orrery_status_to_dict(status_entry)
    template_vals = dict(config_entry_dict.items() + status_entry_dict.items())
    template_vals["title"] = "System Status"
    return flask.render_template("system_status.html", **template_vals)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT ", 5000))
    models.initalize_database()
    app.run(host="0.0.0.0", port=port)