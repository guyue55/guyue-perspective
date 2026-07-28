---
name: video-extractor
description: Methodologies for extracting normalized metadata, post captions, transcripts, and source media from video platforms. Useful when building media ingestion tools or analyzing video links.
---

# video-extractor (Platform Extraction Workflow)

**Mission:** Convert authorized video-platform URLs into a normalized, provenance-aware material folder whose assets match the requested extraction mode.

## The Standard Asset Contract
Create a dedicated folder only when the user asks for an actual extraction. Do not create empty placeholder assets.

| Mode | Required assets | Optional assets |
|---|---|---|
| `metadata-only` (default) | `metadata.json`, `post_caption.txt` | platform-provided caption file |
| `transcript` | metadata assets plus `transcript.txt` | audio intermediate, removed after verification unless requested |
| `source-media` | metadata assets plus the downloaded source file | `transcript.txt` when separately requested |

`metadata.json` records source URL, platform, extraction time, selected mode, field provenance, authorization basis, and planned/generated/failed asset counts. Every known field maps to its concrete source (`user_input`, platform metadata, caption file, ASR, or derivation); do not provide an empty generic provenance schema when values are already known.

Every downloaded or generated file records `sha256`, byte size, and verification status. For planning-only or blocked assets, use `sha256: null` with an explicit status; never omit the checksum field or invent a digest before a file exists.

## Downstream Distillation Handoff

When material will be passed to `book-distiller`, `skill-crafting`, or another methodology extractor, provide one normalized handoff instead of coupling to a downloader-specific directory:

- source URL, platform, title/author when known, extraction time, authorization basis, selected mode, and tool/provider version;
- transcript or caption origin (`platform_caption`, `ASR`, `user_provided`), language, timestamp coverage, known gaps, confidence/quality notes, and transformations;
- file names, byte sizes, SHA-256 values, and field-level provenance;
- missing/failed assets, blocked segments, and what must not be inferred from them.

The downstream Skill consumes this contract, not the downloader implementation. Acquisition failure remains an explicit material gap; it must not be repaired by invented transcript content.

## Authorization Boundary
- Only extract media the user owns, is authorized to process, or that is explicitly licensed for download and reuse.
- Do not bypass login, paywalls, DRM, geo-blocking, private groups, or platform anti-abuse controls.
- Default to `--metadata-only` when the user only needs analysis, title, description, or transcript planning.

## Provider Strategies

### 1. yt-dlp Primary (Default for YT/Bili)
- After authorization and when `source-media` is requested, a suitable command template is:
  `yt-dlp --write-info-json --write-description --format "bv*+ba/b" --merge-output-format mp4 -o "video.%(ext)s" [URL]`
- Parse the resulting `.info.json` and `.description` to populate `metadata.json` and `post_caption.txt`.

### 2. ASR Integration (Transcript)
- Use platform captions first when they are available and authorized.
- If the requested transcript requires ASR, state the local/provider capability, expected download or cost, data boundary, and output before execution. Do not ask about ASR when the user requested metadata only.
- Keep `metadata-only` free of large media downloads.

### 3. Graceful Degradation
- If blocked (e.g. WeChat Channels), say: `[Extractor] Target is heavily walled. Please download manually and place the file here. I will resume the ASR workflow.`
