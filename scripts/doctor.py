#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.install_optional_dependencies import (  # noqa: E402
    KNOWN_DEPENDENCIES,
    verify_git_checkout,
)
from src.local_skill_index import DEFAULT_SEARCH_ROOTS  # noqa: E402


def print_status(msg, is_error=False):
    if is_error:
        print(f"❌ {msg}")
    else:
        print(f"✅ {msg}")


def dependency_health(
    dep: dict,
    search_paths: list[Path],
    *,
    source_root: Path,
) -> dict:
    name = str(dep.get("name", ""))
    package_id = str(dep.get("package_id", ""))
    repo_name = package_id.split("/")[-1] if "/" in package_id else package_id
    found_path = None
    for base_path in search_paths:
        for possible_path in (
            base_path / name,
            base_path / repo_name,
        ):
            if (possible_path / "SKILL.md").exists():
                found_path = possible_path
                break
        if found_path is not None:
            break
    if found_path is None:
        return {"status": "missing", "path": None, "detail": "SKILL.md not found"}
    known = KNOWN_DEPENDENCIES.get(name)
    if known is None:
        return {
            "status": "unverified",
            "path": found_path,
            "detail": "no reviewed source metadata",
        }
    verification_target = (
        source_root / known["source_name"]
        if known.get("adapter")
        else found_path
    )
    verified, detail = verify_git_checkout(
        verification_target,
        known["repo"],
        dep.get("ref"),
    )
    return {
        "status": "verified" if verified else "unverified",
        "path": found_path,
        "detail": detail,
    }


def check_dependencies():
    manifest_path = Path(__file__).parent.parent / "skills_manifest.json"
    principles_path = Path(__file__).parent.parent / "GUYUE_PRINCIPLES.md"
    
    if not principles_path.exists():
        print_status("GUYUE_PRINCIPLES.md not found. Architecture broken.", is_error=True)
        sys.exit(1)
        
    if not manifest_path.exists():
        print_status("skills_manifest.json not found", is_error=True)
        sys.exit(1)

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        print_status("Invalid JSON in skills_manifest.json", is_error=True)
        sys.exit(1)

    deps = manifest.get("external_dependencies", [])
    if not deps:
        print_status("No external dependencies found. All good.")
        sys.exit(0)

    search_paths = [
        Path(raw_path).expanduser()
        for _, raw_path in DEFAULT_SEARCH_ROOTS
    ]
    
    # Also check if AGENT_SKILLS_PATH is set
    env_path = os.environ.get("AGENT_SKILLS_PATH") or os.environ.get("SKILLS_PATH")
    if env_path:
        search_paths.insert(0, Path(env_path))

    all_good = True
    missing_deps = []
    optional_missing = []
    optional_unverified = []
    source_root = Path(
        os.environ.get(
            "GUYUE_OPTIONAL_SOURCE_ROOT",
            "~/.cc-switch/skills/_sources",
        )
    ).expanduser()

    print("🩺 正在执行依赖健康探针 (Doctor)...")
    for dep in deps:
        name = dep.get("name")
        package_id = dep.get("package_id")
        command = dep.get("command")
        url = dep.get("url", "No URL provided")
        required = dep.get("required", True)
        health = dependency_health(dep, search_paths, source_root=source_root)
        if health["status"] == "verified":
            print_status(
                f"依赖正常: {name} ({package_id}) -> "
                f"verified at {health['path']}"
            )
        elif health["status"] == "unverified":
            message = (
                f"依赖存在但来源未验证: {name} ({package_id}) -> "
                f"{health['detail']}"
            )
            if required:
                print_status(message, is_error=True)
                missing_deps.append((name, url, command))
                all_good = False
            else:
                print(f"⚠️ {message}")
                optional_unverified.append((name, url, command))
        elif required:
            print_status(f"依赖缺失: {name} ({package_id})", is_error=True)
            missing_deps.append((name, url, command))
            all_good = False
        else:
            print(f"⚠️ 可选依赖未安装: {name} ({package_id})")
            optional_missing.append((name, url, command))

    print("\n--- 探针诊断报告 ---")
    if all_good:
        print("🎉 必需依赖均已就绪，环境健康！")
        if optional_missing or optional_unverified:
            print("\n--- 可选增强依赖（不阻塞本地验证）---")
            for name, url, cmd in optional_unverified:
                print(f"- **{name}** (来源: {url})")
                if cmd:
                    print(f"  可选来源修复命令: `{cmd}`")
            for name, url, cmd in optional_missing:
                print(f"- **{name}** (来源: {url})")
                if cmd:
                    print(f"  可选安装命令: `{cmd}`")
        sys.exit(0)
    else:
        print("> [!WARNING]")
        print("> ⚠️ 侦测到必要的外部技能缺失，无法继续受控执行。")
        print("> 请用户一键授权以下命令补齐依赖：\n")
        for name, url, cmd in missing_deps:
            print(f"- **{name}** (官方仓库: {url})")
            print(f"  安装命令: \n```bash\n{cmd}\n```\n")
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()
