import sys


def get_binary_sum(prompt_text: str) -> int:
    """Prompts the user for lit LEDs and calculates their binary sum."""
    print(f"\n--- {prompt_text} ---")
    print("Select lit LEDs by entering their numbers separated by spaces:")
    print("  [8] Wash / Soak")
    print("  [4] Rinse")
    print("  [2] Final Spin")
    print("  [1] Done")
    print("  [0] None")

    while True:
        try:
            raw_input = input("Enter values (e.g., '4 1' or '0'): ").strip()
            if not raw_input:
                continue

            choices = [int(x) for x in raw_input.split()]

            if 0 in choices:
                if len(choices) > 1:
                    print("Error: Cannot select '0' along with other numbers.")
                    continue
                return 0

            valid_weights = {8, 4, 2, 1}
            if not all(c in valid_weights for c in choices):
                print("Error: Invalid selection. Only use numbers 8, 4, 2, 1, or 0.")
                continue

            if len(choices) != len(set(choices)):
                print("Error: Duplicate selections detected.")
                continue

            return sum(choices)

        except ValueError:
            print("Error: Invalid input. Please enter numbers separated by spaces.")


def decode_error_database() -> dict:
    """Returns the master dictionary of diagnostic codes from the tech sheet."""
    return {
        "F0E0": {
            "description": "NO FAULT",
            "procedure": "No action required.",
        },
        "F0E2": {
            "description": "OVER SUDS CONDITION DETECTED",
            "procedure": (
                "Check HE detergent usage and quantity. Check pressure hose connection from tub to sensor for pinches or plugs. Check drive mechanism for mechanical friction."
            ),
        },
        "F0E3": {
            "description": "OVERLOAD CONDITION DETECTED",
            "procedure": (
                "Reduce load size. Check for mechanical friction between inner basket and tub. Check suspension and drive components."
            ),
        },
        "F0E4": {
            "description": "HIGH WATER TEMPERATURE - RINSE CYCLE",
            "procedure": (
                "Verify inlet hoses are connected correctly (Hot/Cold not reversed). If hoses are correct, test thermistor resistance (TEST #5)."
            ),
        },
        "F0E5": {
            "description": "OFF BALANCE LOAD DETECTED",
            "procedure": (
                "Check suspension (basket should not bounce >1 time when pushed). Distribute clothing evenly."
            ),
        },
        "F1E1": {
            "description": "MAIN CONTROL FAULT",
            "procedure": "Execute TEST #1 (Main Control).",
        },
        "F1E2": {
            "description": "MOTOR CONTROL FAULT",
            "procedure": "Execute TEST #3b (Drive System Motor).",
        },
        "F2E0": {
            "description": "UI / MAIN CONTROL COMMUNICATION FAULT",
            "procedure": (
                "Disconnect power for 2 min. Check UI harness connection. Execute TEST #4 (Console & Indicators)."
            ),
        },
        "F2E1": {
            "description": "STUCK KEY",
            "procedure": (
                "START key actuated for >10 consecutive minutes. Execute TEST #4 (Console and Indicators)."
            ),
        },
        "F2E3": {
            "description": "MISMATCH OF MAIN CONTROL & UI",
            "procedure": (
                "User Interface ID does not match Main Control. Execute TEST #4 (Console and Indicators)."
            ),
        },
        "F3E1": {
            "description": "PRESSURE SENSOR FAULT",
            "procedure": (
                "Check pressure hose for pinches, kinks, or leaks. Execute TEST #6 (Water Level)."
            ),
        },
        "F3E2": {
            "description": "INLET WATER TEMPERATURE FAULT",
            "procedure": (
                "Inlet Thermistor detected open or shorted. Execute TEST #5 (Temperature Thermistor)."
            ),
        },
        "F5E1": {
            "description": "LID SWITCH FAULT",
            "procedure": (
                "Lid locked state detected while switch is open. Execute TEST #8 (Lid Lock)."
            ),
        },
        "F5E2": {
            "description": "LID LOCK FAULT",
            "procedure": (
                "Lock failed to reach locked position or motor unpowered. Check for striker interference or wash media buildup. Execute TEST #8."
            ),
        },
        "F5E3": {
            "description": "LID UNLOCK FAULT",
            "procedure": (
                "Lock failed to reach unlocked position. Check for striker interference. Execute TEST #8 (Lid Lock)."
            ),
        },
        "F5E4": {
            "description": "LID NOT OPENED BETWEEN CYCLES",
            "procedure": (
                "User pressed START after consecutive cycles without opening lid. Open/close lid. Execute TEST #8."
            ),
        },
        "F7E1": {
            "description": "BASKET SPEED SENSOR FAULT",
            "procedure": (
                "Basket speed unknown or changing too fast. Check for locked rotor, free spin, and harness connections to motor/shifter. Execute TEST #3a."
            ),
        },
        "F7E5": {
            "description": "SHIFTER FAULT",
            "procedure": (
                "Main control cannot determine shifter position. Check harness connections to motor and shifter. Execute TEST #3a."
            ),
        },
        "F7E6": {
            "description": "MOTOR FAULT",
            "procedure": (
                "Open CW or CCW circuit of the motor. Execute TEST #3b (Drive System - Motor)."
            ),
        },
        "F7E7": {
            "description": "MOTOR UNABLE TO REACH TARGET RPM",
            "procedure": (
                "Basket speed sensor detected target RPM was not reached. Check for friction, weak motor/run capacitor, or off-balance load. Execute TEST #3b."
            ),
        },
        "F8E1": {
            "description": "LONG FILL",
            "procedure": (
                "Water level unchanged or filling >6 min. Check supply valves, clogged screens, siphoning (hose >4.5 in pipe), and pressure hose. Execute TEST #2."
            ),
        },
        "F8E3": {
            "description": "OVERFLOW CONDITION",
            "procedure": (
                "Water level exceeds capacity. Check inlet valves and pressure hose connection. Execute TEST #2 & TEST #6."
            ),
        },
        "F8E5": {
            "description": "HOT, COLD REVERSED",
            "procedure": (
                "Hot and cold hoses reversed. Verify hose connections and thermistor resistance. Execute TEST #2 & TEST #5."
            ),
        },
        "F8E6": {
            "description": "NO FILL",
            "procedure": (
                "Water level unchanged for a set duration. Verify supply is connected, check for clogged screens and pressure hose. Execute TEST #2."
            ),
        },
        "F9E1": {
            "description": "LONG DRAIN",
            "procedure": (
                "Water level unchanged after 10 min drain pump run. Check pump for clogs, standpipe height (>96 in), and pressure hose. Execute TEST #7."
            ),
        },
    }


def lookup_code(code: str, db: dict) -> None:
    """Prints error details from the database."""
    code = code.upper().strip()
    if code in db:
        print(f"\n==========================================")
        print(f" FAULT/ERROR CODE: {code}")
        print(f"==========================================")
        print(f"Description: {db[code]['description']}")
        print(f"Procedure:   {db[code]['procedure']}")
        print(f"==========================================\n")
    else:
        print(f"\n[!] Code {code} was not found in the tech sheet database.\n")


def main():
    db = decode_error_database()

    while True:
        print("\n--- MAYTAG / WHIRLPOOL WASHER DIAGNOSTIC DECODER ---")
        print("1. Decode by selecting Lit LEDs")
        print("2. Lookup Code directly (e.g., F5E2)")
        print("3. Exit")

        choice = input("\nSelect mode (1-3): ").strip()

        if choice == "1":
            f_val = get_binary_sum("STATE 1: IN USE LED is ON (Fault Digit)")
            e_val = get_binary_sum("STATE 2: IN USE LED is OFF (Error Digit)")
            calculated_code = f"F{f_val}E{e_val}"
            lookup_code(calculated_code, db)

        elif choice == "2":
            direct_code = input(
                "\nEnter 4-character Code (e.g., F5E2): "
            ).strip()
            lookup_code(direct_code, db)

        elif choice == "3":
            sys.exit(0)

        else:
            print("Invalid selection. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()