# Figure rhetoric: figures as evidence interfaces

## Contents

- [Corpus observations](#corpus-observations)
- [Argument sequence](#argument-sequence)
- [Figure roles](#figure-roles)
- [Caption contract](#caption-contract)
- [Claim-evidence planning table](#claim-evidence-planning-table)
- [Common failures](#common-failures)
- [HTML and atlas integrity](#html-and-atlas-integrity)
- [Final audit](#final-audit)

## Corpus observations

The analyzed corpus contains 75 papers with usable HTML figure assets, 645
figure groups, and 735 image assets. Caption-assisted classes include 98
system-overview assets, 189 quantitative-comparison assets, 51
dataset/taxonomy assets, 47 roofline/SOL assets, 30 worked examples, 24
ablations, and 23 training-process assets.

Figure 1 is not a fixed template. Among 70 official-HTML Figure 1 groups,
automatic caption classification found:

- 37 system overviews (52.9%);
- 11 quantitative results (15.7%);
- 10 other;
- 5 worked examples;
- 2 roofline;
- 2 training;
- 1 ablation;
- 1 dataset/taxonomy;
- 1 scaling.

The labels are navigation aids, not ground truth. Select Figure 1 by the first
belief the Introduction must establish.

## Argument sequence

A strong paper often uses:

`motivation/headline → mechanism/state/feedback → worked example → anchored
main result → scaling/ablation → failure taxonomy/boundary`

Not every paper needs every figure, but every core claim needs an evidence
object and every figure needs one primary claim.

## Figure roles

### Motivated example or teaser

Answer: why is the current situation inadequate, and why should the reader keep
reading?

Strong forms:

- before/failure/ours triptych;
- measured runtime versus analytical bound;
- benchmark task contract;
- one counterexample that exposes the gap;
- compact headline result with a visible baseline.

SOLAR Figure 1 (`2606.26383`) uses headroom, bound tightness, and coverage
panels before the first Introduction paragraph. It is a claim map, not a method
diagram.

### Method overview

Show the causal spine:

- inputs and outputs;
- state before and after each stage;
- control decisions;
- execution, correctness, and profiling feedback;
- persistent memory or archive;
- stopping and candidate selection.

K-Search Figure 1 (`2602.19128`) shows open/closed search-tree state and
Insert/Update/Prune. AdaExplore Figure 2 (`2604.16625`) separates Adapt from
Explore. The prose can then follow these state transitions.

Do not draw every implementation dependency. A box without an input, output,
decision, or state change is a label, not a mechanism.

### Worked example

Use:

`source/problem → intermediate representation or decision → generated
artifact/result → validation`

Show only the relevant code or tensor layout. Name the invariant or bottleneck
that changes. A screenshot of hundreds of code lines is not a worked example.

### Main quantitative result

Install a visual anchor before data:

- `1×` relative baseline;
- measured-equals-predicted diagonal;
- peak or roofline;
- threshold;
- full-method curve;
- original point versus optimized point.

State correctness filtering, hardware, precision, workload, budget, aggregation,
and good direction. Separate compile, execution, semantic correctness, and
speed.

### Scaling

The x-axis is the real resource: candidates, turns, tokens, profiler calls,
wall time, or training compute. Show saturation, variance, and cost. Separate
last-turn from best-history.

### Ablation

An ablation is an intervention on a mechanism hypothesis:

- hold task, hardware, model, sampling, and budget fixed;
- compare full method with one meaningful removal or replacement;
- prefer budget curves when a component changes exploration dynamics;
- report repeats and uncertainty;
- discuss interactions and reversals.

AlphaEvolve Figure 8 (`2506.13131`, ar5iv fallback) compares full and removal
variants across compute budget with uncertainty. This reveals convergence
dynamics that a final-value bar would hide.

### Failure taxonomy and boundary

Use failures to establish why a safeguard is necessary:

`reproducible failure → taxonomy/counterexample → protection mechanism →
before/after change`

Define:

- denominator and sample count;
- whether categories are mutually exclusive;
- compile, runtime, correctness, tolerance, performance regression, or exploit;
- count and percentage;
- model/task/hardware grouping.

Sorted stacked bars usually support cross-group comparison better than pies.
SOL-ExecBench (`2603.19173`) and KernelCraft (`2603.08721`) provide useful
examples of exploit/error composition.

## Caption contract

A self-contained caption states:

1. the question or claim;
2. conditions and analysis unit;
3. panel mapping;
4. visual encoding and baseline;
5. metric direction and denominator;
6. repeats, uncertainty, or why they do not apply;
7. the narrow conclusion.

Template:

> **[Claim/question].** Under [workload, hardware, precision, budget], we compare
> [objects] using [metric and denominator]. (a) ...; (b) ... . [Encoding] denotes
> [meaning], and [anchor] marks [reference]. Values are [aggregation] over
> [repeats]; [uncertainty] shows [definition]. The figure supports [conclusion]
> within [boundary].

Avoid captions that stop at “Overview,” “Performance comparison,” “Ablation
study,” or “Training reward.”

## Claim-evidence planning table

| Claim | Reader question | Evidence | Figure | Main-text location |
|---|---|---|---|---|
| search mechanism fixes a bottleneck | where does prior search fail? | trace/counterexample | motivation | Introduction |
| component changes behavior | how does state update? | transitions/feedback | method | Method |
| method is faster | versus what and where? | anchored performance | result | Main Results |
| component causes gain | what if it is removed? | matched intervention | ablation | Main text |
| verifier is necessary | what exploit appears without it? | example + taxonomy | failure | Method/Analysis |

## Common failures

- giant per-task bars dilute the headline;
- code collages become unreadable at publication width;
- system diagrams show all modules but hide feedback and decisions;
- quantitative plots omit `1×`, a diagonal, a bound, or a full-method anchor;
- ablations list configurations without a mechanism hypothesis;
- captions omit repeats and uncertainty;
- diagnostic panels are detached from their shared caption and checkpoint;
- success, correctness, and speed are collapsed into “performance.”

## HTML and atlas integrity

Treat the HTML `<figure>` and its caption as the logical unit:

- one printed figure may contain several PNG/SVG assets and an HTML table;
- local file numbering may not match the printed Figure number;
- transparent PNGs may be unreadable on an arbitrary preview background;
- standalone SVG export may lose CSS, fonts, or HTML subpanels;
- successful conversion does not establish visual correctness.

Store:

- paper ID;
- printed figure label;
- HTML figure ID;
- caption;
- containing section and first body reference;
- ordered asset list;
- source URL and hashes;
- whether a preview is original, reconstructed, or annotated.

Render transparent assets on a white background for review while preserving
the original alpha file. Visually inspect all converted SVGs and reconstructed
multi-panel figures.

## Final audit

- Can a reader state the claim and good direction in five seconds?
- Does the figure define the baseline or bound?
- Is one primary claim visually dominant?
- Does the prose explain the decisive geometry or intervention?
- Are conditions and uncertainty self-contained?
- Does a negative subgroup remain visible?
- Is the caption narrower than the evidence rather than broader?
