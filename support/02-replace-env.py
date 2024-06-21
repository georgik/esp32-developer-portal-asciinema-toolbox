import json
import re

def transform_asciinema_recording(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read and parse the JSON metadata header
        header = json.loads(f.readline())
        events = []

        # Read the remaining lines (events)
        for line in f:
            events.append(json.loads(line))

    transformed_events = []

    home_pattern = re.compile(r"/Users/georgik")
    project_pattern = re.compile(r"/Users/georgik/projects/asciinema-recording")
    prompt_pattern = re.compile(r"bash-...\$ ")

    for event in events:
        timestamp, event_type, content = event

        # Replace user home directory
        content = home_pattern.sub("/Users/esp", content)

        # Replace project directory
        content = project_pattern.sub("/Users/esp/projects", content)

        # Replace prompt
        content = prompt_pattern.sub(
            "\033[32mesp@developer.espressif.com\033[0m$ ", content
        )

        transformed_events.append([timestamp, event_type, content])

    # Save the transformed events
    with open(output_file, 'w') as f:
        # Write the JSON header
        json.dump(header, f)
        f.write("\n")
        # Write the transformed events
        for event in transformed_events:
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    input_file = 'session_monitor.cast'  # Replace with your input file name
    output_file = 'session_replaced.cast'  # Replace with your desired output file name
    transform_asciinema_recording(input_file, output_file)
