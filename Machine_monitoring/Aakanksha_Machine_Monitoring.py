
def analyze_temperature(readings, temperature_limits):
    results = []
    summary = {}

    for reading in readings:
        if "machine_id" not in reading or "timestamp" not in reading or "temperature_c" not in reading:
          print("Invalid reading:", reading)
          continue

        machine_id = reading["machine_id"]
        temperature = reading["temperature_c"]

        if machine_id not in temperature_limits:
            print("Unknown machine:", machine_id)
            continue

        if temperature is None:
            print("Missing temperature:", reading)
            continue

        try:
            temperature = float(temperature)
        except (ValueError, TypeError):
            print("Invalid temperature:", reading)
            continue

        limit = temperature_limits[machine_id]

        if temperature <= limit:
            status = "NORMAL"
        elif temperature <= limit * 1.10:
            status = "WARNING"
        else:
            status = "CRITICAL"

        result = {
            "machine_id": machine_id,
            "timestamp": reading["timestamp"],
            "temperature_c": temperature,
            "configured_limit": limit,
            "status": status
        }

        results.append(result)
        print(result)

        if machine_id not in summary:
         summary[machine_id] = [0, 0, 0, temperature]

        summary[machine_id][0] += 1
        summary[machine_id][1] += temperature

        if status == "CRITICAL":
            summary[machine_id][2] += 1

    for machine_id in summary:
        count = summary[machine_id][0]
        total = summary[machine_id][1]

        summary[machine_id] = {
            "valid_readings": count,
            "average_temperature": round(total / count, 1),
            "critical_count": summary[machine_id][2]
        }

    print("\nMACHINE SUMMARY")

    for machine_id, details in summary.items():
        print("Machine:", machine_id, details)

    return results, summary


temperature_limits = {
    101: 80.0,
    102: 75.0,
    103: 65.0
}

readings = [
    {"machine_id": 101, "timestamp": "09:00", "temperature_c": 78.0},
    {"machine_id": 101, "timestamp": "09:15", "temperature_c": 84.0},
    {"machine_id": 101, "timestamp": "09:30", "temperature_c": 90.0},
    {"machine_id": 102, "timestamp": "09:00", "temperature_c": 77.0},
    {"machine_id": 103, "timestamp": "09:00", "temperature_c": 64.0},
    {"machine_id": 999, "timestamp": "09:15", "temperature_c": 70.0},
    {"machine_id": 101, "timestamp": "09:45", "temperature_c": None},
    {"machine_id": 102, "timestamp": "09:45", "temperature_c": None},
    {"machine_id": 103, "timestamp": "10:00", "temperature_c": "abcd"}
]

results, summary = analyze_temperature(readings, temperature_limits)
