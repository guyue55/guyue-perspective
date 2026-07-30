---
name: static-demo-hardening
description: Static demo hardening for Demo/index.html-style offline previews, report export, tutorial fallbacks, local assets, print safety, and GSAP/runtime resilience. Use when the user asks to harden a static demo or report surface; do not trigger for backend PDF services, unrelated generic frontend rewrites, or tutorial requests without a static demo surface.
---

# static-demo-hardening

## Core Job

Improve the static demo as a high-fidelity preview without accidentally turning it into backend product work.

Default boundary: `Demo/index.html` and directly related static-demo tests or assets unless the user explicitly expands scope.

## Entry Checklist

1. Read project instructions and current repo state.
2. Inspect:
   - product docs or PRD
   - core backend/frontend entrypoints only as context
   - `Demo/index.html`
   - existing demo smoke tests and runtime checks
3. Run `git status --short --branch`.
4. Confirm whether the user asked for:
   - static demo polish
   - real backend feature work
   - cost measurement
   - export hardening

Do not infer backend implementation from demo-review requests.

## Static Demo Rules

1. Keep preview work inside the static demo.
   - Prefer browser-native behavior for HTML/PDF export.
   - Do not invent backend PDF services unless requested.
2. Centralize runtime helpers.
   - Prefer existing demo runtime wrappers such as animation helpers, integrity checks, and export preparation functions.
   - Avoid scattering raw animation state changes across unrelated handlers.
3. Treat broken embeds as environment/config failures first.
   - If YouTube or tutorial playback fails in `file://`, WebView, or referer-poor contexts, provide a stable fallback instead of leaving a broken iframe.
4. Prefer official tutorial sources.
   - Use official vendor docs/videos when available.
   - If official media is unavailable or unreliable, fall back to official documentation links.
5. Preserve report ergonomics.
   - Download/export controls belong in the report surface where users look for them.
   - Long report sections need spacing rhythm, stable anchors, and print-safe rendering.

## Workflow

用户只要求加固方案且已明确给出静态 Demo 场景时，可把该场景作为任务前提输出方案、失败状态机、回退文案与验证矩阵；不得因当前仓库未包含目标文件就把方案任务误判为实现任务。只有用户要求实际修改而目标文件无法定位时才阻断写入，并报告已检查范围。

1. Map the demo surface.
   - Identify affected sections, triggers, modals, sticky controls, and export paths.
2. Design the smallest static change.
   - Copy change
   - Interaction change
   - Runtime helper change
   - Verification target
3. Implement with stable dimensions and reduced-motion support.
4. Run demo checks.
   - Existing smoke tests
   - Runtime integrity check if present
   - Browser preview for desktop and mobile widths when feasible
   - Print/export path when export behavior changed
5. Report exactly what was verified and what remains environment-dependent.

## Export And Report Checklist

- Full report state is settled before export.
- HTML download contains the expected report content.
- PDF export uses browser print/save-to-PDF when that is the project boundary.
- Sticky controls do not occlude report content.
- Print styles hide non-report controls.
- Section spacing matches neighboring report sections.

## Tutorial Fallback Checklist

- Prefer official video or docs.
- Detect contexts likely to block embedded playback.
- Provide a visible "open in browser" or docs fallback.
- Do not rely on a broken iframe as the only path.
- Do not link random third-party tutorial videos when official sources exist.

## Anti-Patterns

- Do not touch backend implementation for a demo-only request.
- Do not add heavy frameworks to a static HTML demo.
- Do not scatter GSAP calls without a wrapper or cleanup path.
- Do not claim PDF generation exists if the browser print dialog is the actual export mechanism.
- Do not skip mobile/print checks for report surfaces.

## Cross-Skill Invocation

- Need commercial UI polish -> `frontend-expert`.
- Need real AI cost/Grounding measurement -> `ai-cost-grounding-measurement`.
- Need project overview report -> `documentation`.
- Need runtime bug root-cause analysis -> `debugging-mindset`.
