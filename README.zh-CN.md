# paper-agent-skill（中文说明）

[English](README.md) · **中文**

> 一套用 AI agent 迭代严肃 LaTeX 学术论文的**版本化 + 多层校验**工作流——让「源码能编译」永远不被误当成「论文是对的」。

---

## 这是什么

`paper-agent-skill` 是一个 [Agent Skill](https://www.anthropic.com/news/skills)（一个装着「指令 + 脚本 + 参考文档」的文件夹，AI agent 按需加载）。它把**严肃的、多轮的论文迭代**沉淀成一套纪律，而不是一次性的「帮我润色英文」。

核心信念：一篇论文不是待打磨的散文，而是一份 **claim–evidence 契约**。摘要和引言里的每一个声明，都必须能对应到一个真实的方法组件、一个真实的实验产物、一张图或一张表——否则就得下调措辞。这个 skill 的职责，就是让 agent 对这个映射保持诚实，并抓出「编译通过就发」这种粗糙流程会漏掉的缺陷。

## 为什么需要它（要解决的问题）

用 LLM 多轮迭代论文时，有三类反复出现的翻车模式：

1. **表演式严谨**：模型把每个声明都写得滴水不漏、每句话都顺滑，于是悄悄把「可能有用」写成「显著提升」，把「代理指标」写成「业务指标」。
2. **源码干净、成品坏掉**：引用/标签/图表审计全绿，`tectonic` 也没报错，但第 1 页却有一行文字溢出栏宽压到隔壁栏；或者一个表头把合成 proxy 悄悄改名成真实指标。结构检查读的是 `.tex`，从不看渲染出来的页面。
3. **记忆漂移**：改到很多轮之后，模型又把三节前你砍掉的东西端回来，或者和它自己早先写的定义打架。注意力偏向近期上下文，长程一致性得你自己扛。

这个 skill 把**能机械化**的部分做成确定性检查，并把**仍需人判断**的部分明确点名，避免被悄悄跳过。

## 架构

薄路由 + 厚引用 + 确定性脚本 + 回归记忆：

```
paper-agent-skill/
  SKILL.md                     # 薄路由：触发条件、按需加载、红线、模式、工作流
  references/                  # 按需加载，一份一个主题
    manuscript-workflow.md       # 版本恢复、重写模式、结构化工作流
    project-baseline.md          # 按项目填写的基线模板 + 通用 LaTeX 坑
    citation-literature-workflow.md
    figure-table-protocol.md     # 图表设计 + LaTeX 图表 QA
    verification-layers.md       # L1–L6 分层校验模型
    top-conference-review.md     # 顶会清单 + 多审稿人模拟
    iteration-review-template.md # 迭代评审报告模板
    recursive-research-loop.md   # 自包含的递归取证循环
  scripts/                     # 纯标准库 Python，advisory（绝不做硬性 CI 门禁）
    audit_latex_refs.py          # 缺失/未用/重复引用、占位符、过期版本标签
    audit_bib_metadata.py        # BibTeX 条目数 + 缺失 DOI/arXiv/URL 元数据
    audit_figures.py             # 图存在性、caption、label、\Description、被引 label
    audit_claim_language.py      # 扫描正文里的过度声明 / 绝对化 / 因果 / 生产环境措辞
    audit_layout.py              # 编译 + 报告可见的 overfull \hbox，告诉你该渲染哪几页
  evals/                       # 回归记忆：带真实案例的已知故障模式
    citation-hallucination-case.md
    figure-rendering-regression.md
    overclaiming-review-case.md
    layout-overlap-regression.md
```

### 校验层（skill 的核心）

编译通过 + 源码审计全绿是**必要但不充分**的。按顺序跑；即使前面每一层都过，后面某一层仍可能挂：

| 层 | 回答的问题 | 怎么做 | 抓什么 |
|---|---|---|---|
| L1 源码一致性 | 各源文件互相引用对得上吗？ | `audit_latex_refs.py`、`audit_figures.py` | 缺失/未用/重复引用、断裂 label、缺 `\Description` |
| L2 元数据诚实 | 每条引用是真实且完整的吗？ | `audit_bib_metadata.py` + 外部核验 | 编造/不完整的 BibTeX |
| L3 声明措辞 | 正文有没有超出证据的过度声明？ | `audit_claim_language.py` + claim–evidence 矩阵 | 无支撑的 SOTA / 因果 / 生产环境声明 |
| L4 编译 | 能编过吗？ | `tectonic main.tex` | LaTeX 硬错误 |
| **L5 版面（视觉）** | **渲染出来的页面**长得对吗？ | `audit_layout.py` → 再把被标记的页渲染成图片去看 | 栏间重叠、跑飞的长 token、被裁掉的图表 |
| **L6 语义意图** | 表头/坐标轴/caption 的含义和它声称的一致吗？ | 对照证据边界手工通读 | proxy 冒充真实指标、坐标轴标错、caption 漂移 |

L5 和 L6 正是纯源码审计覆盖不到的两层，也正是「0 审计错误」的论文仍然带着可见缺陷发出去的地方。

### 四种工作模式

- **Mode A — 局部修补**：措辞/引用/公式/caption/表格的小改。只打补丁、定向验证、报告残余风险。
- **Mode B — 结构性重写**：定位/新颖性/方法/实验/图系统改动。先锁定一句话贡献、Figure 1 审稿人问题、claim–evidence 矩阵、证据边界；再重写、编译、审计，产出 Iteration Review。
- **Mode C — 算法/架构改动**：tokenizer/模型/loss/serving/baseline/ablation 改动。把每条声明归类为 已实现 / proxy / 提议中 / 未来工作，并对齐 论文↔代码↔runbook，否则下调声明。
- **Mode D — 评审/策略备忘**：不改源码只做批评；结论先行，给出按优先级排序的修复动作。

## 适合谁用（适用性）

**适合**你，如果：

- 你写 **LaTeX** 论文（本项目用 [`tectonic`](https://tectonic-typesetting.github.io/) 构建，测过的文档类是 `acmart`），并且要迭代很多轮。
- 你用的 AI agent 能读文件、跑 shell 命令、渲染 PDF。
- 你在意**工业赛道 / 系统论文的严谨度**（RecSys / CIKM / WWW / KDD 风格），声明诚实、可复现边界、图表正确性比文笔更重要。
- 你希望「已实现 / proxy 实验 / 提议 / 未来工作」这四者的边界被强制区分，而不是被糊在一起。

**不太适合**，如果：

- 你用 Word / Google Docs 写作（版面和审计脚本都假设 LaTeX 源码）。
- 你想要一键「去味/润色」按钮——这个 skill 会刻意拒绝在 claim/evidence 链修好之前做浅层润色。
- 你要一个硬性 CI 门禁——脚本按设计是 **advisory**（只打印结果并 exit 0），因为多数告警需要人来分诊。

## 依赖

- **Python 3**（脚本纯标准库，无需 `pip install`）。
- **tectonic**（或其他 LaTeX 引擎）用于 L4/L5 构建 + overfull 检测。
- L5 渲染核查用的 PDF 光栅化工具：[PyMuPDF](https://pymupdf.readthedocs.io/)（`fitz`）、`pdftoppm` 或 ImageMagick 任一。
- 一个支持 Agent Skills 格式的 AI agent 宿主（本 skill 是宿主无关的 Markdown + Python，不绑定任何厂商）。

## 快速上手

```bash
# 对一个论文版本目录跑确定性审计
python3 scripts/audit_latex_refs.py     /path/to/paper_dir
python3 scripts/audit_bib_metadata.py   /path/to/paper_dir
python3 scripts/audit_figures.py        /path/to/paper_dir
python3 scripts/audit_claim_language.py /path/to/paper_dir
python3 scripts/audit_layout.py         /path/to/paper_dir --threshold 12

# 然后：编译，并把 audit_layout 标记的页渲染成图片亲眼看（L5），
# 再对照证据边界通读每一个表头 / 坐标轴标签 / caption（L6）。
```

脚本假设论文目录里有 `main.tex`（含 `\documentclass`）、各章节 `.tex` 文件、以及一个 `.bib`。`audit_layout.py` 有 `tectonic` 就调用它，否则解析已有的 `.log`。

## 局限与已知问题

诚实清单——信任它之前先读：

1. **是 advisory，不是证明**：脚本只覆盖**客观可查的一个子集**。跑绿只代表「没有机械红旗」，不代表「论文正确」。L5/L6 仍需人/agent 真的去看渲染页、读 caption。
2. **正则级检查**：引用/标签/声明检测是模式匹配。可能漏掉格式刁钻的 `\cite`、非常规的 float 结构、或词表之外的过度声明；也可能误报（比如一个本就合理重复的技术术语）。每个命中都当「去确认」，不是「去删」。
3. **工具链假设**：`acmart` + `tectonic` 是测过的路径，其他文档类/引擎可能要调。`audit_layout.py` 的 overfull 阈值（12pt）是启发式，小的 overfull 往往不可见。
4. **是占位符，不是自动探测**：`SKILL.md` 和 `references/project-baseline.md` 里的路径是 `<workspace>` / `<paper-root>` 占位符，需你自己填；skill 不会自动发现你的论文目录结构。
5. **示例领域是推荐系统**：文中的示例（tokenizer / Semantic-ID / 效用头）只是举例、不是约束——换成你自己的架构即可。方法论与领域无关，示例才有领域色彩。
6. **尚无打包测试**：这是一份可用的抽取版，不是硬化的库。脚本纯标准库且自检，但还没有测试套件——当作依赖前先加 smoke test。

## 配置（按你的项目填）

skill 出厂即已去身份、通用；用之前先指向你自己的论文：

- 在 `SKILL.md` → *Quick Target Defaults* 里，把 `<workspace>` / `<paper-root>` / `<reports-dir>` 换成你的真实目录。
- 复制 `references/project-baseline.md`，填入你论文的当前状态、定位、证据边界。
- 在 `SKILL.md` 里设定你的 *Default Evidence Stance*（论文是什么/不是什么、哪些已验证 vs 仅提议）。
- 可选：把你尚未实现的扩展名字加进 `scripts/audit_claim_language.py` 的 `PROJECT_EXTENSION_TERMS`，一旦被当成已实现来写就会被标出。
- 若你的文档类/页边距和 `acmart` 不同，调 `audit_layout.py --threshold`。

## License

MIT —— 见 [LICENSE](LICENSE)。

## 由来

抽取自一个长期迭代的个人论文 skill。分层校验这个想法，源于一次真实事故：所有源码审计都通过，渲染出的 PDF 却仍然栏间重叠——见 `evals/layout-overlap-regression.md`。
