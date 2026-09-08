---
title: Efficient Genomic Interval Search With a SIMD-Enhanced COITree
description: I ported COITree's SIMD path from AVX2 to ARM NEON in Rust and benchmarked it against BEDTools, AIList, and Bedtk on GA4GH interval data.
categories: ["Bioinformatics", "Algorithms"]
tags: ["Rust", "Performance"]
date: 2023-03-12
featured: true
draft: false
---

{{< katex >}}

## Background

Bioinformatics researchers routinely work with many kinds of genomic data: DNA sequencing, RNA sequencing, and epigenetic assays among them.
Much of that work comes down to manipulating genomic intervals, which is central to understanding the genetic basis of disease and to identifying therapeutic targets.
A genomic interval is a region spanning a start and an end position; it can represent a gene, a regulatory element, or any other functional element of the genome.
One primary application is the analysis of ChIP-seq data, where interval operations let us integrate ChIP-seq peaks with other data types such as gene expression and genetic variation.
This integration gives a more complete picture of biological processes and of how they contribute to normal development or disease.
Integrating these data types into a single data structure is challenging, however, especially for large datasets.

The Cache Oblivious Interval Tree (COITree) is a good fit for this problem.
It stores intervals in contiguous memory and uses an in-order van Emde Boas layout, so the tree is arranged to minimize cache misses during traversal and to answer queries quickly.
Even so, COITree still hits performance bottlenecks on large datasets.
One way to relieve that bottleneck is Single Instruction Multiple Data (SIMD) processing, which is designed for vector operations.
My hypothesis was that adding SIMD support would be a viable way to speed up genomic interval analysis.

## Transitioning from AVX2 to NEON

The existing SIMD path in COITree targets AVX2, which is not available on ARM64.
NEON is the SIMD instruction set of the ARM64 architecture: it executes a single instruction on multiple pieces of data at once, which can yield significant speedups.
Porting the SIMD path to NEON makes the optimized COITree usable on ARM64 machines and reduces the computational resources needed for large datasets.

## Results

To evaluate the benefit of NEON in COITree, I benchmarked the implementation with and without NEON and compared it against existing tools: BEDTools (Quinlan and Hall, 2010), Augmented Interval List (AIList), and Bedtk.
The evaluation task is the interval search problem, which is fundamental to genomic data analysis.
For benchmarking data, I used stratification BED files from the Global Alliance for Genomics and Health (GA4GH) Benchmarking effort.
Comparing COITree with NEON against state-of-the-art tools tells us whether this approach significantly improves the speed and efficiency of genomic data analysis.

A genomic interval \\(r\\) is defined by two coordinates that represent the start and end of a feature on a chromosome.
The general interval search problem is defined as follows (Feng et al., 2019):

Given a set of \\(N\\) intervals \\(R = \\{r_1, r_2, \dots, r_N\\}\\) where \\(N \gg 1\\), and a query interval \\(q\\), find the subset \\(S\\) of \\(R\\) that intersects \\(q\\).
If all intervals are half-open, \\(S\\) can be written as:

$$
S(q) = \{\, r \in R \mid r.\text{start} < q.\text{end} \wedge r.\text{end} > q.\text{start} \,\}
$$

I implemented the optimized COITree in Rust.
To evaluate its performance, I used two genomic interval datasets (A and B) from GA4GH.
Datasets A and B contain 4,816,112 and 44,426,501 genomic intervals, respectively.
I compared the implementation with and without NEON instructions, and against BEDTools (v2.30.0), AIList (v0.1.1), and Bedtk (v0.0-r25dirty).
Every interval in dataset A was queried against dataset B, yielding a total of 35,032,849 overlapping intervals.
Because BEDTools and Bedtk are general-purpose toolkits, I used the `coverage` subcommand of BEDTools and the `cov` subcommand of Bedtk to find overlapping intervals; the other tools are built specifically for this problem and need no subcommand.
I used [hyperfine](https://github.com/sharkdp/hyperfine), a command-line benchmarking tool, to measure runtime.

Each tool was given three warm-up runs and then executed ten times.
All experiments ran on a computer with macOS 12.6 (ARM64) and 32 GB of memory.
On the sorted dataset, the optimized COITree outperformed every other tool, as shown in Table 1.

Table 1: Runtime of each tool on the sorted dataset

| Command                           | Mean [s] | Min [s] | Max [s] | Relative |
| --------------------------------- | -------- | ------- | ------- | -------- |
| coitree-default                   | 4.36     | 4.28    | 4.44    | 1.24     |
| coitree-neon                      | **3.53** | 3.50    | 3.57    | **1.00** |
| ailist                            | 5.63     | 5.54    | 5.87    | 1.59     |
| bedtk cov                         | 4.70     | 4.67    | 4.75    | 1.33     |
| bedtools coverage -counts -sorted | 13.48    | 13.40   | 13.64   | 3.82     |

Table 2: Runtime of each tool on the unsorted dataset

| Command                   | Mean [s] | Min [s] | Max [s] | Relative |
| ------------------------- | -------- | ------- | ------- | -------- |
| coitree-neon              | **5.46** | 5.43    | 5.50    | **1.00** |
| coitree-default           | 6.41     | 6.35    | 6.44    | 1.17     |
| ailist                    | 6.49     | 6.48    | 6.49    | 1.19     |
| bedtk cov                 | 7.11     | 6.97    | 7.18    | 1.30     |
| bedtools coverage -counts | 256.08   | 244.48  | 276.65  | 46.88    |

Sorted input simplifies the problem, so the sorted benchmark may understate the differences between tools.
I therefore shuffled dataset B and repeated the experiment.
As Table 2 shows, the optimized COITree again performed best, running roughly 46 times faster than BEDTools.
NEON delivers a substantial improvement, especially on unsorted data, and the gains grow with dataset size.

## Conclusion

Adding SIMD instructions to COITree significantly improves its performance.
The same strategy applies to other data structures and offers a general route to faster algorithms for genomic data analysis.
The complete Rust implementation is open source:

{{< github repo="cauliyang/coitrees" >}}

For more details, see my [presentation slides](https://yangyangli.top/coitree-slide.html) on this work.

## References

Feng, J., Ratan, A., & Sheffield, N. C. (2019). Augmented interval list: A novel data structure for efficient genomic interval search. *Bioinformatics*, 35(23), 4907–4911.

Quinlan, A. R., & Hall, I. M. (2010). BEDTools: A flexible suite of utilities for comparing genomic features. *Bioinformatics*, 26(6), 841–842.

{{< signoff >}}
