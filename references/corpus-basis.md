# Corpus basis and evidence boundary

## Contents

- [Snapshot](#snapshot)
- [Coverage](#coverage)
- [Repository quality findings](#repository-quality-findings)
- [Deep-reading strata](#deep-reading-strata)
- [Automated textual observations](#automated-textual-observations)
- [Visual observations](#visual-observations)
- [Evidence levels](#evidence-levels)

## Snapshot

This skill was distilled from a 2026-07-24 snapshot of
`qhy991/Awesome-LLM-Kernel-Agent`, plus primary arXiv HTML and figure assets.
The snapshot is evidence for recurring writing patterns, not an exhaustive or
permanent census of the field.

Sources:

- list: <https://github.com/qhy991/Awesome-LLM-Kernel-Agent>
- exemplar HTML requested by the user:
  <https://arxiv.org/html/2606.26383v1>
- official HTML pattern: `https://arxiv.org/html/<arxiv-id>`
- fallback HTML pattern: `https://ar5iv.labs.arxiv.org/html/<arxiv-id>`

## Coverage

- 80 unique arXiv IDs were extracted from the complete README, including the
  traditional-kernel section.
- 70 papers yielded usable official arXiv HTML figures.
- 10 official-HTML failures were retried through ar5iv.
- ar5iv recovered figures for 5 additional papers.
- The analyzed visual corpus therefore covers 75 papers, 645 HTML figure
  groups, and 735 downloaded or extracted image assets.
- Five papers still had no usable HTML figure assets. Do not call the image
  corpus complete; use official PDF/source fallback when those papers matter.

The 735 assets comprise 679 PNG, 53 SVG, and 3 JPEG files. A figure group is
not the same as an asset: 90 groups were HTML-only, 456 contained one asset,
and the remainder were multi-panel or multi-asset groups.

## Repository quality findings

Do not trust list-level counts or tags without checking the underlying rows:

- the structured landscape contains 81 entries;
- its categories are Agent4Kernel 31, LLM4Kernel 20, Benchmarks 17,
  Datasets 7, and Systems/Platforms 6;
- its backend tags are multi-label and strongly CUDA-skewed: CUDA 67,
  Triton 23, NPU 4, HIP 4, Metal 3;
- the README says the methods table contains 66 papers, while the captured
  table has 63 rows;
- one arXiv item appears in two README sections;
- four structured entries disagree with the timeline about the year.

Consequences:

1. deduplicate by canonical arXiv ID;
2. obtain dates from the paper page, not a secondary YAML year;
3. stratify samples so CUDA agent papers do not stand in for the field;
4. treat README tags as retrieval metadata, never definitions.

## Deep-reading strata

The primary deep-reading set covered complementary paper types:

### Foundational evaluation

- `2502.10517` KernelBench
- `2502.14752` TritonBench
- `2509.14279` Robust-KBench
- `2605.04956` KernelBenchX
- `2605.23215` FastKernels
- `2603.19173` SOL-ExecBench

### Model training and RL

- `2507.05687` AutoTriton
- `2602.05885` Dr. Kernel
- `2602.24286` CUDA Agent
- `2606.04847` MusaCoder
- `2606.16497` daVinci-kernel

### Agent and search systems

- `2509.07506` Astra
- `2602.19128` K-Search
- `2604.16625` AdaExplore

### Compiler, verification, and system safety

- `2606.09682` AutoMegaKernel
- `2604.22032` Kernel Contracts
- `2603.24595` Model2Kernel

### Performance analysis

- `2606.26383` SOLAR
- `2605.04467` KEET
- `2602.11506` RooflineBench

The source list also contains traditional kernel/compiler papers. They are
useful for hardware terminology and experimental controls, but their writing
patterns should not be silently merged with agent/RL papers.

## Automated textual observations

Seventy-five usable Introductions were detected in the HTML snapshot.
Lightweight cue matching found:

- a contrast/gap cue in 68;
- an absence/limitation cue in 63;
- a response cue such as “to address” or “we propose” in 63;
- an explicit contribution cue in 55;
- a result cue in 53;
- an evaluation cue in 37.

Among the 63 Introductions containing both gap and response cues, the first gap
cue preceded the first response cue in 61 (96.8%). Among the 46 containing both
response and contribution cues, response preceded contributions in 44 (95.7%).

These are noisy structural measurements, not quality scores. They support the
gap-before-method and method-before-contributions pattern; they do not justify
copying stock phrases or forcing every paper into the same paragraph count.

## Visual observations

Caption-assisted grouping found:

- 98 system-overview assets;
- 189 quantitative-comparison assets;
- 51 dataset/taxonomy assets;
- 47 roofline/SOL assets;
- 30 worked-example assets;
- 24 ablation assets;
- 23 training-process assets;
- 23 scaling assets;
- 5 heatmap assets;
- 245 assets that the lightweight classifier left as other.

The labels are review aids, not ground truth. Direct tool metadata identified
117 Matplotlib assets, 53 LaTeXML/TikZ assets, and 2 Inkscape-tagged assets;
563 had no direct tool evidence. Never infer the authoring tool from visual
appearance alone.

## Evidence levels

Keep these levels separate in all outputs:

1. **Direct evidence**: paper text, caption, table, equation, official source,
   artifact metadata, or author repository.
2. **Structural observation**: section order, panel count, aspect ratio,
   repeated encoding, or visible comparison design.
3. **Supported inference**: a mechanism interpretation consistent with
   ablations, traces, or counterexamples.
4. **Hypothesis**: a plausible explanation that the paper does not test.

Do not upgrade levels 2–4 into author claims.
