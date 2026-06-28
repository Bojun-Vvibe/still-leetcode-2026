# data/ —— 预留：结构化数据

目前公司清单直接维护在根目录 [`README.md`](../README.md) 的表格里，**贡献者改表格就行**，无需关心这个目录。

这个目录是为将来预留的：当数据量变大、想做成可检索的网站 / API 时，会把表格迁移成结构化文件（每家公司一个 YAML），再自动生成 README 表格。

设想中的格式（**尚未启用**）：

```yaml
# data/companies/bytedance.yaml
name: 字节跳动
asks_leetcode: partial        # yes | partial | no | unknown
format: [现场手写, OA]
difficulty: 中-难
ai_policy: 面试中禁用 AI
sources:
  - type: 亲历
    date: 2026-05
```

在迁移启用之前，**请不要往这里加文件**，直接编辑根 README 表格即可。有兴趣帮忙做自动化（脚本 / GitHub Action）的，欢迎来 [Discussions](../../discussions) 认领。
