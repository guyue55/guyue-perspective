最小修复应把权限边界收回后端，并让两个页面复用同一前端权限入口。

```ts
// 后端：DELETE /users/:id
router.delete("/users/:id", requireAuth, async (req, res) => {
  requirePermission(req.user, "users:delete");

  await userService.delete(req.params.id);
  res.sendStatus(204);
});
```

```ts
// 前端：由后端下发的权限集合驱动，不再硬编码 role === "admin"
export const canDeleteUsers = (permissions: string[]) =>
  permissions.includes("users:delete");
```

```ts
// 页面 A、页面 B 共用
const showDeleteButton = canDeleteUsers(currentUser.permissions);

{showDeleteButton && <DeleteUserButton userId={user.id} />}
```

审查结论：

- `role == admin` 仅能控制界面显隐，不能构成安全控制；删除接口必须在后端鉴权后才执行。
- 两处重复判断应收敛为单一 `canDeleteUsers`/权限 Hook，避免权限规则漂移。
- 后端鉴权需覆盖越权反例：非 `users:delete` 权限的已登录用户请求删除接口，应返回拒绝响应且不删除数据。
