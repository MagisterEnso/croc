#!/usr/bin/env python3
"""
Example: Using croc with JSON output from Python
"""
import subprocess
import json
import sys

def monitor_croc_transfer(croc_command):
    """
    Monitor a croc transfer with JSON output
    
    Args:
        croc_command: List of command arguments, e.g. ['./croc-json-test', '--json', 'send', 'file.txt']
    
    Returns:
        Final status or raises exception on error
    """
    process = subprocess.Popen(
        croc_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffered
    )
    
    print(f"Started croc process (PID: {process.pid})")
    print("-" * 60)
    
    try:
        # Read JSON progress from stdout
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
                
            # Try to parse as JSON
            try:
                progress = json.loads(line)
                
                status = progress.get('status', 'unknown')
                
                if status == 'preparing':
                    print(f"📦 Preparing: {progress.get('message', '')}")
                    print(f"   Total size: {progress.get('bytes_total', 0)} bytes")
                    print(f"   Total files: {progress.get('total_files', 0)}")
                    
                elif status == 'transferring':
                    filename = progress.get('filename', 'unknown')
                    percent = progress.get('percent', 0)
                    bytes_sent = progress.get('bytes_sent', 0)
                    bytes_total = progress.get('bytes_total', 0)
                    file_num = progress.get('file_num', 0)
                    total_files = progress.get('total_files', 0)
                    
                    print(f"📤 Transferring [{file_num}/{total_files}]: {filename}")
                    print(f"   Progress: {percent:.1f}% ({bytes_sent}/{bytes_total} bytes)")
                    
                elif status == 'receiving':
                    print(f"📥 Receiving: {progress.get('message', '')}")
                    print(f"   Total size: {progress.get('bytes_total', 0)} bytes")
                    
                elif status == 'complete':
                    print(f"✅ Transfer complete!")
                    print(f"   Files transferred: {progress.get('total_files', 0)}")
                    return progress
                    
                elif status == 'error':
                    error_msg = progress.get('error', 'Unknown error')
                    print(f"❌ Error: {error_msg}", file=sys.stderr)
                    raise Exception(error_msg)
                    
                else:
                    print(f"ℹ️  Status: {status}")
                    if 'message' in progress:
                        print(f"   {progress['message']}")
                        
            except json.JSONDecodeError:
                # Not JSON, just regular output
                print(f"   {line}")
                
        # Wait for process to complete
        process.wait()
        
        if process.returncode != 0:
            raise Exception(f"croc exited with code {process.returncode}")
            
    except KeyboardInterrupt:
        print("\n⚠️  Transfer interrupted by user")
        process.terminate()
        raise
    
    return None


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        print("Usage examples:")
        print("  Send:    python test_json_output.py send <file>")
        print("  Receive: python test_json_output.py <code>")
        print()
        print("Note: Make sure to build croc-json-test first:")
        print("  go build -o croc-json-test")
        sys.exit(1)
    
    # Build croc command
    croc_cmd = ['./croc-json-test', '--json'] + sys.argv[1:]
    
    print(f"Running: {' '.join(croc_cmd)}")
    print()
    
    try:
        result = monitor_croc_transfer(croc_cmd)
        print("\n" + "=" * 60)
        print("Transfer completed successfully!")
        if result:
            print(f"Final result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"\n❌ Transfer failed: {e}", file=sys.stderr)
        sys.exit(1)
