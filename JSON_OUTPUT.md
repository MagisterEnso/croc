# JSON Output Feature for croc

## Overview

The `--json` flag enables machine-readable JSON output on stdout. Perfect for integration with other programs (e.g., Python, Node.js, etc.).

**Note:** When using `--stdout` to redirect file output, JSON will be sent to stderr instead to avoid conflicts.

## Usage

```bash
# Send with JSON output
croc --json send file.txt

# Receive with JSON output
CROC_SECRET=code-phrase croc --json
```

## JSON Format

All progress updates are output as individual JSON objects on stdout (one object per line), unless `--stdout` is used for file output, in which case JSON goes to stderr.

### Status Types

#### 1. `preparing` - Transfer preparation (Sender)

```json
{
  "status": "preparing",
  "message": "Sending 'file.txt' (1.5 MB)",
  "bytes_total": 1572864,
  "total_files": 1
}
```

#### 2. `receiving` - Receive preparation (Receiver)

```json
{
  "status": "receiving",
  "message": "Receiving 'file.txt' (1.5 MB)",
  "bytes_total": 1572864,
  "total_files": 1
}
```

#### 3. `transferring` - Active data transfer

```json
{
  "status": "transferring",
  "bytes_sent": 786432,
  "bytes_total": 1572864,
  "percent": 50.0,
  "filename": "file.txt",
  "file_num": 1,
  "total_files": 1
}
```

**Fields:**
- `bytes_sent`: Bytes transferred so far
- `bytes_total`: Total size of current file
- `percent`: Progress percentage (0-100)
- `filename`: Name of current file
- `file_num`: Number of current file (1-indexed)
- `total_files`: Total number of files

**Note:** Progress updates are sent periodically (every 50-100 chunks), not for every chunk.

#### 4. `complete` - Transfer successfully completed

```json
{
  "status": "complete",
  "message": "Transfer completed successfully",
  "total_files": 1
}
```

#### 5. `error` - Error occurred

```json
{
  "status": "error",
  "error": "connection refused"
}
```

## Python Integration

### Simple Example

```python
import subprocess
import json

def send_file_with_progress(filename):
    process = subprocess.Popen(
        ['croc', '--json', 'send', filename],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    for line in process.stdout:
        try:
            data = json.loads(line.strip())
            
            if data['status'] == 'transferring':
                percent = data.get('percent', 0)
                print(f"Progress: {percent:.1f}%")
            
            elif data['status'] == 'complete':
                print("Transfer complete!")
                break
                
            elif data['status'] == 'error':
                print(f"Error: {data['error']}")
                break
                
        except json.JSONDecodeError:
            # Ignore non-JSON output
            pass
    
    process.wait()
    return process.returncode == 0

# Usage
send_file_with_progress('mydocument.pdf')
```

### Advanced Example with GUI

```python
import subprocess
import json
import threading
from tkinter import ttk, Tk

class CrocTransferGUI:
    def __init__(self, root):
        self.root = root
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=20)
        self.label = ttk.Label(root, text="")
        self.label.pack()
    
    def send_file(self, filename):
        def monitor():
            process = subprocess.Popen(
                ['croc', '--json', 'send', filename],
                stdout=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                try:
                    data = json.loads(line.strip())
                    
                    if data['status'] == 'transferring':
                        percent = data.get('percent', 0)
                        self.progress['value'] = percent
                        self.label['text'] = f"{data['filename']}: {percent:.1f}%"
                        
                    elif data['status'] == 'complete':
                        self.progress['value'] = 100
                        self.label['text'] = "Transfer complete!"
                        
                except json.JSONDecodeError:
                    pass
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

# Usage
root = Tk()
gui = CrocTransferGUI(root)
gui.send_file('file.txt')
root.mainloop()
```

## Complete Test Script

A complete test script is included in `test_json_output.py`:

```bash
# Test sending
python test_json_output.py send testfile.txt

# Test receiving
python test_json_output.py <code-phrase>
```

## Notes

1. **stdout vs stderr**: JSON output goes to stdout by default. If `--stdout` is used to redirect file content, JSON will use stderr instead to avoid conflicts
2. **Line-based**: Each JSON object is a complete line
3. **Mixed with normal output**: When `--json` is active, `--quiet` should NOT be used as some status messages may be missing
4. **Error handling**: Always check both `status: "error"` and the exit code
5. **Performance**: JSON updates are not sent for every chunk but periodically (every 50-100 chunks)

## Combining with Other Flags

```bash
# JSON output with custom code
croc --json send --code my-secret file.txt

# JSON output via custom relay
croc --json --relay myrelay.example.com:9009 send file.txt

# JSON output without compression (faster)
croc --json --no-compress send largefile.iso
```

## Troubleshooting

### JSON Parsing Errors

If JSON parsing fails, the output might contain mixed content. Filter for lines starting with `{`:

```python
for line in process.stderr:
    line = line.strip()
    if line.startswith('{'):
        data = json.loads(line)
        # process JSON
```

### No Progress Updates

For very small files (<100KB), there may be few or no progress updates since they're only sent every N chunks.

### Check Exit Code

Even with `status: "complete"`, the exit code should be checked:

```python
process.wait()
if process.returncode != 0:
    print("Transfer failed!")
```
