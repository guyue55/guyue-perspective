# 30 秒产品更新视频生产包（仅规划）

状态：**blocked**。三张截图的实际内容、产品更新信息、投放规格及最终音频决策均未提供，不能产出可发布脚本或进入渲染。

最小下一步：提供以下四项即可解除阻断：

1. 产品名、版本/更新时间、三项更新要点及 CTA。
2. 三张截图文件（或路径）、对应更新点，以及确认可裁切、加字幕和重复使用。
3. 目标平台、画幅、受众与语言。
4. 最终音频选择：明确静音成片，或指定后续配音/音乐方案。当前“自动播放不得有声音”仅锁定播放器默认静音，不等于成片永久静音。

## brief.md

```markdown
## Video Brief
- Goal: 待提供产品更新目标与核心信息
- Audience: 待提供
- Platform: 待提供
- Aspect ratio: 待提供
- Duration: 30 秒
- Core message: 待提供
- Source materials: 3 张用户声明已授权的产品截图；文件、内容和规格待提供
- Allowed asset sources: 仅上述用户资产及后续确认的文字叠层；不生成、不下载素材
- Main route: HTML/motion 产品截图编排，planning_only
- Native/configured capabilities: 未调用
- Required configuration if missing: 本次仅规划无需配置；后续渲染前需确认可用渲染路径
- Audio policy: 自动播放默认静音；配音、旁白、音乐、音效均为 open，未锁定静音成片
- Review checkpoints:
  1. 文案与三张截图映射确认
  2. 画幅与安全区确认
  3. 音频最终决策确认
  4. 成片 QA
```

## script.md

```markdown
| 段落 | 时间 | 画面与屏幕文字 | 旁白/对白 | 音频 |
|---|---:|---|---|---|
| 开场 | 0-3s | 截图 1 背景；[产品名] [版本/更新日期] | 未定 | open |
| 更新点 1 | 3-11s | 截图 1；[更新点 1 标题]；[用户价值] | 未定 | open |
| 更新点 2 | 11-19s | 截图 2；[更新点 2 标题]；[用户价值] | 未定 | open |
| 更新点 3 | 19-27s | 截图 3；[更新点 3 标题]；[用户价值] | 未定 | open |
| 收束 | 27-30s | 截图 3 复用；[CTA] | 未定 | open |
```

说明：屏幕文字必须在提供产品更新信息后填写；当前不能将无配音人选推断为静音成片。

## storyboard.md

| 场景 | 时间 | 视觉方案 | 素材来源 | 声音/文字 | 验收条件 |
|---|---:|---|---|---|---|
| 1 | 0-3s | 截图 1 轻微缩放或静态展示，叠加版本标题 | 用户截图 1，planning_only | 标题待提供；音频 open | 标题在目标画幅安全区内 |
| 2 | 3-11s | 截图 1 聚焦更新区域，叠加更新点 1 | 用户截图 1，planning_only | 文案待提供；音频 open | 不遮挡关键产品信息 |
| 3 | 11-19s | 截图 2 聚焦更新区域，叠加更新点 2 | 用户截图 2，planning_only | 文案待提供；音频 open | 裁切不损失关键界面信息 |
| 4 | 19-27s | 截图 3 聚焦更新区域，叠加更新点 3 | 用户截图 3，planning_only | 文案待提供；音频 open | 文字可读、信息映射正确 |
| 5 | 27-30s | 复用截图 3，叠加 CTA | 用户截图 3，planning_only | CTA 待提供；音频 open | CTA 清晰且与产品目标一致 |

时长合计：3 + 8 + 8 + 8 + 3 = 30 秒。

## asset_manifest.json

```json
{
  "status": "blocked",
  "assets": [
    {
      "id": "screenshot-01",
      "type": "image",
      "source": "user_asset",
      "filename": null,
      "role": "opening_and_update_1",
      "license": {
        "permission": "user_stated_authorized",
        "evidence": null,
        "publication_status": "pending_confirmation",
        "modification_allowed": "unconfirmed"
      },
      "resolution": null
    },
    {
      "id": "screenshot-02",
      "type": "image",
      "source": "user_asset",
      "filename": null,
      "role": "update_2",
      "license": {
        "permission": "user_stated_authorized",
        "evidence": null,
        "publication_status": "pending_confirmation",
        "modification_allowed": "unconfirmed"
      },
      "resolution": null
    },
    {
      "id": "screenshot-03",
      "type": "image",
      "source": "user_asset",
      "filename": null,
      "role": "update_3_and_cta",
      "license": {
        "permission": "user_stated_authorized",
        "evidence": null,
        "publication_status": "pending_confirmation",
        "modification_allowed": "unconfirmed"
      },
      "resolution": null
    }
  ]
}
```

## edit_plan.json

```json
{
  "status": "planning_only_blocked",
  "duration_sec": 30,
  "aspect_ratio": null,
  "timeline": [
    { "time": "0-3s", "asset": "screenshot-01", "purpose": "opening" },
    { "time": "3-11s", "asset": "screenshot-01", "purpose": "update_1" },
    { "time": "11-19s", "asset": "screenshot-02", "purpose": "update_2" },
    { "time": "19-27s", "asset": "screenshot-03", "purpose": "update_3" },
    { "time": "27-30s", "asset": "screenshot-03", "purpose": "cta" }
  ],
  "transitions": "cut_or_short_dissolve_pending_visual_review",
  "motion": "static_or_subtle_pan_zoom_only_after_crop_review",
  "text_overlays": "blocked_pending_product_copy",
  "caption_policy": "not_applicable_until_voice_or_narration_decision",
  "audio": {
    "final_track_status": "open",
    "preview_autoplay_muted": true,
    "autoplay_sound": false
  },
  "review_checkpoints": [
    "copy_and_asset_mapping",
    "ratio_and_safe_area",
    "final_audio_decision",
    "pre_export_qa"
  ]
}
```

## compose_plan.json

```json
{
  "status": "blocked",
  "clip_order": [
    "screenshot-01:opening",
    "screenshot-01:update_1",
    "screenshot-02:update_2",
    "screenshot-03:update_3",
    "screenshot-03:cta"
  ],
  "unique_asset_count": 3,
  "timeline_item_count": 5,
  "expected_duration_sec": 30,
  "audio_tracks": [
    {
      "status": "open",
      "reason": "no_voice_candidate; music_and_sfx_not_decided"
    }
  ],
  "subtitle_policy": "pending_script_and_audio_decision",
  "render_route": "unselected_planning_only",
  "codec_container": null,
  "output_path": null,
  "export_evidence": null
}
```

## prompts/

不适用。本包仅规划使用既有截图和文字叠层，不包含任何生成素材。

## qa_report.md

```markdown
## QA Report
- Overall status: blocked
- Duration plan: pass — 30 秒时间线已闭合
- Aspect ratio: blocked — 未提供平台或画幅
- Product accuracy: blocked — 未提供产品名、版本、更新点及 CTA
- Screenshot integrity: blocked — 未提供文件，无法检查裁切、分辨率、文字可读性或黑帧
- Asset permission: needs_confirmation — 用户声明已授权；仍缺文件对应关系、修改许可与发布证据
- Caption sync: blocked — 无已确认脚本或音频轨
- Audio playback: planned — 自动播放必须静音
- Final audio: blocked — 配音、旁白、音乐和音效均未决，不可默认为静音成片
- Export readiness: blocked — 无画幅、素材文件、文案和最终音频决策
```
