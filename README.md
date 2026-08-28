# Skill Forge

> A bilingual, contract-first toolkit for creating, testing, and maintaining AI Agent Skills.

[中文](#中文说明) · [English](#english)

---

## 中文说明

### 项目是什么

Skill Forge 是一个面向个人项目的 AI Agent Skill 工程模板库。它把一个 Skill 所需的说明、参数、数据输入、确定性计算、输出契约和回归验证组织成固定结构，从而可以用一条命令快速创建新的分析能力。

它适合构建：

- 市场快照、行情监控和指标分析；
- 数据查询、评分、筛选和排序工具；
- 风险提示、事件归因和研究卡片；
- 需要 MCP、API 或本地数据源的 Agent 工作流。

它不是完整的前端应用、MCP 服务端或自动交易系统，而是 AI Agent 能力的可复用组件层。

### 核心架构

```text
用户问题 / User request
        ↓
SKILL.md：触发条件、参数和工作流
        ↓
L1：MCP / API / 本地数据获取
        ↓
L2：Python 确定性计算
        ↓
L3：Agent 解释结果和数据缺口
        ↓
L4：结构化 JSON Payload
        ↓
前端、报告或下游 Agent
```

核心原则是：语言模型负责理解和解释，脚本负责计算和组装。这样可以减少重复计算、格式漂移和不可复现的结果。

### 技术栈与语言职责

| 语言 / 格式 | 用途 | 关键位置 |
|---|---|---|
| Python 3 | 生成器、校验器、数据清洗、指标计算、Payload 组装 | `scripts/`、`skills/*/scripts/` |
| Bash | 提供简洁的命令行入口 | `bin/new-skill` |
| JSON | 参数元数据、输入 Fixture、输出契约、评测用例 | `*.json` |
| YAML | Skill 的 Agent 元数据和可读配置 | `SKILL.md` frontmatter、可扩展配置 |
| Markdown | Agent 指令、产品说明、评审记录 | `SKILL.md`、`review.md`、`README.md` |
| HTML | 可选的静态展示层或交互原型 | `skills/*/*.html` |

当前版本只依赖 Python 标准库，不需要安装第三方 Python 包。

### 目录结构

```text
skill-forge/
├── README.md                         # 本文档，中英文项目说明
├── core/                             # 运行时与输入/输出契约
├── connectors/                       # Fixture、HTTP 等数据连接器
├── evaluation/                       # 离线评测执行器
├── docs/design/                      # 持续设计文档与决策记录
├── bin/
│   ├── new-skill                     # 一键生成命令
│   └── run-skill                     # 统一运行和校验入口
├── scripts/
│   ├── create_skill.py               # 从模板生成 Skill
│   ├── validate_skill.py             # 校验 Skill 文件和 JSON 契约
│   ├── run_skill.py                  # 运行时实现
│   └── run_evals.py                  # 评测入口
├── tests/                            # 框架冒烟测试
├── templates/
│   └── skill/                        # 新 Skill 的完整基础模板
└── skills/
    ├── demo-market-snapshot/         # 基础离线示例
    └── rfq-routing-simulator/        # 报价路由与结算状态模拟器
```

每个生成出来的 Skill 包含：

```text
<skill-name>/
├── SKILL.md                          # 触发条件、步骤、工具和边界
├── skill.meta.json                   # 中英文参数定义
├── payload-schema.json               # 输出 JSON 契约
├── scripts/process.py                # 确定性处理器：stdin JSON → stdout JSON
├── fixtures/sample-input.json        # 离线测试输入
├── fixtures/_meta.json               # Fixture 版本和有效期
├── evals/evals.json                  # 最小评测用例
└── review.md                         # 发布前检查记录
```

### 快速开始

```bash
git clone https://github.com/bieberCN/skill-forge.git
cd skill-forge

# 生成一个新的 Skill
./bin/new-skill market-snapshot \
  --title "Market Snapshot" \
  --domain crypto

# 检查生成结果
python3 scripts/validate_skill.py skills/market-snapshot

# 通过统一运行器执行并校验输出
./bin/run-skill skills/market-snapshot \
  --input skills/market-snapshot/fixtures/sample-input.json

# 运行评测用例
PYTHONPATH=. python3 scripts/run_evals.py skills/market-snapshot

# 运行示例 Skill
python3 skills/demo-market-snapshot/scripts/process.py \
  < skills/demo-market-snapshot/fixtures/sample-input.json
```

生成器参数：

```text
new-skill <name>             Skill 名称，只允许小写字母、数字和短横线
--title <title>              展示名称
--domain <domain>            业务领域，例如 crypto、finance、research
--description <description>  Skill 触发描述，可选
--output <directory>         输出目录，默认是 skills/
```

### 创建新 Skill 后的工作流

1. 修改 `skill.meta.json` 中的 `input_schema`，定义中英文参数、类型、默认值和选项。
2. 在 `SKILL.md` 中同步参数说明、触发词、MCP 工具和失败处理方式。
3. 在 `connectors/` 或外部适配层接入数据源；连接器只负责取数。
4. 在 `scripts/process.py` 中实现稳定、可测试的计算逻辑。
5. 将真实数据快照或脱敏样本放入 `fixtures/`，不要把 Token、私钥和用户数据提交到仓库。
6. 更新 `payload-schema.json`，确保下游能够稳定消费输出。
7. 增加 `evals/evals.json` 用例，并运行统一运行器和评测器。
8. 在 `review.md` 中记录 MCP 覆盖率、数据缺口、降级行为和已知限制。

### 交易基础设施示例

`skills/rfq-routing-simulator/` 展示一个安全的 RFQ 后端流程：比较多个流动性源的价格、手续费、滑点和延迟，过滤无效报价，选择最佳有效价格，并输出 `REQUESTED → QUOTED → ROUTED` 状态审计。它不连接钱包、不持有私钥、不提交链上交易，适合作为真实交易系统的架构演示和回归测试样例。

对应的 Dashboard 视觉稿位于 `skills/rfq-routing-simulator/rfq-routing-simulator.html`，持续设计记录位于 `docs/design/`，包括产品流程、视觉规范、架构决策和路线图。

### 输出契约

默认 Payload 至少包含：

```json
{
  "subject": {},
  "headline": {},
  "metrics": [],
  "data_gaps": [],
  "disclaimer": ""
}
```

金融或高风险领域的 Skill 应明确声明数据时效、统计假设、无法覆盖的风险，以及“仅供研究参考”的边界。

### 设计边界

- 不在 `SKILL.md` 中堆放大量实现代码；复杂逻辑放进脚本。
- 不让 Agent 重算脚本已经计算过的数字。
- 不把人工编造的数据当作真实 Fixture。
- 不把研究信号描述成确定性预测。
- 不在仓库中保存 API Token、私钥、账号信息或未脱敏数据。

---

## English

### What is Skill Forge?

Skill Forge is a personal, contract-first toolkit for building reusable AI Agent Skills. It standardizes the files needed for an Agent capability: instructions, parameters, data fixtures, deterministic processing, output contracts, and regression checks.

It is useful for:

- market snapshots and monitoring tools;
- data queries, scoring, screening, and ranking;
- risk alerts, event attribution, and research cards;
- Agent workflows backed by MCP tools, APIs, or local data.

It is not a frontend application, an MCP server, or an automated trading system. It is the reusable capability layer between an Agent and a downstream UI or report.

### Architecture

```text
User request
    ↓
SKILL.md: triggers, parameters, and workflow
    ↓
L1: MCP / API / local data fetch
    ↓
L2: deterministic computation in Python
    ↓
L3: Agent interpretation and data-gap explanation
    ↓
L4: structured JSON payload
    ↓
Frontend, report, or downstream Agent
```

The language model handles intent and explanation; Python handles calculations and assembly. This separation improves reproducibility and reduces format drift.

### Technology and language responsibilities

| Language / format | Responsibility | Main locations |
|---|---|---|
| Python 3 | Generators, validators, data processing, metrics, payload assembly | `scripts/`, `skills/*/scripts/` |
| Bash | Short command-line entry points | `bin/new-skill` |
| JSON | Metadata, fixtures, output contracts, evaluation cases | `*.json` |
| YAML | Agent metadata and readable configuration | `SKILL.md` frontmatter |
| Markdown | Agent instructions, product notes, review records | `SKILL.md`, `review.md`, `README.md` |
| HTML | Optional static UI or interactive prototype | `skills/*/*.html` |

The current version uses only the Python standard library and has no third-party Python dependency.

### Quick start

```bash
git clone https://github.com/bieberCN/skill-forge.git
cd skill-forge

./bin/new-skill market-snapshot \
  --title "Market Snapshot" \
  --domain crypto

python3 scripts/validate_skill.py skills/market-snapshot

python3 skills/demo-market-snapshot/scripts/process.py \
  < skills/demo-market-snapshot/fixtures/sample-input.json
```

### Extension workflow

1. Define bilingual parameters in `skill.meta.json`.
2. Keep triggers, tools, workflow, and failure handling in `SKILL.md`.
3. Add a connector for the data source; keep fetching separate from business calculations.
4. Put deterministic calculations in `scripts/process.py`.
5. Store sanitized, reproducible inputs under `fixtures/`.
6. Keep the downstream output stable through `payload-schema.json`.
7. Add evaluation cases and run the unified runner and evaluator.
8. Record coverage, data gaps, fallbacks, and limitations in `review.md`.

### Trading-infrastructure example

`skills/rfq-routing-simulator/` demonstrates a safe RFQ backend flow: normalize quotes from multiple liquidity sources, account for fees, slippage, and latency, reject invalid or expired quotes, select the best effective price, and emit a `REQUESTED → QUOTED → ROUTED` audit trail. It never connects to a wallet, holds keys, or submits an on-chain transaction.

The visual dashboard is at `skills/rfq-routing-simulator/rfq-routing-simulator.html`. Living product-design records are maintained in `docs/design/`, covering product flow, visual tokens, architecture decisions, and the roadmap.

### License

MIT. Add domain-specific attribution or compliance notes when a new Skill requires them.
