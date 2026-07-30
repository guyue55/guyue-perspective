[Ponytail Check] 停在第 1 层：只有一次加法调用，不需要扩展机制。

删除 `ICalculator`、`AbstractCalculator`、`CalculatorFactory` 和 `DefaultCalculator`，直接写：

```text
result = a + b
```

若需命名表达业务意图，保留一个普通函数即可：

```text
add(a, b)
```

仅当出现真实的第二个使用点，且确实需要在多种计算策略间选择时才抽象：

- `ICalculator`：存在多个可替换实现，调用方确实依赖统一契约。
- `AbstractCalculator`：多个实现共享稳定且非微小的通用逻辑。
- `CalculatorFactory`：实例选择由配置、输入或运行环境决定，且调用方不应知道具体实现。

“可能以后会有更多算法”不是抽象理由；等需求真实出现再加。
