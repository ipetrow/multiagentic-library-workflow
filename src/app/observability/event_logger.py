import asyncio
from datetime import datetime
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

class EventLogger:

    def __init__(
        self,
        log_dir: Path,
        run_id: str | None = None
    ):
        self._run_id = run_id or str(uuid4())

        if not log_dir.exists():
            log_dir.mkdir(parents=True)
        self._path = log_dir / f"log_{self._run_id}.jsonl"

        self._lock = asyncio.Lock()

    async def log(
        self,
        event: str,
        agent: str | None = None,
        input_tokens: str | None = None,
        output_tokens: str | None = None,
        **data: Any
    ) -> None:

        now = datetime.now()

        record = {
            "run_id": self._run_id,
            "agent": agent,
            "event": event,
            "data": data
        }

        if event.endswith("_start"):
            record["start_at"] = now.isoformat()

        if event.endswith("_end"):
            record["end_at"] = now.isoformat()

        if input_tokens is not None:
            record["input_tokens"] = input_tokens

        if output_tokens is not None:
            record["output_tokens"] = output_tokens

        if input_tokens is not None and output_tokens is not None:
            record["total_tokens"] = input_tokens + output_tokens

        await self._write(record)

    async def _write(self, record: dict[str, Any]) -> None:
        try:
            line = json.dumps(record)

            async with self._lock:
                await asyncio.to_thread(
                    self._append_line,
                    line
                )
        except Exception as ex:
            print(f"Event loggins failed: {ex}")

    async def _append_line(self, line: str) -> None:
        with self._path.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
