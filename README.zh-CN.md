# LLM Kernel Paper Writing

**面向 LLM 驱动 GPU Kernel 系统的证据约束科研写作 Skill。**

[English](README.md) · [Skill](SKILL.md) ·
[完整案例](EXAMPLES.md) · [语料边界](references/corpus-basis.md)

LLM Kernel Paper Writing 是一个开放的 Agent Skill 和小型确定性工具链。它把
代码、实验、日志、论文和图表等研究材料组织为有边界的研究主张、可追溯术语、
匹配的实验比较和完整论文逻辑。

它适用于 CUDA、Triton、HIP、Metal、NPU Kernel，Kernel 生成 Agent 与搜索
系统，SFT/RL，Benchmark/Dataset，编译与验证，以及性能分析论文。

核心原则是：**从 claim-evidence ledger 写论文，而不是依赖模型记忆补全。**

## 包含内容

- [`SKILL.md`](SKILL.md) 中的完整写作工作流；
- 对齐摘要、Introduction、Related Work、贡献与结论的四句 argument checksum；
- 与实验比较协议分离的 nearest-neighbor 文献定位矩阵；
- 模型训练、Agent/Search、编译与验证、Benchmark、性能分析五类 playbook；
- Paper Contract 和严格的 claim-evidence ledger；
- canonical concept、proper name、author-defined construct、metric 与
  claim language 的术语分类；
- 从比较协议出发的实验表格与科研图表组织规则；
- 基于 arXiv HTML 的证据提取器，保留章节位置、caption、上下文、哈希和
  candidate 状态；
- 在写正文前阻止缺失范围、基线、证据或限制项的确定性校验器；
- 在保留必要科学边界的同时，清理防御性 AI 文风的宏观优先审计；
- 公开语料清单和基于一手 arXiv 来源的完整案例。

## 工作流

```text
研究材料
  -> Paper Contract
  -> 判断 / 证据缺口 / 处理方式 / 核心发现 checksum
  -> 一手来源证据
  -> 文献 positioning matrix
  -> claim / term / 实验 comparison ledgers
  -> 论文论证链
  -> 表格与图片计划
  -> 有边界的正文
  -> 投稿前审计
```

## 安装为 Agent Skill

```bash
git clone https://github.com/qhy991/llm-kernel-paper-writing.git \
  ~/.agents/skills/llm-kernel-paper-writing

python3 -m pip install -r \
  ~/.agents/skills/llm-kernel-paper-writing/requirements.txt
```

之后让 Agent 使用 `llm-kernel-paper-writing`。

## 快速开始

把模板复制到论文工程：

```bash
cp assets/paper-contract.json path/to/paper/paper-contract.json
cp assets/evidence-ledger.json path/to/paper/evidence-ledger.json
```

填写后执行严格校验：

```bash
python3 scripts/validate_evidence_ledger.py \
  path/to/paper/evidence-ledger.json --strict
```

空白模板本来就应当失败。仓库提供了可以通过严格校验的 SOLAR 示例：

```bash
python3 scripts/validate_evidence_ledger.py \
  assets/example-solar-ledger.json --strict
```

## 从 arXiv HTML 提取证据

需要固定论文版本时，传入带版本号的 arXiv ID：

```bash
python3 scripts/extract_arxiv_evidence.py \
  --id 2606.26383v1 \
  --output-dir evidence-output/solar \
  --download-images
```

也可以读取含多篇论文链接的 Markdown：

```bash
python3 scripts/extract_arxiv_evidence.py \
  --readme path/to/papers.md \
  --output-dir evidence-output/corpus
```

提取器生成的是**需要人工核验的候选证据**，不是自动成立的论文事实或术语定义。
输出会保留来源位置和状态，只有检查原文上下文后才能写入最终论文。

## 语料与版权边界

该 Skill 来自 2026-07-24 的
[Awesome-LLM-Kernel-Agent](https://github.com/qhy991/Awesome-LLM-Kernel-Agent)
快照和一手 arXiv HTML：

- 请求了 80 个唯一 arXiv ID；
- 70 篇通过官方 arXiv HTML 获得图片；
- ar5iv 补充恢复了 5 篇；
- 最终可分析语料为 75 篇论文、645 个 figure group、735 个图片资产。

这些数字只是固定时间点的语料范围，不是完整领域统计或论文质量排名。具体见
[`assets/corpus-manifest.json`](assets/corpus-manifest.json) 和
[`references/corpus-basis.md`](references/corpus-basis.md)。

仓库不会重新发布下载的论文 HTML 或图片。需要本地证据时，应使用提取器从
一手来源重新获取。

## 开发与验证

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py tests/*.py
ruff check scripts tests
```

## 配套项目

[Scientific Figure Design](https://github.com/qhy991/Scientific-Figure-Design)
负责从 Figure Contract 到可编辑 Draw.io、统一配色、矢量导出和终稿视觉验证；
本仓库负责主张、证据、术语、实验比较和论文逻辑。两者可以组合使用。

## 许可证

仓库原创内容使用 [MIT License](LICENSE)。论文标题、方法名称和来源引用仍归
相应作者与出版方所有。
