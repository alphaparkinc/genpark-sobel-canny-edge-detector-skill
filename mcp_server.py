import sys
import json
from client import SobelCannyEdgeDetector

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-sobel-canny-edge-detector-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "detect_edges",
                    "description": "Perform Sobel/Canny edge detection on a 2D grayscale image matrix",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "image": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                            "low_threshold": {"type": "number", "default": 20.0},
                            "high_threshold": {"type": "number", "default": 50.0}
                        },
                        "required": ["image"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "detect_edges":
            detector = SobelCannyEdgeDetector(
                low_threshold=args.get("low_threshold", 20.0),
                high_threshold=args.get("high_threshold", 50.0)
            )
            data = detector.detect_edges(args.get("image", []))
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
