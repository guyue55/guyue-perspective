```yaml
extraction_plan:
  mode: source-media
  execution: blocked
  authorization_basis: "作者明确允许下载，仅用于内部评审"
  known_metadata:
    title: Demo
    duration_seconds: 95
    subtitles_available: false
  planned_assets:
    - metadata.json
    - post_caption.txt
    - video.<ext>
  constraints:
    - 不下载、不生成文件
    - 不尝试绕过登录、DRM、地域或平台限制
    - 不以 ASR 补全未请求的字幕
  blocker:
    missing:
      - source_url
      - platform
    minimum_next_step: "提供公开视频 URL；平台可由 URL 识别。"

result_schema:
  source_url:
    value: null
    provenance: user_input
    status: blocked_missing_input
  platform:
    value: null
    provenance: derivation
    status: blocked_missing_source_url
  extraction_time:
    value: null
    provenance: derivation
    status: planned_not_executed
  selected_mode:
    value: source-media
    provenance: user_input
  authorization_basis:
    value: "作者明确允许下载，仅用于内部评审"
    provenance: user_input
  metadata:
    title:
      value: Demo
      provenance: user_input
    duration_seconds:
      value: 95
      provenance: user_input
    author:
      value: null
      provenance: user_input
      status: not_provided
    subtitles_available:
      value: false
      provenance: user_input
  assets:
    metadata.json:
      status: planned_blocked
      sha256: null
      byte_size: null
      verification_status: not_created
    post_caption.txt:
      status: planned_blocked
      sha256: null
      byte_size: null
      verification_status: not_created
    source_media:
      filename: null
      status: planned_blocked
      sha256: null
      byte_size: null
      verification_status: not_downloaded
    platform_caption:
      status: unavailable
      sha256: null
      byte_size: null
      verification_status: not_applicable
  asset_counts:
    planned: 3
    generated: 0
    failed: 0
    blocked: 3
```

缺口：公开视频 URL。提供后可识别平台并执行该计划。
