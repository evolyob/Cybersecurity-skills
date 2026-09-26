#!/usr/bin/env python3
"""ViewFile Safety Guard: Binary block + smart overlap chunk planner."""
import sys
import json
from pathlib import Path

MAX_VIEW_LINES = 800
STEP = 750  # 800-line window with 50-line boundary overlap
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".pdf", ".mp4"}

def count_lines(p: Path) -> int:
    try:
        with open(p, "rb") as f:
            return sum(chunk.count(b"\n") for chunk in iter(lambda: f.read(65536), b""))
    except Exception:
        return 0

def main():
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            print(json.dumps({"decision": "allow"})); return

        args = json.loads(raw).get("toolCall", {}).get("args", {})
        target = Path(args.get("AbsolutePath") or args.get("file_path") or "")
        if not target.is_file() or target.suffix.lower() in MEDIA_EXTS:
            print(json.dumps({"decision": "allow"})); return

        # 1. 二進制阻斷
        with open(target, "rb") as f:
            if b"\x00" in f.read(512):
                print(json.dumps({"decision": "deny", "reason": f"【二進制阻斷】{target.name} 為非文字檔案。"}, ensure_ascii=False))
                return

        # 2. 已指定行數範圍
        start, end = args.get("StartLine"), args.get("EndLine")
        if start is not None and end is not None:
            if (int(end) - int(start) + 1) > MAX_VIEW_LINES:
                print(json.dumps({"decision": "deny", "reason": f"【跨度超限】單次最多讀取 {MAX_VIEW_LINES} 行。"}, ensure_ascii=False))
                return
            print(json.dumps({"decision": "allow"})); return

        # 3. 未指定行數且超過 800 行時，輸出重疊分段規劃
        total = count_lines(target)
        if total > MAX_VIEW_LINES:
            batches = [f"批次 {i+1} (StartLine: {s}, EndLine: {min(s + MAX_VIEW_LINES - 1, total)})"
                       for i, s in enumerate(range(1, total + 1, STEP))][:4]
            plan = "；".join(batches) + ("..." if total > STEP * 4 else "")
            reason = f"【防截斷分段建議】{target.name} 共 {total} 行。請依序分段閱讀：{plan}。"
            print(json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False))
            return

    except Exception:
        pass

    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
