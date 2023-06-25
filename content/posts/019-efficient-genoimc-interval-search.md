---
title: Efficient Genomic Interval Search Using SIMD-Enhanced COITree
description: Fast implementation of intervel tree.
tags: ["Rust", "Algorithm", "Bioinformatics"]
date: 2023-03-12
featured: false
draft: false
image: "https://raw.githubusercontent.com/lecepin/rust-logo/main/images/1660287876916.jpeg"
bibFile: data/bib/019-support-arm-for-coitrees-bibliography.json
---

{{< katex >}}

## Background

In bioinformatics, researchers frequently analyze various types of genomic data, such as DNA sequencing data, RNA sequencing data, and epigenetic data.
Manipulating genomic intervals is a crucial task in comprehending the genetic basis of diseases and identifying potential therapeutic targets.
Genomic intervals are defined as regions that span from a starting position to an ending position and can encompass genes, regulatory elements, and other functional elements of the genome.
One primary application of genomic interval manipulation is analyzing ChIP-seq data.
Moreover, manipulating genomic intervals allows for the integration of ChIP-seq data with other genomic data types, such as gene expression and genetic variations.
This integration provides a more comprehensive understanding of biological processes and their contribution to normal development or disease.
However, integrating these data types into a single data structure can pose challenges, especially when handling large datasets.
Cache Oblivious Interval Trees (COITree), with cache-oblivious design and efficient query algorithms, have the potential to handle and integrate multiple types of genomic data into a single data structure.
It stores the intervals in contiguous memory and employs in-order van Emde Boas layout to enhance query performance {{<cite  vanEmdeBoas1976Dec >}}.
The tree is designed to optimize cache performance by reducing the number of cache misses during traversal {{<cite  vanEmdeBoas1977Jun >}}.
However, COITree still suffer from performance bottlenecks, particularly when dealing with large datasets.
One approach to addressing this bottleneck is to use Single Instruction Multiple Data (SIMD), which is optimized for vector operations, to improve the performance of COITree.
Thus, I hypothesize that the approach is a viable solution for improving the speed and efficiency of genomic interval analysis.

## How transfer avx2 to neon

Neon instruction set is a specialized instruction set available in arm64 architecture that enables Single Instruction Multiple Data (SIMD) processing.
It facilitates executing a single instruction on multiple pieces of data simultaneously, resulting in a significant performance improvement.
This feature enables more accurate and comprehensive analyses of large-scale genomic data, leading to novel insights into the genetic basis of diseases and the development of more effective treatments.
Furthermore, it can reduce the need for computational resources, which is especially important in processing large datasets.
Overall, I intend to develop optimized COITree to address a critical need in bioinformatics for faster and more efficient methods of analyzing gnomic data.

## Result

To evaluate the performance benefits of using neon instruction set in COITree, I will conduct bench-marking tests with and without the neon instruction set, as well as existing tools including BEDTools (Quinlan and Hall, 2010), Augmented interval list {{<cite  Feng2019Dec    >}}, and Bedtk {{<cite  Li2021May  >}}.
The evaluation task involves interval search problem that is fundamental to genomic data analysis.
For benchmarking data, I will use stratification BED files from the Global Alliance for Genomics and Health (GA4GH) Benchmarking {{<cite  Krusche2019May  >}}.
By comparing the effectiveness of COITree with neon instruction set against state-of-the-art tools, we can determine whether this approach can significantly enhance the speed and efficiency of genomic data analysis

A genomic interval $r$ is defined by two coordinates that represent the start and end locations of a feature on a chromosome.
The general interval search problem is defined as follows {{<cite   Feng2019Dec >}}.

Given a set of $ N $ intervals in a $R = {r_1, r_2, \dots,r_N} \; for \; N \gg 1 $, and a query interval $ q $, find the subset of $ S $ of $ R $ that intersect q.
If we define all intervals to be half-open, $ S $ can be represented as:

$$
        S(q) = \{ r \in R | (r.start < q.end \wedge r.end > q.start)\}
$$

I have implemented the optimized COITree in Rust.
To evaluate its performance, I used two genomic interval datasets A and B from GA4GH.
Dataset A and B contain 4816112 and 44426501 genomic intervals, respectively.
I compared the performance with and without the neon instruction set as well as existing tools including BEDTools (v2.30.0), Augmented interval list (v0.1.1), and Bedtk (v0.0-r25dirty).
I query every genomic interval of dataset A on dataset B, and the total overlapping genomic intervals is 35 032 849.
As BEDTools and bedtk provide enrich features, I used subcommand coverage of BEDTools and subcommand cov of Bedtk to find overlapping intervals.
Other tools are designed to the problem so that I do not need to use subcommand.
I used hyperfine {{<cite  Peter2022  >}}, which is command-line benchmarking tool, to evaluate the performance.

For each tool, I warmed up the tool three times before executing it ten times.
All experiments were run on a computer with macOS 12.6.6.3 2 21G320 arm64 and 32 GB of memory.
In the case of sorted datasets, the optimized COITree outperformed all other tools, as shown in Table 1.

Table 1: Runtime of tools on the sorted dataset

| Command                           | Mean [s] | Min [s] | Max [s] | Relative |
| --------------------------------- | -------- | ------- | ------- | -------- |
| coitree-default                   | 4.36     | 4.28    | 4.44    | 1.24     |
| coitree-neon                      | **3.53** | 3.50    | 3.57    | **1.00** |
| ailist                            | 5.63     | 5.54    | 5.87    | 1.59     |
| bedtk cov                         | 4.70     | 4.67    | 4.75    | 1.33     |
| bedtools coverage -counts -sorted | 13.48    | 13.40   | 13.64   | 3.82     |

Table 2: Runtime of tools on the unsorted dataset

| Command                   | Mean [s] | Min [s] | Max [s] | Relative |
| ------------------------- | -------- | ------- | ------- | -------- |
| coitree-neon              | **5.46** | 5.43    | 5.50    | **1.00** |
| coitree-default           | 6.41     | 6.35    | 6.44    | 1.17     |
| ailist                    | 6.49     | 6.48    | 6.49    | 1.19     |
| bedtk cov                 | 7.11     | 6.97    | 7.18    | 1.30     |
| bedtools coverage -counts | 256.08   | 244.48  | 276.65  | 46.88    |

Since sorted datasets reduce the complexity of the problem, we may not observe a relatively significant speedup.
Therefore, I shuffled interval dataset B and repeated the experiment.
As shown in Table 2, the optimized COITree demonstrated the best performance, and was about 46 times faster than BEDTools.
Our results demonstrate a substantial performance improvement when using the Neon instruction set, especially on unsorted datasets.
The tests also showed that the performance gain was particularly noticeable when working with large datasets.

In conclusion, incorporating SIMD in COITree can significantly enhance its performance.
This strategy can also be applied to other data structures, providing a way to optimize performance.
By leveraging the power of specialized instruction sets such as Neon, we can achieve more efficient and performant algorithms.
The optimized COITree will empower researchers to mine genomics data more ergonomically and efficiently.
The code for optimized implementation in Rust is freely available on both https://github.com/cauliyang/coitrees/tree/avx.

I also gave a presentation for the work if you are interested in that please
check the [slides](https://yangyangli.top/coitree-slide.html).

## Reference

{{< bibliography cited >}}
