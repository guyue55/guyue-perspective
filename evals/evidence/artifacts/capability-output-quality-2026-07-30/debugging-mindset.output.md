[Trace: Guyue/DebuggingMindset] 建立症状、假设与最低充分证据边界

基于用户提供前提，故障高度收敛在应用之前的 Nginx/Ingress 请求体接收边界：小文件成功、8MB 稳定 413，说明“偶发”更可能是文件大小、路由或实例差异造成，而非瞬时故障。尚不能断言具体是 `client_max_body_size`、Ingress 配置还是另一层网关限制。

| 症状 | 待验证假设 | 最小判定证据 |
|---|---|---|
| Nginx 记录 413，应用无同请求日志 | Nginx 本机在读取请求体时拒绝 | 同时段 error log 出现请求体过大语义；access log 的 `upstream_status` 为空 |
| 8MB 必现，小文件正常 | 生效的请求体上限低于 8MB | 该 `Host + URI` 匹配的 `server/location` 生效配置及其来源 |
| 发布后出现，表现“偶发” | 新旧实例、灰度版本或路由配置不一致 | 每个入口实例的生效配置、镜像/发布版本、启动时间存在差异 |
| access log 为 413 但无本机错误日志 | 413 来自上游网关/WAF/另一层代理 | `upstream_status=413`、响应头特征及上游对应日志 |

先收集以下最低充分证据，按同一请求 ID；若没有请求 ID，则以时间窗口、`Host`、URI、客户端 IP、`Content-Length` 关联：

1. Nginx access log 原始行：请求方法、URI、状态、`request_length`、`upstream_status`、`upstream_addr`、`request_time`、`upstream_response_time`。
2. 同一时间窗口的 Nginx error log 原始行。重点寻找“请求体过大”类信息。
3. 413 响应头：`Server`、请求 ID、任何网关标识。
4. 实际命中入口的生效配置：所有 `client_max_body_size` 定义、对应 `server_name`、`location`、`proxy_pass` 与 include 来源。
5. 发布前后入口实例清单：版本/镜像、启动时间、负载均衡目标；若使用 Ingress，同时提供 Ingress 与 Controller ConfigMap 的只读导出。

可在实际拒绝请求的 Nginx 实例执行以下只读采集：

```sh
rg -n -C 2 '<request-id>|<精确时间>' /var/log/nginx/access.log /var/log/nginx/error.log

nginx -T 2>&1 | rg -n -C 4 'client_max_body_size|server_name|location|proxy_pass|include'
```

若运行在 Kubernetes，补充只读导出实际入口的 Ingress、Controller 配置和全部入口 Pod 的版本/启动时间；不要只查看发布仓库中的模板配置。

当前止血边界：

- 暂时在产品侧明确拒绝接近 8MB 的上传，避免用户反复失败；不要把上传请求加入重试。
- 不要盲目全局调大请求体上限、重启入口或回滚。只有证实是本次发布引入且回滚目标的生效配置正确时，回滚才是可评估的止血选项。
- 若证据确认 Nginx 本机拒绝，再按命中的 `Host + location` 做最小范围修复，并用 1MB、阈值附近、8MB 三组文件回归；同时核对所有入口实例一致。

[等待日志/证据] 当前缺少同请求的 Nginx error log、`upstream_status` 与实际生效配置，不能安全给出具体配置补丁。
