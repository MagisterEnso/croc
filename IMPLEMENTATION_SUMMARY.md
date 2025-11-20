# Summary: JSON Output Feature for croc

## ⚠️ Implementation Status: Incomplete / Experimental

**This implementation has known issues and is not recommended for production use.**

### Problems Encountered

1. **Code invasiveness**: The implementation required adding `if !c.Options.JSONOutput` checks throughout the codebase, making it harder to maintain
2. **Edge cases**: Normal operation (without `--json` flag) was broken by progressbar visibility changes
3. **Architectural issues**: A cleaner approach would require:
   - A separate UI abstraction layer
   - Writer interfaces that can switch between normal and JSON modes
   - Better separation of concerns between business logic and output formatting

### Lessons Learned

- Suppressing UI elements (text messages, progress bars, etc.) for a "clean" JSON mode requires touching many parts of the code
- Without a proper abstraction layer, this type of feature becomes maintenance-heavy
- The original codebase wasn't designed with programmatic output in mind, making retrofitting difficult

**This branch is published as documentation of what was attempted and the challenges encountered.**

---

## What Was Implemented

A new `--json` flag that outputs machine-readable JSON events to stderr. Perfect for integrating croc into Python processes or other programs.

## Modified Files

1. **src/croc/croc.go**
   - Added `JSONOutput` option to Options structure
   - Defined `JSONProgress` structure for JSON events
   - Implemented `emitJSON()` method for outputting JSON
   - Added JSON events at key points:
     - Preparation (preparing)
     - Receiving (receiving)
     - Transfer start (transferring)
     - Progress updates during transfer
     - Successful completion (complete)
     - Errors (error)

2. **src/cli/cli.go**
   - Added `--json` flag to global flags
   - Passed JSONOutput option to croc.New() (send & receive)

## JSON Event Types

### 1. preparing
```json
{
  "status": "preparing",
  "message": "Sending 'file.txt' (1.5 MB)",
  "bytes_total": 1572864,
  "total_files": 1
}
```

### 2. receiving
```json
{
  "status": "receiving",
  "message": "Receiving 'file.txt' (1.5 MB)",
  "bytes_total": 1572864,
  "total_files": 1
}
```

### 3. transferring
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

### 4. complete
```json
{
  "status": "complete",
  "message": "Transfer completed successfully",
  "total_files": 1
}
```

### 5. error
```json
{
  "status": "error",
  "error": "connection refused"
}
```

## Usage

### Sending
```bash
CROC_SECRET=my-code croc --json send file.txt
```

### Receiving
```bash
CROC_SECRET=my-code croc --json
```

### Python Integration
```python
import subprocess
import json

process = subprocess.Popen(
    ['croc', '--json', 'send', 'file.txt'],
    env={'CROC_SECRET': 'my-code'},
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1
)

for line in process.stdout:
    if line.strip().startswith('{'):
        event = json.loads(line)
        
        if event['status'] == 'transferring':
            print(f"Progress: {event['percent']:.1f}%")
        
        elif event['status'] == 'complete':
            print("Transfer complete!")
            break
        
        elif event['status'] == 'error':
            print(f"Error: {event['error']}")
            break
```

## Test Files

1. **test_json_output.py** - Complete example with nice output
2. **demo_json_parsing.py** - Quick JSON parsing demo
3. **JSON_OUTPUT.md** - Comprehensive documentation

## Building

```bash
# Standard build
go build -o croc-json-test

# All platforms
./build-all.sh
```

## Testing

```bash
# Simple test
CROC_SECRET=test ./croc-json-test --json send testfile.txt

# With Python script
python test_json_output.py send testfile.txt
```

## Advantages Over Output Parsing

1. **Reliable**: JSON is structured and easy to parse
2. **Complete**: All relevant information in each event
3. **Extensible**: New fields can be added without breaking existing code
4. **Machine-readable**: No regex or string parsing needed
5. **Separated**: JSON on stderr, file output on stdout possible

## Notes

- JSON events are output to **stdout** (or stderr when `--stdout` is used for file output)
- Progress updates occur **periodically** (every 50-100 chunks), not for every chunk
- For small files there may be only a few progress updates
- `--json` can be combined with all other flags
- Works for both sender and receiver
