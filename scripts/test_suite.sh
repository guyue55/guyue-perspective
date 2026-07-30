#!/bin/bash

# Guyue Digital Twin - Comprehensive Test Suite
# Runs all health probes, CI validators, and internal audits.

set -e
export PYTHONDONTWRITEBYTECODE=1

echo "=========================================="
echo "🚀 Starting Guyue Universal Test Suite..."
echo "=========================================="

echo "[0/15] Running Zero-Leakage Security Scanner..."
python3 scripts/security_scanner.py

echo ""
echo "[1/15] Running Security Scanner Regression Tests..."
python3 scripts/test_security_scanners.py

echo ""
echo "[2/15] Running Ruff Static Checks..."
ruff check --no-cache scripts src

echo ""
echo "[3/15] Running Codex Session Extractor Tests..."
python3 scripts/test_codex_extractor.py

echo ""
echo "[4/15] Running Routing And Context Budget Gates..."
python3 scripts/test_skill_router.py
python3 scripts/test_cognitive_expansion_contract.py
python3 scripts/test_cognitive_expansion_output_audit.py
python3 scripts/check_capability_chain.py --json
python3 scripts/test_capability_runner_paths.py
python3 scripts/test_context_budget.py
python3 scripts/check_context_budget.py
python3 scripts/test_try_guyue.py
python3 scripts/try_guyue.py >/dev/null

echo ""
echo "[5/15] Running Behavior Replay Checker Tests..."
python3 scripts/check_behavior_replay.py --self-test
for observations_path in evals/observations-*.json; do
  python3 scripts/check_behavior_replay.py "$observations_path"
done

echo ""
echo "[6/15] Running Long Goal Control-Pack Checker..."
python3 scripts/check_long_goal_pack.py --self-test
python3 scripts/simulate_long_goal_lifecycle.py --json

echo ""
echo "[7/15] Running Full Install Payload Checker..."
python3 scripts/test_release_payload.py
python3 scripts/check_full_install.py --self-test
python3 scripts/simulate_install_journey.py --json

echo ""
echo "[8/15] Running Claude Marketplace Validation..."
if command -v claude >/dev/null 2>&1; then
  claude plugin validate --strict .
else
  echo "Claude CLI not found; internal marketplace schema checks remain active in CI validation."
fi

echo ""
echo "[9/15] Running MCP Route And Memory Safety Tests..."
python3 scripts/test_guyue_paths.py
python3 scripts/test_local_skill_discovery.py
python3 scripts/test_memory_concurrency.py
python3 scripts/test_memory_migration.py
python3 scripts/test_mcp_server.py

echo ""
echo "[10/15] Running Environmental Doctor Probe..."
python3 scripts/doctor.py

echo ""
echo "[11/15] Running CI Validators..."
python3 scripts/test_single_entrypoint_contract.py
python3 scripts/ci_validate_skills.py

echo ""
echo "[12/15] Running Prompt And Behavior Contract Evaluator..."
python3 scripts/run_eval.py

echo ""
echo "[13/15] Running Birth Certificate Check..."
python3 scripts/check_birth_certificate.py

echo ""
echo "[14/15] System Health Check Completed."
echo "✅ Guyue local validation passed."
echo "=========================================="
