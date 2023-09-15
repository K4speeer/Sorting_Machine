from flask import views, request, Blueprint, render_template, redirect, session, url_for
from datetime import datetime
from sorting_machine import init_board, init_machine, Gate 
from . import db
from .models import sessions
from time import sleep
from configs import IR, STP_P, DIR_P, SRV_CONF
from sqlalchemy import funcfilter
from picamera2 import Picamera2
import os


views = Blueprint("views", __name__)


generalParameters = ["color", "size", "colorsize"]
gatesList = ["Gate1", "Gate2"]
colorList = ["blue", "green", "orange", "purple", "red", "yellow"]
sizeList = ["small", "big"]        
gatesParams = []
board = ''
machine = ''

@views.route("/", methods=["GET", "POST"])
@views.route("home", methods=["POST", "GET"])
def home():
    global board
    global machine
    global generalParameters
    global gatesList
    global colorList
    global sizeList
    global gatesParams
    
    if request.method == "POST":
        if "start_new_session" in request.form:
            last_id = sessions.query.count()
            session.permanent = True
            session["session_id"] = last_id
            if board == "":
                board = init_board()
            return redirect("/configurations") 
        elif "history" in request.form:
            return redirect("/full_history") 
        else:
            return render_template("home.html")
    if "finishing" in session:
        generalParameters = ["color", "size", "colorsize"]
        gatesList = ["Gate1", "Gate2"]
        colorList = ["blue", "green", "orange", "purple", "red", "yellow"]
        sizeList = ["small", "big"]        
        gatesParams = []
        board = ''
        machine = ''
        session.pop("gen_param", None)
        session.pop("Gate1_color", None)
        session.pop("Gate1_size", None)
        session.pop("Gate2_color", None)
        session.pop("Gate2_size", None)
        session.pop("session_id", None)
        session.pop("gates_params", None)
        session.pop('start', None)
        session.pop('initialize_machine', None)
        session.pop("finishing", None)
    return render_template("home.html")



@views.route("/configurations", methods=["GET", "POST"])
def configs():
    global board
    if request.method == "POST":
        if "servo_test" in request.form:
            selected_servo = request.form.get("servo-gates")
            selected_servo = int(selected_servo)
            if selected_servo != 0:
                close_pos = SRV_CONF[selected_servo][0]
                open_pos = SRV_CONF[selected_servo][1]
                pos = SRV_CONF[selected_servo][2]
                g = Gate(board, selected_servo, close_pos, open_pos, pos)
                g.test_servo()
                
            return redirect("/configurations#motors")
        if "apply" in request.form or "discard" in request.form:
            return redirect("/sort")
    return render_template("configs.html")      


@views.route("/sort", methods=["POST", "GET"])
def sort():
    if request.method == "POST":
        if "accept" in request.form:
            general_parameter = request.form.get("gen_param")
            session['gen_param'] = general_parameter
            print(general_parameter)
            print("redirecting to pick from sort")
            return redirect(f"/pick/{general_parameter}")
            
    return render_template("sort.html")

@views.route("/pick", methods=["GET", "POST"])
def pick():
    return redirect("/verify")


@views.route("/pick/color", methods=["GET", "POST"])
def pick_color():
    global gatesList
    for gate in gatesList:
        if f"{gate}_color" not in session:
            print(f"redirecting to /pick/color/{gatesList[0]}")
            return redirect(f"/pick/color/{gatesList[0]}")
        return redirect(f"/pick/color/{gatesList[1]}")
    
    return redirect("/pick")

@views.route("/pick/color/<gate>", methods=["GET", "POST"])
def pick_color_gate(gate):
    global gatesList
    global colorList
    if request.method =="POST":
        print(request.form)
        key = f"{gate}_color"
        print(key)
        val = request.form.get(gate)
        print(val)
        session[key] = val
        print(session)
        return redirect("/pick/color")
    gen_param = session["gen_param"]
    if gate == gatesList[1] and f"{gate}_color" not in session:
        if session["gen_param"] != "colorsize":
            color_to_remove = session["Gate1_color"]
            options = colorList
            options.remove(color_to_remove)
            return render_template("pick.html", gate=gate, optionList=options, gen_param=gen_param)
        return render_template("pick.html", gate=gate, optionList=colorList, gen_param=gen_param)
    elif f"{gatesList[0]}_color" in session and f"{gatesList[0]}_color" in session:
        if session["gen_param"] != "colorsize":
            return redirect("/pick")
        return redirect("/pick/colorsize")
    return render_template("pick.html", gate=gate, optionList=colorList, gen_param=gen_param)
   
@views.route("/pick/size", methods=["GET", "POST"])
def pick_size():
    global gatesList
    for gate in gatesList:
        if f"{gate}_size" not in session:
            print(f"redirecting to /pick/size/{gatesList[0]}")
            return redirect(f"/pick/size/{gatesList[0]}")
        return redirect(f"/pick/size/{gatesList[1]}")
    
    return redirect("/pick")

@views.route("/pick/size/<gate>", methods=["GET", "POST"])
def pick_size_gate(gate):
    global gatesList
    global sizeList
    if request.method =="POST":
        print(request.form)
        key = f"{gate}_size"
        print(key)
        val = request.form.get(gate)
        print(val)
        session[key] = val
        print(session)
        return redirect("/pick/size")
    gen_param = session["gen_param"]
    if gate == gatesList[1] and f"{gate}_size" not in session:
        if session["gen_param"] != "colorsize":
            size_to_remove = session["Gate1_size"]
            options = sizeList
            options.remove(size_to_remove)
            return render_template("pick.html", gate=gate, optionList=options, gen_param=gen_param)
        return render_template("pick.html", gate=gate, optionList=sizeList, gen_param=gen_param)
    
    elif f"{gatesList[0]}_size" in session and f"{gatesList[0]}_size" in session:
        if session["gen_param"] != "colorsize":
            return redirect("/pick")
        return redirect("/pick/colorsize")
    
    return render_template("pick.html", gate=gate, optionList=sizeList, gen_param=gen_param)

@views.route("/pick/colorsize", methods=["GET", "POST"])
def pick_color_size():
    global gatesList
    sort_types = ["color", "size"]
    for gate in gatesList:
        for s_type in sort_types:
            if f"{gate}_{s_type}" not in session:
                return redirect(f"/pick/{s_type}/{gate}")
    
    return redirect("/pick")

        
@views.route("/verify", methods=("GET", "POST"))
def verify():
    data = []
    gen = session["gen_param"]
    data.append(gen)
    global gatesList
    sort_types = ["color", "size"]
    gate_params = []
    for gate in gatesList:
        gateParameter = ''
        for s_type in sort_types:
            key = f"{gate}_{s_type}"
            if key in session:
                parameter = session[key]
                gateParameter += parameter
                data.append(parameter)
            else:
                data.append("-")
        gate_params.append(gateParameter)
    gate_params.append('')
    session["gates_params"] = gate_params
    # Add some logic to prevent same color or same size in multi-mode
    if request.method == "POST":
        if "start" in request.form:
            session["start"] = True
            return redirect("/in_process")
            
    
    return render_template("verify.html", configs=data)    

  
    
@views.route("/history", methods=["GET", "POST"])
def history():
    last_sessions = sessions.query.order_by(sessions.dateTime.desc()).limit(3).all()

    # Prepare the data for rendering
    session_data = []
    for session in last_sessions:
        session_info = {
            '_id': session._id,
            'dateTime': session.dateTime,
            'total_objects': session.total_objects,
            'parameters': [
                session.gate1_params,
                session.gate2_params,
                session.gate3_params
            ]
        }
        session_data.append(session_info)
        
    if request.method == "POST":
        if "full_history" in request.form:
            return redirect("/full_history")
    return render_template("history.html", sessions = session_data)

@views.route("/report/<int:s_id>", methods=["GET", "POST"])
def report(s_id):
    global generalParameters
    global gatesList
    global colorList
    global sizeList
    global gatesParams
    s_data = sessions.query.get(s_id)
    report_session = {
            "Date": s_data.dateTime,
            "Start Time": s_data.start_time,
            "End Time": s_data.end_time,
            "Total Objects": s_data.total_objects,
            "General Parameter": s_data.general_parameter,
            "Gate 1 Parameter": s_data.gate1_params,
            "Gate 1 Objects": s_data.gate1_objects,
            "Gate 2 Parameter": s_data.gate2_params,
            "Gate 2 Objects": s_data.gate2_objects,
            "Gate 3 Parameter": s_data.gate3_params,
            "Gate 3 Objects": s_data.gate3_objects}
    session.pop("gen_param", None)
    session.pop("Gate1_color", None)
    session.pop("Gate1_size", None)
    session.pop("Gate2_color", None)
    session.pop("Gate2_size", None)
    session.pop("session_id", None)
    session.pop("gates_params", None)
    session.pop('start', None)
    session.pop('initialize_machine', None)
    generalParameters = ["color", "size", "colorsize"]
    gatesList = ["Gate1", "Gate2"]
    colorList = ["blue", "green", "orange", "purple", "red", "yellow"]
    sizeList = ["small", "big"]        
    gatesParams = []
    print(report_session)
    return render_template("report.html", report=report_session)



@views.route("/full_history", methods=["GET", "POST"])
def full_history():
    data = sessions.query.all()
    full_report = []
    for s_data in data:
        session = {"ID": s_data._id,
            "Date": s_data.dateTime,
            "Start Time": s_data.start_time,
            "End Time": s_data.end_time,
            "Total Objects": s_data.total_objects,
            "General Parameter": s_data.general_parameter,
            "Gate 1 Parameter": s_data.gate1_params,
            "Gate 1 Objects": s_data.gate1_objects,
            "Gate 2 Parameter": s_data.gate2_params,
            "Gate 2 Objects": s_data.gate2_objects,
            "Gate 3 Parameter": s_data.gate3_params,
            "Gate 3 Objects": s_data.gate3_objects}
        full_report.append(session)
    return render_template("full_history.html", data=full_report)

@views.route("/in_process", methods=["GET", "POST"])
def in_process():
    if request.method == "POST":
        if "stop" in request.form:
            return redirect("/in_process/finishing")
    if 'start' in session:
        return redirect("/in_process/initializing_machine")

    return render_template("in_process.html", info="Processing")

@views.route("/in_process/initializing_machine", methods=["GET", "POST"])
def initing():
    global board 
    global machine
    if request.method == "POST":
        if "stop" in request.form:
            return redirect("/in_process/finishing")  
    if 'initializing_machine' not in session:
        machine = init_machine(board, IR, STP_P, DIR_P, SRV_CONF)
        session['initializing_machine'] = True
        return redirect("/in_process/configuring")
    
    return redirect("/in_process")
        
    
    

@views.route("/in_process/configuring", methods=["POST", "GET"])
def configuring():
    global machine 
    if request.method == "POST":
        if "stop" in request.form:
            return redirect("/in_process/finishing")
    
    session_id = session['session_id']
    gen_param = session['gen_param']
    gates_params = session['gates_params']
    machine.set_session_id(session_id)
    machine.set_general_sort_parameter(gen_param)
    machine.set_gates_params(gates_params)
    print("in conf in ")
    return redirect("/in_process/sorting")
    

@views.route("/in_process/sorting", methods=["POST", "GET"])
def sorting():
    global machine
    if request.method == "POST":
        if "stop" in request.form:
            return redirect("/in_process/finishing")
    machine.run()
    print("in sorting in process")
    return redirect("/in_process/finishing")

@views.route("/in_process/finishing")
def finishing():
    global machine 
    machine.finish_and_report()
    report = machine.get_report()
    print(report)
    
    session_date_time = datetime.strptime(report[1], "%Y-%m-%d - %H:%M")
    session_start_time = datetime.strptime(report[2], "%H:%M:%S")
    session_end_time = datetime.strptime(report[3], "%H:%M:%S")
    session_report = sessions(
        dateTime = session_date_time,
        start_time = session_start_time,
        end_time = session_end_time,
        total_objects = report[4],
        general_parameter = report[5],
        gate1_params = report[6],
        gate1_objects = report[7],
        gate2_params = report[8],
        gate2_objects = report[9],
        gate3_params = report[10],
        gate3_objects = report[11])
    
    db.session.add(session_report)
    db.session.commit()
    print("commited to db")
    session['finishing'] = True
    
    return redirect(f"/report/{report[0]}")

   
@views.route("/preview")
def cam_preview():
    directory = os.path.dirname(os.path.abspath(__file__))
    preview_image_path = os.path.join(directory, "static", "images" , "preview.jpg")
    with Picamera2() as cam:
        cam.start()
        cam.capture_file(preview_image_path)
        
    return render_template("preview.html")
