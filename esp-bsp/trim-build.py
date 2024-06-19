import json

def process_asciinema_recording(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read and parse the JSON metadata header
        header = json.loads(f.readline())
        events = []
        
        # Read the remaining lines (events)
        for line in f:
            events.append(json.loads(line))
    
    filtered_events = []
    build_counter = 0
    accumulated_time = 0
    skip_patterns = [
        "warning: unknown kconfig symbol",
        "This driver is an old"
    ]
    flash_patterns = ["Writing at 0x"]
    flash_keep_percentages = {"25", "50", "75", "100"}

    for event in events:
        timestamp, event_type, content = event

        # Skip lines with specific unwanted strings
        if any(pattern in content for pattern in skip_patterns):
            continue

        # Detect build lines based on the pattern
        if "/989]" in content:
            build_counter += 1
            if build_counter % 100 != 0:
                continue
            # Set the interval between kept build lines to 200 ms
            accumulated_time += 0.2
        elif any(pattern in content for pattern in flash_patterns):
            # Skip most of the flash progress lines
            if not any(f"({percentage} %" in content for percentage in flash_keep_percentages):
                continue
            # Adjust the interval to be shorter for flash progress lines
            accumulated_time += 0.5
        else:
            if filtered_events:
                accumulated_time += (timestamp - filtered_events[-1][0])

        new_timestamp = round(accumulated_time, 6)
        filtered_events.append([new_timestamp, event_type, content])

    # Save the processed events
    with open(output_file, 'w') as f:
        # Write the JSON header
        json.dump(header, f)
        f.write("\n")
        # Write the filtered events
        for event in filtered_events:
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    input_file = 'session.cast'  # Replace with your input file name
    output_file = 'session_trimmed.cast'  # Replace with your desired output file name
    process_asciinema_recording(input_file, output_file)
