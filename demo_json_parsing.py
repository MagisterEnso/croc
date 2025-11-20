#!/usr/bin/env python3
"""
Quick demo of croc JSON output parsing
"""
import subprocess
import json
import sys

def demo_json_parsing():
    """
    Parse the JSON output from croc --json send command
    This simulates what your Python program would do
    """
    
    print("=" * 70)
    print("CROC JSON OUTPUT DEMO")
    print("=" * 70)
    print()
    print("Starting croc with --json flag...")
    print("JSON events will be parsed and displayed below:")
    print("-" * 70)
    
    # Run croc with JSON output
    process = subprocess.Popen(
        ['./croc-json-test', '--json', 'send', 'testfile.txt'],
        env={'CROC_SECRET': 'demo-12345'},
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    json_events = []
    
    try:
        # Read from stderr where JSON is output
        for line in process.stderr:
            line = line.strip()
            
            # Check if it's JSON
            if line.startswith('{'):
                try:
                    event = json.loads(line)
                    json_events.append(event)
                    
                    # Pretty print the event
                    print(f"📊 JSON Event #{len(json_events)}:")
                    print(f"   Status: {event.get('status', 'unknown')}")
                    
                    for key, value in event.items():
                        if key != 'status':
                            print(f"   {key}: {value}")
                    print()
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON parsing error: {e}")
            else:
                # Regular output (not JSON)
                print(f"   {line}")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        process.terminate()
    
    print("-" * 70)
    print(f"\n✅ Captured {len(json_events)} JSON events")
    print("\nAll JSON events in raw format:")
    print(json.dumps(json_events, indent=2))
    
    return json_events


if __name__ == "__main__":
    print("This demo shows how croc --json output can be parsed in Python")
    print()
    
    # Note: This will wait for a receiver, so we'll timeout quickly
    print("Note: The sender will wait for a receiver.")
    print("Press Ctrl+C after seeing the JSON output to continue.")
    print()
    input("Press ENTER to start the demo...")
    print()
    
    try:
        events = demo_json_parsing()
        
        if events:
            print("\n" + "=" * 70)
            print("SUMMARY")
            print("=" * 70)
            for i, event in enumerate(events, 1):
                status = event.get('status', 'unknown')
                print(f"{i}. Status: {status}")
                if status == 'preparing':
                    print(f"   → Total bytes: {event.get('bytes_total', 0)}")
                    print(f"   → Total files: {event.get('total_files', 0)}")
                elif status == 'transferring':
                    print(f"   → Progress: {event.get('percent', 0):.1f}%")
                elif status == 'complete':
                    print(f"   → Files transferred: {event.get('total_files', 0)}")
                elif status == 'error':
                    print(f"   → Error: {event.get('error', 'unknown')}")
        
    except KeyboardInterrupt:
        print("\n\nDemo aborted by user.")
