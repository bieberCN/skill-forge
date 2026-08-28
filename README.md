# Skill Forge

一个用于快速生成和校验 AI Agent Skill 的个人模板库。但把重点收敛到可维护的脚手架：

```text
SKILL.md → MCP/外部数据 → scripts/process.py → payload-schema.json → 前端/Agent
```

## 快速开始

```bash
./bin/new-skill market-snapshot --title "市场快照" --domain crypto
python3 scripts/validate_skill.py skills/market-snapshot
python3 skills/market-snapshot/scripts/process.py < skills/market-snapshot/fixtures/sample-input.json
```

生成器会创建：

```text
skills/<name>/
├── SKILL.md
├── skill.meta.json
├── payload-schema.json
├── scripts/process.py
├── fixtures/sample-input.json
├── fixtures/_meta.json
├── evals/evals.json
└── review.md
```

## 约定

- `SKILL.md` 只描述 Agent 的触发条件、数据源、步骤和边界。
- 需要稳定复现的计算放进 `scripts/process.py`，不要让 LLM 自己重算。
- `fixtures/` 使用冻结输入，便于离线回归；线上实时数据不直接提交。
- 输出必须符合 `payload-schema.json` 的顶层结构。
- MCP 地址、Token、用户数据只从环境变量读取，不写入仓库。

## 参数

生成后编辑 `skill.meta.json` 的 `input_schema`，再同步 `SKILL.md` 的参数表。当前生成器支持 `string`、`number`、`integer`、`select`、`multiple`。

## 设计边界

这个仓库是 Skill 模板和本地回归工具，不是 MCP 服务端、自动交易系统或前端应用。它默认输出研究辅助结果，金融类 Skill 必须保留免责声明和数据缺口。
