import json
import argparse

def create_intro_screen():
    ascii_art = """
███████ ███████ ██████  ██████  ███████ ███████ ███████ ██ ███████
██      ██      ██   ██ ██   ██ ██      ██      ██      ██ ██
█████   ███████ ██████  ██████  █████   ███████ ███████ ██ █████
██           ██ ██      ██   ██ ██           ██      ██ ██ ██
███████ ███████ ██      ██   ██ ███████ ███████ ███████ ██ ██
    """
    intro_lines = [
        ascii_art,
        "",
        "                 ESP-BSP for ESP32-S3",
        "                  Espressif Systems",
        "",
        " Let's go through the steps of creating ESP-IDF project with ESP-BSP.",
        "",
    ]
    intro_events = []
    timestamp = 0.0
    typing_delay = 0.02

    for line in intro_lines:
        if line == ascii_art:
            for art_line in ascii_art.split('\n'):
                intro_events.append([round(timestamp, 6), "o", f"\u001b[32m{art_line}\u001b[0m\r\n"])
                timestamp += 0.05
        else:
            for char in line:
                intro_events.append([round(timestamp, 6), "o", char])
                timestamp += typing_delay
            intro_events.append([round(timestamp, 6), "o", "\r\n"])
            timestamp += 0.2
    timestamp += 0.5
    return intro_events, timestamp

def inject_intro(recording_path, output_path):
    with open(recording_path, 'r') as f:
        lines = f.readlines()
    
    header = json.loads(lines[0])
    events = [json.loads(line) for line in lines[1:]]
    
    intro_events, intro_duration = create_intro_screen()

    # Adjust timestamps for original events
    adjusted_events = []
    for event in events:
        event[0] = round(event[0] + intro_duration, 6)
        adjusted_events.append(event)

    new_events = intro_events + adjusted_events

    with open(output_path, 'w') as f:
        f.write(json.dumps(header) + '\n')
        for event in new_events:
            f.write(json.dumps(event, separators=(',', ':')) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Inject an intro screen into an Asciinema recording.")
    parser.add_argument('input_file', type=str, help='Path to the input Asciinema recording file.')
    parser.add_argument('output_file', type=str, help='Path to the output Asciinema recording file.')

    args = parser.parse_args()

    inject_intro(args.input_file, args.output_file)
    print(f"Intro screen added successfully to {args.output_file}.")

if __name__ == "__main__":
    main()
