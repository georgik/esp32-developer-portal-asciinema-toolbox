import json
import re

def consolidate_monitor_output(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read and parse the JSON metadata header
        header = json.loads(f.readline())
        events = []
        
        # Read the remaining lines (events)
        for line in f:
            events.append(json.loads(line))
    
    consolidated_events = []
    monitoring = False
    buffer = ""
    last_timestamp = 0

    for event in events:
        timestamp, event_type, content = event
        
        # Check if the monitor has started
        if "Executing action: monitor" in content:
            monitoring = True
        
        if monitoring:
            # Consolidate monitor output
            if re.match(r'^\[\d{3}\.\d+\]', content) or not content.strip():
                # Flush the buffer if the line looks like a new log entry or is empty
                if buffer:
                    consolidated_events.append([last_timestamp, "o", buffer])
                    buffer = ""
                last_timestamp = timestamp
                buffer += content
            else:
                buffer += content
        else:
            consolidated_events.append([timestamp, event_type, content])
    
    # Flush any remaining buffer content
    if buffer:
        consolidated_events.append([last_timestamp, "o", buffer])
    
    # Save the consolidated events
    with open(output_file, 'w') as f:
        # Write the JSON header
        json.dump(header, f)
        f.write("\n")
        # Write the consolidated events
        for event in consolidated_events:
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    input_file = 'session_replaced.cast'  # Replace with your input file name
    output_file = 'session_monitor.cast'  # Replace with your desired output file name
    consolidate_monitor_output(input_file, output_file)
