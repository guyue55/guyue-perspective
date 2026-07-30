[Trace: Guyue/FrontendExpert] 识别为 B2B 运维后台登录表单；采用现有 React 表单与 toast，低动效；验证视口为 320px、375px、768px。

## 实现方案

- 使用语义化 `<form onSubmit>`：天然支持 Tab 与 Enter 提交。
- 登录失败显示持久的表单内错误摘要；toast 仅作同步提示，不能是唯一错误载体。
- 所有认证失败统一为“账号或密码不正确”，不渲染后端原始文案、账号状态或具体 HTTP 错误。
- 请求中禁用提交以防重复提交；失败后把焦点移到错误摘要。
- 不新增状态管理或动画依赖；沿用现有表单字段、按钮、token 与 toast。

当前仓库未提供实际 React 后台、表单/toast API 或登录接口，因此以下通过 `authenticate` 与 `notify` 两个适配入口接入；最小下一步是将它们绑定到现有登录请求与 toast API。

```tsx
import { FormEvent, useEffect, useRef, useState } from 'react';

type LoginInput = {
  account: string;
  password: string;
};

type LoginOutcome =
  | { type: 'success' }
  | { type: 'invalid_credentials' }
  | { type: 'rate_limited' }
  | { type: 'unavailable' };

type LoginFormProps = {
  authenticate: (input: LoginInput) => Promise<LoginOutcome>;
  notify: (message: string) => void; // 绑定现有 toast.error
  onSuccess: () => void;
};

const messages = {
  invalid_credentials: '账号或密码不正确，请检查后重试。',
  rate_limited: '尝试过于频繁，请稍后再试。',
  unavailable: '暂时无法登录，请稍后重试。',
} as const;

export function LoginForm({
  authenticate,
  notify,
  onSuccess,
}: LoginFormProps) {
  const [account, setAccount] = useState('');
  const [password, setPassword] = useState('');
  const [pending, setPending] = useState(false);
  const [submitError, setSubmitError] =
    useState<keyof typeof messages | null>(null);
  const errorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (submitError) errorRef.current?.focus();
  }, [submitError]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (pending) return;

    setSubmitError(null);
    setPending(true);

    try {
      const outcome = await authenticate({ account: account.trim(), password });

      if (outcome.type === 'success') {
        onSuccess();
        return;
      }

      const errorType =
        outcome.type === 'rate_limited' ? 'rate_limited' : outcome.type;

      setSubmitError(errorType);
      notify(messages[errorType]);
    } catch {
      setSubmitError('unavailable');
      notify(messages.unavailable);
    } finally {
      setPending(false);
    }
  }

  return (
    <form className="login-form" onSubmit={handleSubmit} aria-busy={pending}>
      {submitError && (
        <div
          ref={errorRef}
          className="login-error-summary"
          role="alert"
          tabIndex={-1}
        >
          {messages[submitError]}
        </div>
      )}

      {/* 替换为现有 Form.Field / Form.Control，保留 label 与 control 的关联 */}
      <div className="login-field">
        <label htmlFor="login-account">账号</label>
        <input
          id="login-account"
          name="account"
          type="text"
          autoComplete="username"
          required
          disabled={pending}
          value={account}
          onChange={(event) => setAccount(event.target.value)}
          aria-describedby={submitError ? 'login-error-hint' : undefined}
        />
      </div>

      <div className="login-field">
        <label htmlFor="login-password">密码</label>
        <input
          id="login-password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          disabled={pending}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          aria-describedby={submitError ? 'login-error-hint' : undefined}
        />
      </div>

      <span id="login-error-hint" className="sr-only">
        登录失败信息会显示在表单顶部。
      </span>

      <button type="submit" disabled={pending}>
        {pending ? '登录中…' : '登录'}
      </button>
    </form>
  );
}
```

认证适配层不得把后端返回文案直接透传到 UI：

```ts
export async function authenticate(input: LoginInput): Promise<LoginOutcome> {
  const response = await fetch('/实际登录接口路径', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (response.ok) return { type: 'success' };
  if (response.status === 429) return { type: 'rate_limited' };

  // 所有普通认证失败统一呈现，避免区分账号不存在、密码错误、账号状态等。
  if (response.status >= 400 && response.status < 500) {
    return { type: 'invalid_credentials' };
  }

  return { type: 'unavailable' };
}
```

```css
.login-page {
  box-sizing: border-box;
  display: grid;
  min-block-size: 100dvh;
  place-items: center;
  padding: clamp(16px, 4vw, 32px);
}

.login-form {
  box-sizing: border-box;
  display: grid;
  inline-size: min(100%, 28rem);
  min-inline-size: 0;
  gap: 16px;
}

.login-field {
  display: grid;
  min-inline-size: 0;
  gap: 6px;
}

.login-field input,
.login-form button {
  box-sizing: border-box;
  inline-size: 100%;
  min-inline-size: 0;
}

.login-error-summary {
  border-inline-start: 4px solid var(--color-danger);
  color: var(--color-danger-text);
  overflow-wrap: anywhere;
  padding: 8px 12px;
}

.login-form :is(input, button):focus-visible,
.login-error-summary:focus-visible {
  outline: 3px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.sr-only {
  block-size: 1px;
  clip: rect(0, 0, 0, 0);
  inline-size: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  white-space: nowrap;
}
```

验收要点：

- 键盘：Tab 顺序为账号、密码、登录；任一输入框按 Enter 提交；失败后焦点到错误摘要。
- 移动端：在 320px、375px、768px 视口确认无横向滚动；页面包含标准 viewport meta。
- 防泄露：模拟“账号不存在”和“密码错误”时，页面与 toast 文案完全一致，且不显示后端原始消息。
- 后端前置条件：接口也必须避免通过响应内容、状态码差异或明显时序差异暴露账号是否存在；前端统一文案本身不能构成完整安全边界。
