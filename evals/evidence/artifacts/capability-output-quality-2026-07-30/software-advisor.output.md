本地目录可直接推荐：悟空CRM；若重点是企业微信私域运营，可备选 LinkWeChat。

- **名称 (Name)**: 悟空CRM
- **分类 (Category)**: 开源程序
- **链接 (URL)**: [https://gitee.com/wukongcrm/crm_php](https://gitee.com/wukongcrm/crm_php)
- **推荐理由 (Why)**: 本地目录明确标注为开源 CRM 系统，并注明支持 PHP、Java 多语言，和“部署一套 CRM”的需求直接匹配。
- **来源与核对时间 (Source / Checked At)**: 本地目录 `skills/software-advisor/software_catalog.json` 记录的项目链接（未访问）；2026-07-30T10:42:17+0800
- **边界 (Boundary)**: 未联网，未核验该链接是否仍为官方入口、许可证、最新版本、安全状况、兼容性或当前维护状态。

- **名称 (Name)**: LinkWeChat
- **分类 (Category)**: 开源程序
- **链接 (URL)**: [https://gitee.com/LinkWeChat/link-wechat](https://gitee.com/LinkWeChat/link-wechat)
- **推荐理由 (Why)**: 本地目录标注为基于企业微信的开源 SCRM；适合客户运营主要发生在企业微信内的场景，不应替代通用 CRM 的需求评估。
- **来源与核对时间 (Source / Checked At)**: 本地目录 `skills/software-advisor/software_catalog.json` 记录的项目链接（未访问）；2026-07-30T10:42:17+0800
- **边界 (Boundary)**: 未联网，未核验许可证、企业微信适配情况、功能范围、最新维护状态或上游项目真实性。

本地检索记录：

```sh
rg -n -i '"description": ".*crm' skills/software-advisor/software_catalog.json
shasum -a 256 skills/software-advisor/software_catalog.json
```

- `activity`: `local_catalog_lookup`
- 目录路径：`skills/software-advisor/software_catalog.json`
- 目录 SHA-256：`7b68f24dfc7aa1b10f0b226013a440f19f4e23a76bde627e16e29d957719e288`
- 命中：4 条——CRMEB、CRMEB知识付费系统、悟空CRM、LinkWeChat；前两项在目录中被描述为商城/知识付费系统，未作为 CRM 推荐。
- `artifact_ref`: `response`
- 外部版本与上游 Hash：`not-applicable`；未发生外部检索或派生。
