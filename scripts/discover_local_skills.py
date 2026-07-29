#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.paths import discovery_cache_file, ensure_private_directory  # noqa: E402
from src.local_skill_index import build_local_skill_index  # noqa: E402

def write_index_atomic(output_file: Path, index: dict) -> None:
    ensure_private_directory(output_file.parent)
    temporary = output_file.with_name(f".{output_file.name}.{os.getpid()}.tmp")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(output_file)
        output_file.chmod(0o600)
    finally:
        temporary.unlink(missing_ok=True)


def discover(output_file: Path | None = None):
    index = build_local_skill_index()
    destination = output_file or discovery_cache_file()
    write_index_atomic(destination, index)

    print(
        f"✅ 成功发现 {len(index['skills'])} 个本地技能并写入可重建缓存: "
        f"{destination}"
    )
    return destination

if __name__ == "__main__":
    discover()
