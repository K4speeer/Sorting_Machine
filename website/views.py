from flask import views, request, Blueprint, render_template, redirect, session, url_for
from datetime import datetime
from sorting_machine import init_board, init_machine, Gate 
from . import db
from .models import sessions
from time import sleep
from configs import IR, STP_P, DIR_P, SRV_CONF
from sqlalchemy import funcfilter

views = Blueprint("views", __name__)




colorList = ["black", "blue", "green", "Orange", "purple", "red", "yellow"]
sizeList = ["small", "big"]        



@views.route("/", methods=["GET", "POST"])
@views.route("home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "start_new_session" in request.form:
            last_id = sessions.query.count()
            session.permanent = True
            session["session_id"] = last_id + 1
            # session["board"] = init_board()
            return redirect("/configurations") 
        elif "history" in request.form:
            return redirect("/full_history") 
        else:
            return render_template("home.html")
    if session:
        session.clear()
    return render_template("home.html")



@views.route("/configurations", methods=["GET", "POST"])
def configs():
    if request.method == "POST":
        if "servo_test" in request.form:
            selected_servo = request.form.get("servo-gates")
            if selected_servo != 0:
                # close_pos = selected_servo[selected_servo][0]
                # open_pos = selected_servo[selected_servo][1]
                # pos = selected_servo[selected_servo][2]
                # g = Gate(session["board"], selected_servo, close_pos, open_pos, pos)
                # g.test_servo()
                pass
                
            return redirect("/configurations#motors")
        if "apply" in request.form or "discard" in request.form:
            return redirect("/sort")
    return render_template("configs.html")      
            

@views.route("/sort", methods=["POST", "GET"])
def sort():
    servo_params = []
    if request.method == "POST":
        print(request.form)
        if "sns" in request.form:
            general_sort_parameter = request.form.get("gen_param")
            g1_color = request.form.get("colorRadios1")
            g1_size = request.form.get("sizeRadios1")
            g2_color = request.form.get("colorRadios2")
            g2_size = request.form.get("sizeRadios2")
            servo_params = [f"{g1_color}{g1_size}",f"{g2_color}{g2_size}"]
            return render_template("in_process.html", general=general_sort_parameter, servo=servo_params)
        elif "default" in request.form:
            return render_template("in_process.html", general="color", servo=["red", "green", ""])
    return render_template("sort.html")
    
@views.route("/history", methods=["GET", "POST"])
def history():
    if request.method == "POST":
        if "full_history" in request.form:
            return redirect("/full_history")
    return render_template("history.html")

@views.route("/full_history", methods=["GET", "POST"])
def full_history():
    return render_template("full_history.html")

@views.route("/in_process", methods=["GET", "POST"])
def process():
    return render_template("process.html")
# @views.route("/configurations", methods=["POST", "GET"])
# def configs():
#     if request.method == "POST":
#         if "com_port" in request.form:
#             com_port = request.form.get("com_port")
#             session["com_port"] = com_port
#             user_configs["com_port"] = com_port
#             return render_template("configs.html", submitted_settings = user_configs)
#         elif "cam_resolution" in request.form:
#             cam_resoultion = request.form.get("cam_resolution")
#             session["cam_resolution"] = cam_resoultion
#             user_configs["cam_resolution"] = cam_resoultion
#             return render_template("configs.html", submitted_settings =  user_configs)
#         elif "servo-gates" in request.form:
#             selected_servo = request.form.get("servo-gates")
#             if selected_servo != 0:
#                 close_pos = selected_servo[selected_servo][0]
#                 open_pos = selected_servo[selected_servo][1]
#                 pos = selected_servo[selected_servo][2]
#                 g = Gate(session["board"], selected_servo, close_pos, open_pos, pos)
#                 g.open()
#                 sleep(1.5)
#                 g.close()
#                 sleep(1.5)
#             else:
#                 pass
#             return render_template("configs.html", submitted_settings = user_configs)
#         elif "servo_test" in request.form:
#             return render_template("configs.html", submitted_settings = user_configs)
#         elif "apply" in request.form:
#             return redirect("/sort")
#         elif "discard" in request.form:
#             return render_template("configs.html", submitted_settings = default_configs)
#         else:
#             return render_template("configs.html", submitted_settings = default_configs)
        
        
#     return render_template("configs.html", submitted_settings = default_configs)


# @views.route("preview")
# def cam_preview():
#     preview_image_path = "../sessions/preview.jpg"
#     with Picamera2() as cam:
#         cam.start()
#         cam.capture_file(preview_image_path)
        
#     return render_template("preview.html", preview_image_path=preview_image_path)