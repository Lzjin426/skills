# Python 代码 AI 痕迹检测与改写清单

本清单专门针对软著申请场景下的 Python 源代码文档。按"识别强度"分级，从"机器查重
必中"到"加分项纹理"。改写时**从上往下过**，红线和一级是必做，二三级按情况挑。

---

## ❗ 红线（软著规则硬要求，必须清除）

软著规则明确要求源代码文档不得出现以下内容（见《计算机软件著作权登记办法》）。
这些和 AI 味无关，是独立的硬要求。

| 模式 | 示例 | 处理 |
|------|------|------|
| 版权声明块 | `# Copyright 2026 ...` / `# All rights reserved` | 删除整块 |
| 作者标签 | `@author: xxx` / `# Author: xxx` / `__author__ = ...` | 删除整行 |
| 邮箱 / URL | `xxx@gmail.com` / `https://github.com/...` | 删除或替换 |
| 日期字符串 | `# Created on 2026-03-12` / `__date__ = ...` | 删除整行 |
| License 声明 | `# License: MIT` / `# SPDX-License-Identifier: ...` | 删除整行 |
| 块注释头 | `""" ... """` 作为文件头大段说明 | 整块删除或压成一行 `#` |
| `copyright` 字样 | 代码里任何位置出现 | 全文搜索删除 |
| 真实人名 / 公司名 | 注释或字符串里的真实姓名、公司 | 替换为通用占位 |

**扫描方法**：用 Grep 一次过。

```
copyright|Copyright|COPYRIGHT|@author|__author__|__date__|License:|SPDX-|https?://
```

注意：字符串字面量里的 URL（比如 API endpoint）如果是程序必要的不能删，要判断
是否为注释/声明用途。这种情况下 audit 标注、让用户决定。

---

## 🔴 一级痕迹（AI 味重度，查重高风险）

### 1. Docstring 地毯式覆盖

**AI 特征**：几乎每个函数都配 Google / NumPy 风格三段式 docstring，`Args/Returns/Raises`
齐全，经常只是把签名用英文复述一遍。

```python
# AI 风格
def add_user(name: str, age: int) -> User:
    """Add a new user to the system.

    Args:
        name: The name of the user.
        age: The age of the user.

    Returns:
        The created User object.

    Raises:
        ValueError: If age is negative.
    """
    ...
```

**改写**：保留类和对外入口的 docstring 并压成 1 行；内部 helper 的 docstring 直接删。
真人只在信息密度高的地方写 docstring。

```python
# 改后
def add_user(name: str, age: int) -> User:
    """新建用户。age<0 抛 ValueError。"""
    ...

def _validate_age(age):  # 原本也有 docstring，删掉
    if age < 0:
        raise ValueError("age must be >= 0")
```

### 2. 类型注解 100% 覆盖

**AI 特征**：每个参数和返回值都标注，包括明显冗余的 `def _sum(a: int, b: int) -> int`。

**改写**：
- 公共 API（对外函数、类的 `__init__`、复杂泛型）：**保留**
- 私有函数（`_` 开头）、lambda、局部 helper：**去掉注解**
- 明显类型（`def greet(name)` 不用 `name: str`）：**去掉**

```python
# AI
def _calculate_discount(price: float, rate: float) -> float:
    return price * (1 - rate)

# 改后
def _calculate_discount(price, rate):
    return price * (1 - rate)
```

### 3. 固定流程模板

**AI 特征**：文件结构极度规整，千篇一律 `import → 常量 → 定义函数 → if __name__ == "__main__"`。
可视化脚本常见模板 `加载数据 → 处理 → 绘图 → plt.show()`。

**改写**：
- 把常量塞到使用点附近，不必全部顶在文件头
- `if __name__ == "__main__"` 块可以拆出来或在小脚本里直接裸写
- 在文件间打破对称：有的文件先定义类后写函数、有的反过来

### 4. 注释全英文 + 复述型

**AI 特征**：中文项目里注释清一色英文，且多为"解释代码做什么"（`# increment counter`），
而不是"解释为什么这么做"。

**改写**：
- 删掉复述型注释（`i += 1  # increment counter` → `i += 1`）
- 在业务逻辑拐点、workaround、踩坑点加简短中文注释
- 保留少量英文注释作为"混用"痕迹，不必全改中文

```python
# AI
count = count + 1  # increment the counter by one
result = process(data)  # process the data and get result

# 改后
count += 1
result = process(data)  # FIXME 这里 data 为空时会炸，先这样
```

### 5. Try/except 地毯式覆盖

**AI 特征**：几乎每个函数体都包一层 `try: ... except Exception as e: logger.error(...)`。

**改写**：
- 只在边界保留（IO、网络请求、用户输入解析、子进程调用）
- 内部工具函数的外包 try/except 全删
- `except Exception` 改成更具体的异常类；或者干脆让它炸

---

## 🟡 二级痕迹（明显但不致命）

### 6. "现代 Python" 炫技

| AI 爱用 | 回退为 | 理由 |
|---------|--------|------|
| `match/case` 简单分派 | `if/elif/else` | 3.10 新语法，真人小项目少用 |
| 海象 `:=` | 显式赋值 | 炫技感强 |
| `f"{x=}"` debug | `print("x:", x)` 或 `logger.debug("x=%s", x)` | 3.8 debug 语法，教程里才密集出现 |
| `@dataclass(frozen=True, slots=True)` | 普通 `class` 或 `dict` / `NamedTuple` | 过度设计 |
| `typing.Protocol` / `TypeVar` / `Generic` | duck typing | 真人小项目几乎不用 |
| `from __future__ import annotations` | 直接写注解或不写 | 非必要不加 |
| `functools.reduce` / `operator.xxx` | 显式 for 循环 | 学院派写法 |
| `itertools` 链式调用堆叠 | 拆成 for 循环 | 同上 |

**原则**：不是全改，是挑最扎眼的几处。保留 1–2 处现代语法作为"偶尔炫技"的真人痕迹。

### 7. 命名过度语义化

**AI 特征**：`user_authentication_service_instance`、`calculate_total_price_with_tax`、
`retrieve_user_data_from_database`——名字恨不得就是一句话。

**改写**（分层处理）：
- **类名、对外公共函数**：保留完整语义名
- **局部变量、循环变量、参数**：缩短为惯用名

```python
# AI
user_authentication_service = UserAuthenticationService()
retrieved_user_data = retrieve_user_data_from_database(user_id)
for current_item_index, current_item in enumerate(item_list):
    ...

# 改后
auth = UserAuthenticationService()
user = fetch_user(user_id)  # 注意：如果 fetch_user 在别处定义，要一起重命名
for i, item in enumerate(items):
    ...
```

**随意命名策略**（让名字更像人随手起的）：
- 局部变量、循环变量可用极简惯用名：`tmp`、`buf`、`x`、`val`、`item`、`it`
- 循环索引用 `i`、`j`、`idx`，而非 `current_item_index`
- 允许缩写不一致：`db` vs `database`、`cfg` vs `config`、`resp` vs `response`
- 偶尔用无意义占位：`stuff`、`thing`、`data`（但要控制密度）

```python
# 更随意的改后示例
auth = UserAuthenticationService()
user = fetch_user(uid)
for i, it in enumerate(items):
    tmp = calc(it)
    buf[i] = tmp
```

**重要**：函数重命名时必须用 Grep 找到所有调用点一起改，禁止只改定义。

### 8. 导入顺序过度整齐

**AI 特征**：import 严格按 PEP 8 三段分组（stdlib / 第三方 / 本地），每组内部字母排序，
组间空行整齐。

**改写**：偶尔打破一两处顺序——真人 import 是边写边加的，常有"忘了加在上面直接丢末尾"
的情况。**克制**，只打破 1–2 处。

### 9. 日志 / 配置样板

**AI 特征**：
```python
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

**改写**：小项目直接用 `logging.basicConfig(level=logging.INFO)` 一行搞定，
或者干脆用 `print`（真人小工具很常见）。

### 10. Pathlib 模板化

**AI 特征**：`Path(__file__).parent / "config" / "settings.yaml"` 这套写法被 AI 用滥。

**改写**：
- 小脚本可以混用 `os.path.join` 和 `pathlib`
- 相对路径场景直接用字符串 `"config/settings.yaml"`
- 不是全改，挑 2–3 处替换

---

## 🟢 三级纹理（加分项，让代码有"活人感"）

### 11. 时间层次 / 考古痕迹

**真人特征**：
- `# TODO 周一再看这个边界条件`
- `# FIXME 这里 pandas 2.0 会 deprecation warning`
- `# hack: 暂时这样，等 API 升级`
- 被注释掉的旧实现 `# result = old_method(x)  # 性能太差弃用`
- `# 原来这里是 threading，改成 asyncio 后这段要清掉`

**改写策略**：在每个文件**克制地**插入 1 处此类注释。约束：
- 全项目累计最多 3 处
- 单文件最多 1 处
- **不得出现在核心算法函数中**（审查员会重点看核心算法）
- 优先放在工具函数、配置模块等次要位置

### 12. 不一致细节

- **引号混用**：大部分用 `"`，偶尔一两个字符串用 `'`
- **空行**：偶尔连续空两行，或者该空的地方不空
- **缩进后注释对齐**：偶尔对不齐

**约束**：每个文件最多 2 处。太多就过犹不及。

### 13. 调试残留

- `print(x)  # debug` 或 `# print(x)`（注释掉的 debug）
- `breakpoint()` 注释掉 `# breakpoint()`
- `# import pdb; pdb.set_trace()  # 调试用`

**约束**：全项目累计最多 2 处，仅限非关键函数。千万别放在函数入口或主流程里，
否则看起来像没完成的代码。

### 14. 变量复用

**AI 特征**：每步计算都起新名字 `raw_data → cleaned_data → normalized_data → final_data`。

**真人特征**：常常复用 `data = load(); data = clean(data); data = normalize(data)`。

**改写**：在数据处理流水线类代码里合并 1–2 处即可。

### 15. 偶发"口语化"

**真人特征**：
- 变量名偶尔搞怪 `stuff`、`tmp2`、`x_new`
- 短注释带语气 `# 靠，这里 API 又变了` / `# 这段是从 xx 改的`

**约束**：商业代码里不要出现，学生/个人项目全项目累计最多 2 处。

---

## 改写检查表（rewrite 模式收尾必看）

完成后逐条核对：

- [ ] 所有 ❗ 红线项已清除（grep 验证）
- [ ] 代码能 `python -c "import ..."` 或运行——语法/导入没断
- [ ] 重命名的函数/变量在所有调用点同步更新（全项目 grep 验证）
- [ ] 说明书里提到的函数名、模块名、类名**未被改动**
- [ ] 生成 `dehumanize-diff-<timestamp>.md`，列出所有改动点
- [ ] 字数/行数变化不超过原文 ±15%（除非是删红线）——过度改写会引发功能对应性校验问题

## 一个完整改写示例（浓缩）

**改前（典型 AI 风格）**：

```python
# -*- coding: utf-8 -*-
"""
User authentication module.

Copyright (c) 2026 Example Corp.
Author: John Doe <john@example.com>
Created on: 2026-03-12
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user with username and password.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        A dict containing user information if authentication succeeds,
        None otherwise.
    """
    try:
        user_record = database_query_user_by_username(username)
        if user_record is None:
            logger.info(f"User not found: {username=}")
            return None
        match verify_password(password, user_record["password_hash"]):
            case True:
                return {"user_id": user_record["id"], "username": username}
            case False:
                return None
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return None
```

**改后**：

```python
import logging

log = logging.getLogger(__name__)


def authenticate_user(username, password):
    """校验用户名密码，成功返回 user 信息 dict，失败返回 None。"""
    user = db_get_user(username)
    if user is None:
        log.info("用户不存在: %s", username)
        return None
    # TODO password hash 升级到 argon2 后这里要改
    if verify_password(password, user["password_hash"]):
        return {"user_id": user["id"], "username": username}
    return None
```

改动点：
- 删除模块头 docstring、copyright、author、日期
- 删除冗余类型注解（私有函数层级）
- docstring 压成一行中文
- `database_query_user_by_username` → `db_get_user`（缩短 + 全局同步）
- `logger` → `log`（个人习惯痕迹）
- `match/case` → `if`
- 外层 try/except 删除，让异常自然抛出（边界层再接）
- 加一条 `# TODO` 体现时间痕迹
- `f"{username=}"` → `%s` 占位符
