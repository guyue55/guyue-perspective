#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "skills_manifest.json"

DEFAULT_SKILL_ROOTS = [
    "~/.cc-switch/skills",
    "~/.codex/skills",
    "~/.gemini/config/skills",
    "~/.cursor/skills",
]

KNOWN_DEPENDENCIES = {
    "luban": {
        "repo": "https://github.com/LearnPrompt/luban-skill",
        "source_name": "luban",
        "skill_subpath": "skills/luban",
        "risk": "red",
        "risk_note": "contains maintenance shell tools that use deletion commands",
    },
    "huashu-nuwa": {
        "repo": "https://github.com/alchaincyf/nuwa-skill",
        "source_name": "nuwa-skill",
        "skill_subpath": ".",
        "risk": "yellow",
        "risk_note": "contains external links in documentation",
    },
    "superpowers": {
        "repo": "https://github.com/obra/superpowers",
        "source_name": "superpowers",
        "adapter": True,
        "risk": "adapter",
        "risk_note": "root checkout is a suite; child skills live under skills/",
    },
    "taste-skill": {
        "repo": "https://github.com/Leonxlnx/taste-skill",
        "source_name": "taste-skill",
        "skill_subpath": "skills/taste-skill",
        "risk": "yellow",
        "risk_note": "contains external links in documentation",
    },
    "ui-ux-pro-max": {
        "repo": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        "source_name": "ui-ux-pro-max",
        "skill_subpath": ".claude/skills/ui-ux-pro-max",
        "risk": "yellow",
        "risk_note": "contains external links in documentation",
    },
    "gsap-core": {
        "repo": "https://github.com/greensock/gsap-skills",
        "source_name": "gsap-core",
        "skill_subpath": "skills/gsap-core",
        "risk": "yellow",
        "risk_note": "contains external links in documentation",
    },
    "find-skills": {
        "repo": "https://github.com/vercel-labs/skills",
        "source_name": "vercel-skills",
        "skill_subpath": "skills/find-skills",
        "risk": "yellow",
        "risk_note": "contains external links in documentation",
    },
    "headroom": {
        "repo": "https://github.com/chopratejas/headroom",
        "source_name": "headroom",
        "adapter": True,
        "risk": "adapter",
        "risk_note": "root checkout is a project, not a single Skill directory",
    },
    "ponytail": {
        "repo": "https://github.com/DietrichGebert/ponytail",
        "source_name": "ponytail",
        "skill_subpath": "skills/ponytail",
        "risk": "green",
        "risk_note": "skill subdirectory passed local heuristic preflight",
    },
    "skillspector": {
        "repo": "https://github.com/NVIDIA/SkillSpector",
        "source_name": "skillspector",
        "adapter": True,
        "risk": "adapter",
        "risk_note": "root checkout is a project, not a single Skill directory",
    },
}

ADAPTER_TEMPLATE = """---
name: {name}
description: Adapter for the local {name} source checkout. Use only when the user explicitly asks about this optional dependency; inspect the source README before suggesting commands.
---

# {title} Adapter

This is a local adapter entry for the checked-out `{source_name}` project.

Source checkout:

`~/.cc-switch/skills/_sources/{source_name}`

Before using it, read the source README and relevant docs. Do not run install scripts, hooks, networked commands, or project CLIs unless the user explicitly authorizes that specific action.
"""


def load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def skill_roots():
    roots = []
    for raw in DEFAULT_SKILL_ROOTS:
        path = Path(raw).expanduser()
        if path not in roots:
            roots.append(path)
    return roots


def external_dependencies(manifest):
    return [dep for dep in manifest.get("external_dependencies", []) if not dep.get("required", False)]


def dependency_aliases(dep):
    aliases = [dep.get("name", "")]
    package_id = dep.get("package_id", "")
    if "/" in package_id:
        aliases.append(package_id.rsplit("/", 1)[-1])
    known = KNOWN_DEPENDENCIES.get(dep.get("name", ""))
    if known:
        aliases.append(known["source_name"])
    return [item for idx, item in enumerate(aliases) if item and item not in aliases[:idx]]


def find_existing_skill(dep):
    matches = []
    for root in skill_roots():
        for alias in dependency_aliases(dep):
            skill_file = root / alias / "SKILL.md"
            if skill_file.exists():
                matches.append(root / alias)
    return matches


def normalize_repo_url(url):
    value = str(url).strip()
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.removeprefix("git@github.com:")
    return value.removesuffix(".git").rstrip("/")


def verify_git_checkout(path, expected_repo, expected_ref):
    """Verify that an existing Skill resolves inside the reviewed checkout."""
    if not expected_ref:
        return False, "manifest ref is missing"
    if not path.exists():
        return False, f"reviewed source checkout is missing: {path}"
    root_result = run(["git", "rev-parse", "--show-toplevel"], cwd=path, capture=True)
    if root_result.returncode != 0:
        return False, "existing Skill is not inside a Git checkout"
    git_root = Path(root_result.stdout.strip()).resolve()
    try:
        path.resolve().relative_to(git_root)
    except ValueError:
        return False, "existing Skill resolves outside its Git checkout"
    head_result = run(["git", "rev-parse", "HEAD"], cwd=git_root, capture=True)
    if head_result.returncode != 0 or head_result.stdout.strip() != expected_ref:
        actual = head_result.stdout.strip() or "<unknown>"
        return False, f"checkout HEAD {actual} does not match reviewed ref {expected_ref}"
    remote_result = run(["git", "remote", "get-url", "origin"], cwd=git_root, capture=True)
    if remote_result.returncode != 0:
        return False, "checkout has no verifiable origin remote"
    actual_repo = normalize_repo_url(remote_result.stdout)
    if actual_repo != normalize_repo_url(expected_repo):
        return False, f"checkout origin {actual_repo} does not match {normalize_repo_url(expected_repo)}"
    return True, f"verified {expected_ref} from {actual_repo}"


def skill_frontmatter_name(target):
    skill_file = target / "SKILL.md"
    if not skill_file.exists():
        return None
    content = skill_file.read_text(encoding="utf-8", errors="ignore")
    if not content.startswith("---"):
        return None
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return None
    frontmatter = yaml.safe_load(content[3:end_idx]) or {}
    value = frontmatter.get("name")
    return str(value).strip() if value else None


def skill_aliases(name, target):
    aliases = [name]
    frontmatter_name = skill_frontmatter_name(target)
    if frontmatter_name:
        aliases.append(frontmatter_name)
    return [item for idx, item in enumerate(aliases) if item and item not in aliases[:idx]]


def desired_skill_links(name):
    cc_root = Path("~/.cc-switch/skills").expanduser()
    codex_root = Path("~/.codex/skills").expanduser()
    return [cc_root / name, codex_root / name]


def missing_skill_links(names):
    paths = []
    for name in names:
        paths.extend(path for path in desired_skill_links(name) if not (path / "SKILL.md").exists())
    return paths


def run(cmd, cwd=None, capture=False):
    if capture:
        return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return subprocess.run(cmd, cwd=cwd, check=True)


def clone_or_update(repo, ref, destination, dry_run):
    if destination.exists():
        if not ref:
            return "missing_ref"
        result = run(["git", "rev-parse", "HEAD"], cwd=destination, capture=True)
        if result.returncode != 0 or result.stdout.strip() != ref:
            return "ref_mismatch"
        return "exists"
    if dry_run:
        return "would_clone"
    if not ref:
        return "missing_ref"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="guyue-skill-source-") as temp_dir:
        staged = Path(temp_dir) / destination.name
        staged.mkdir()
        run(["git", "init", "--quiet"], cwd=staged)
        run(["git", "remote", "add", "origin", repo], cwd=staged)
        run(["git", "fetch", "--quiet", "--depth", "1", "origin", ref], cwd=staged)
        run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=staged)
        resolved = run(["git", "rev-parse", "HEAD"], cwd=staged, capture=True)
        if resolved.returncode != 0 or resolved.stdout.strip() != ref:
            raise RuntimeError(f"fetched ref mismatch for {repo}: expected {ref}")
        shutil.move(str(staged), str(destination))
    return "cloned"


def scan_target(target):
    proc = run(["python3", "scripts/run_security_scan.py", str(target)], cwd=REPO_ROOT, capture=True)
    output = proc.stdout
    if "状态: Green" in output:
        return "green", output
    if "状态: Yellow" in output:
        return "yellow", output
    if "状态: Red" in output:
        return "red", output
    return "unknown", output


def write_adapter(adapter_dir, dep_name, source_name, dry_run):
    if dry_run:
        return
    adapter_dir.mkdir(parents=True, exist_ok=True)
    content = ADAPTER_TEMPLATE.format(
        name=dep_name,
        title=dep_name,
        source_name=source_name,
    )
    (adapter_dir / "SKILL.md").write_text(content, encoding="utf-8")


def link_skill(name, target, dry_run):
    cc_root = Path("~/.cc-switch/skills").expanduser()
    codex_root = Path("~/.codex/skills").expanduser()
    cc_link = cc_root / name
    codex_link = codex_root / name

    if dry_run:
        return

    cc_root.mkdir(parents=True, exist_ok=True)
    codex_root.mkdir(parents=True, exist_ok=True)

    if cc_link.resolve() != target.resolve():
        if cc_link.is_symlink():
            cc_link.unlink()
        if not cc_link.exists():
            cc_link.symlink_to(target)

    if codex_link.resolve() != cc_link.resolve():
        if codex_link.is_symlink():
            codex_link.unlink()
        if not codex_link.exists():
            codex_link.symlink_to(cc_link)


def sync_existing_skill_links(name, target, dry_run):
    aliases = skill_aliases(name, target)
    missing = missing_skill_links(aliases)
    if not missing:
        print_plan_row(name, "skip", f"already installed at {target}")
        return {"name": name, "status": "already_installed"}

    detail = "missing links: " + ", ".join(str(path) for path in missing)
    if dry_run:
        print_plan_row(name, "would_sync", detail)
        return {"name": name, "status": "would_sync"}

    for alias in aliases:
        link_skill(alias, target, dry_run=False)
    print_plan_row(name, "synced", detail)
    return {"name": name, "status": "synced"}


def link_new_skill(name, target, dry_run):
    cc_root = Path("~/.cc-switch/skills").expanduser()
    codex_root = Path("~/.codex/skills").expanduser()

    if dry_run:
        return

    cc_root.mkdir(parents=True, exist_ok=True)
    codex_root.mkdir(parents=True, exist_ok=True)

    for alias in skill_aliases(name, target):
        cc_link = cc_root / alias
        codex_link = codex_root / alias

        if cc_link.is_symlink():
            cc_link.unlink()
        if not cc_link.exists():
            cc_link.symlink_to(target)

        if codex_link.is_symlink():
            codex_link.unlink()
        if not codex_link.exists():
            codex_link.symlink_to(cc_link)


def print_plan_row(name, status, detail):
    print(f"- {name}: {status} — {detail}")


def install_dependency(dep, source_root, dry_run, force):
    name = dep["name"]
    known = KNOWN_DEPENDENCIES.get(name)
    existing = find_existing_skill(dep)
    if existing:
        if not known:
            print_plan_row(name, "blocked", "existing Skill has no reviewed source metadata")
            return {"name": name, "status": "blocked", "scan": "unverified_source"}
        verification_target = source_root / known["source_name"] if known.get("adapter") else existing[0]
        verified, detail = verify_git_checkout(
            verification_target,
            known["repo"],
            dep.get("ref"),
        )
        if not verified:
            print_plan_row(name, "blocked", detail)
            return {"name": name, "status": "blocked", "scan": "unverified_source"}
        print_plan_row(name, "verified", detail)
        return sync_existing_skill_links(name, existing[0], dry_run)

    if not known:
        print_plan_row(name, "manual", "no installer metadata; keep manifest command as fallback")
        return {"name": name, "status": "manual"}

    source_dir = source_root / known["source_name"]
    clone_state = clone_or_update(known["repo"], dep.get("ref"), source_dir, dry_run)
    if clone_state in {"missing_ref", "ref_mismatch"}:
        print_plan_row(name, "blocked", f"source checkout is not pinned to reviewed ref {dep.get('ref') or '<missing>'}")
        return {"name": name, "status": "blocked", "scan": "unverified_source"}

    if known.get("adapter"):
        adapter_dir = source_root / "_adapters" / name
        target_dir = adapter_dir
        scan_status = "adapter"
        scan_detail = known["risk_note"]
        write_adapter(adapter_dir, name, known["source_name"], dry_run)
    else:
        rel = known.get("skill_subpath", ".")
        target_dir = source_dir if rel == "." else source_dir / rel
        if dry_run and clone_state == "would_clone":
            scan_status = known["risk"]
            scan_detail = f"expected {known['risk']} from previous metadata: {known['risk_note']}"
        else:
            scan_status, scan_output = scan_target(target_dir)
            scan_detail = scan_output.splitlines()[-1] if scan_output.splitlines() else "scan produced no output"

    if scan_status == "red" and not force:
        print_plan_row(name, "blocked", f"{scan_status}; rerun with --force to link anyway")
        return {"name": name, "status": "blocked", "scan": scan_status}

    if scan_status in {"yellow", "red"} and not force:
        print_plan_row(name, "needs-confirmation", f"{scan_status}; rerun with --force after review")
        return {"name": name, "status": "needs_confirmation", "scan": scan_status}

    if not dry_run:
        if not (target_dir / "SKILL.md").exists():
            print_plan_row(name, "failed", f"target has no SKILL.md: {target_dir}")
            return {"name": name, "status": "failed"}
        link_new_skill(name, target_dir, dry_run=False)

    action = "would_link" if dry_run else "linked"
    print_plan_row(name, action, f"{target_dir} ({scan_status}; {scan_detail})")
    return {"name": name, "status": action, "scan": scan_status}


def main():
    parser = argparse.ArgumentParser(description="Plan or install Guyue optional skill dependencies.")
    parser.add_argument("--install", action="store_true", help="Create source checkouts and skill links. Default is dry-run.")
    parser.add_argument("--force", action="store_true", help="Install yellow/red/adapter dependencies after explicit user review.")
    parser.add_argument("--only", nargs="*", help="Install only these dependency names.")
    parser.add_argument(
        "--source-root",
        default="~/.cc-switch/skills/_sources",
        help="Where third-party source checkouts are stored.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    selected = external_dependencies(manifest)
    if args.only:
        wanted = set(args.only)
        selected = [dep for dep in selected if dep.get("name") in wanted]

    dry_run = not args.install
    source_root = Path(args.source_root).expanduser()

    print("[Trace: Guyue/OptionalDeps] scanning local skill roots before any install")
    print(f"mode: {'dry-run' if dry_run else 'install'}")
    print(f"source_root: {source_root}")
    if not dry_run and args.force:
        print("force: enabled for reviewed yellow/red/adapter dependencies")
    elif not dry_run:
        print("force: disabled; yellow/red dependencies will stop")

    results = [install_dependency(dep, source_root, dry_run=dry_run, force=args.force) for dep in selected]
    blocked = [item for item in results if item["status"] in {"blocked", "needs_confirmation", "failed"}]

    if blocked:
        print("\n[Trace: Guyue/OptionalDeps] incomplete dependencies:")
        for item in blocked:
            print(f"- {item['name']}: {item['status']}")
        if not dry_run:
            sys.exit(2)

    print("\n[Trace: Guyue/OptionalDeps] complete")


if __name__ == "__main__":
    main()
