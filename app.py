from flask import Flask, render_template_string, request

app = Flask(__name__)

ERROR_DATABASE = {
    "F0E0": {"desc": "NO FAULT", "proc": "No action required."},
    "F0E2": {
        "desc": "OVER SUDS CONDITION DETECTED",
        "proc": "Check HE detergent usage and quantity. Check pressure hose connection for pinches or plugs. Check drive mechanism for friction.",
    },
    "F0E3": {
        "desc": "OVERLOAD CONDITION DETECTED",
        "proc": "Reduce load size. Check for mechanical friction between inner basket and tub. Check suspension and drive components.",
    },
    "F0E4": {
        "desc": "HIGH WATER TEMPERATURE - RINSE CYCLE",
        "proc": "Verify inlet hoses are connected correctly. If correct, test thermistor resistance (TEST #5).",
    },
    "F0E5": {
        "desc": "OFF BALANCE LOAD DETECTED",
        "proc": "Check suspension (basket should not bounce >1 time when pushed). Distribute clothing evenly.",
    },
    "F1E1": {"desc": "MAIN CONTROL FAULT", "proc": "Execute TEST #1 (Main Control)."},
    "F1E2": {
        "desc": "MOTOR CONTROL FAULT",
        "proc": "Execute TEST #3b (Drive System Motor).",
    },
    "F2E0": {
        "desc": "UI / MAIN CONTROL COMMUNICATION FAULT",
        "proc": "Disconnect power for 2 min. Check UI harness connection. Execute TEST #4 (Console & Indicators).",
    },
    "F2E1": {
        "desc": "STUCK KEY",
        "proc": "START key actuated >10 min. Execute TEST #4 (Console and Indicators).",
    },
    "F2E3": {
        "desc": "MISMATCH OF MAIN CONTROL & UI",
        "proc": "User Interface ID does not match Main Control. Execute TEST #4 (Console and Indicators).",
    },
    "F3E1": {
        "desc": "PRESSURE SENSOR FAULT",
        "proc": "Check pressure hose for pinches, kinks, or leaks. Execute TEST #6 (Water Level).",
    },
    "F3E2": {
        "desc": "INLET WATER TEMPERATURE FAULT",
        "proc": "Inlet Thermistor detected open or shorted. Execute TEST #5 (Temperature Thermistor).",
    },
    "F5E1": {
        "desc": "LID SWITCH FAULT",
        "proc": "Lid locked state detected while switch is open. Execute TEST #8 (Lid Lock).",
    },
    "F5E2": {
        "desc": "LID LOCK FAULT",
        "proc": "Lock failed to reach locked position or motor unpowered. Check for striker interference or buildup. Execute TEST #8.",
    },
    "F5E3": {
        "desc": "LID UNLOCK FAULT",
        "proc": "Lock failed to reach unlocked position. Check for striker interference. Execute TEST #8 (Lid Lock).",
    },
    "F5E4": {
        "desc": "LID NOT OPENED BETWEEN CYCLES",
        "proc": "User pressed START after consecutive cycles without opening lid. Open/close lid. Execute TEST #8.",
    },
    "F7E1": {
        "desc": "BASKET SPEED SENSOR FAULT",
        "proc": "Basket speed unknown or changing too fast. Check for locked rotor, free spin, and harness connections. Execute TEST #3a.",
    },
    "F7E5": {
        "desc": "SHIFTER FAULT",
        "proc": "Main control cannot determine shifter position. Check harness connections to motor and shifter. Execute TEST #3a.",
    },
    "F7E6": {
        "desc": "MOTOR FAULT",
        "proc": "Open CW or CCW circuit of the motor. Execute TEST #3b (Drive System - Motor).",
    },
    "F7E7": {
        "desc": "MOTOR UNABLE TO REACH TARGET RPM",
        "proc": "Target RPM not reached. Check for friction, weak motor/run capacitor, or off-balance load. Execute TEST #3b.",
    },
    "F8E1": {
        "desc": "LONG FILL",
        "proc": "Water level unchanged or filling >6 min. Check supply valves, screens, siphoning (<4.5 in pipe), and pressure hose. Execute TEST #2.",
    },
    "F8E3": {
        "desc": "OVERFLOW CONDITION",
        "proc": "Water level exceeds capacity. Check inlet valves and pressure hose connection. Execute TEST #2 & TEST #6.",
    },
    "F8E5": {
        "desc": "HOT, COLD REVERSED",
        "proc": "Hot and cold hoses reversed. Verify hose connections and thermistor resistance. Execute TEST #2 & TEST #5.",
    },
    "F8E6": {
        "desc": "NO FILL",
        "proc": "Water level unchanged. Verify supply is connected, check screens and pressure hose. Execute TEST #2.",
    },
    "F9E1": {
        "desc": "LONG DRAIN",
        "proc": "Water level unchanged after 10 min drain pump run. Check pump for clogs, standpipe height (>96 in), and pressure hose. Execute TEST #7.",
    },
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Washer Diagnostic Decoder</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 15px; background: #121212; color: #e0e0e0; }
        h2 { color: #4db6ac; text-align: center; margin-bottom: 20px; }
        .card { background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #333; }
        label { display: block; margin: 8px 0; font-size: 16px; }
        input[type="checkbox"] { transform: scale(1.3); margin-right: 10px; }
        input[type="text"] { width: 100%; padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #444; background: #2a2a2a; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00897b; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; margin-top: 10px; }
        .result { background: #263238; border-left: 5px solid #00b0ff; padding: 15px; margin-top: 20px; border-radius: 4px; }
        .code { font-size: 22px; font-weight: bold; color: #00e676; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h2>Washer Diagnostic Decoder</h2>
    
    <div class="card">
        <h3>Option 1: LED Selector</h3>
        <form method="POST">
            <p><strong>STATE 1: IN USE is ON</strong></p>
            <label><input type="checkbox" name="f_led" value="8"> Wash (8)</label>
            <label><input type="checkbox" name="f_led" value="4"> Rinse (4)</label>
            <label><input type="checkbox" name="f_led" value="2"> Final Spin (2)</label>
            <label><input type="checkbox" name="f_led" value="1"> Done (1)</label>
            
            <p><strong>STATE 2: IN USE is OFF</strong></p>
            <label><input type="checkbox" name="e_led" value="8"> Wash (8)</label>
            <label><input type="checkbox" name="e_led" value="4"> Rinse (4)</label>
            <label><input type="checkbox" name="e_led" value="2"> Final Spin (2)</label>
            <label><input type="checkbox" name="e_led" value="1"> Done (1)</label>
            
            <button type="submit" name="action" value="leds">Decode LEDs</button>
        </form>
    </div>

    <div class="card">
        <h3>Option 2: Direct Lookup</h3>
        <form method="POST">
            <input type="text" name="direct_code" placeholder="e.g. F5E2">
            <button type="submit" name="action" value="direct">Search Code</button>
        </form>
    </div>

    {% if result %}
    <div class="result">
        <div class="code">{{ result.code }}</div>
        <p><strong>Description:</strong> {{ result.desc }}</p>
        <p><strong>Procedure:</strong> {{ result.proc }}</p>
    </div>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        action = request.form.get("action")

        if action == "leds":
            f_sum = sum([int(x) for x in request.form.getlist("f_led")])
            e_sum = sum([int(x) for x in request.form.getlist("e_led")])
            code = f"F{f_sum}E{e_sum}"
        elif action == "direct":
            code = request.form.get("direct_code", "").strip().upper()
        else:
            code = ""

        if code in ERROR_DATABASE:
            result = {
                "code": code,
                "desc": ERROR_DATABASE[code]["desc"],
                "proc": ERROR_DATABASE[code]["proc"],
            }
        else:
            result = {
                "code": code,
                "desc": "NOT FOUND",
                "proc": "Code not recognized in database.",
            }

    return render_template_string(HTML_TEMPLATE, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)