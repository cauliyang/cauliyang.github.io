---
title: Efficient Genomic Interval Search Using SIMD-Enhanced COITree
description: High-performance interval tree implementation leveraging SIMD instructions for faster genomic data analysis.
tags: ["Rust", "Algorithm", "Bioinformatics", "Performance"]
date: 2023-03-12
featured: true
draft: false
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
It stores the intervals in contiguous memory and employs in-order van Emde Boas layout to enhance query performance.
The tree is designed to optimize cache performance by reducing the number of cache misses during traversal.
However, COITree still suffer from performance bottlenecks, particularly when dealing with large datasets.
One approach to addressing this bottleneck is to use Single Instruction Multiple Data (SIMD), which is optimized for vector operations, to improve the performance of COITree.
Thus, I hypothesize that the approach is a viable solution for improving the speed and efficiency of genomic interval analysis.

## Transitioning from AVX2 to NEON

The NEON instruction set is a specialized SIMD instruction set available in ARM64 architecture that enables Single Instruction Multiple Data processing.
It facilitates executing a single instruction on multiple pieces of data simultaneously, resulting in significant performance improvements.
This feature enables more accurate and comprehensive analyses of large-scale genomic data, leading to novel insights into the genetic basis of diseases and the development of more effective treatments.
Furthermore, it reduces computational resource requirements, which is especially important when processing large datasets.
By developing an optimized COITree implementation, we address a critical need in bioinformatics for faster and more efficient methods of analyzing genomic data.

## Results

To evaluate the performance benefits of using the NEON instruction set in COITree, I conducted benchmarking tests with and without NEON, as well as comparisons with existing tools including BEDTools (Quinlan and Hall, 2010), Augmented Interval List, and Bedtk.
The evaluation task involves the interval search problem, which is fundamental to genomic data analysis.
For benchmarking data, I used stratification BED files from the Global Alliance for Genomics and Health (GA4GH) Benchmarking.
By comparing the effectiveness of COITree with NEON instructions against state-of-the-art tools, we can determine whether this approach significantly enhances the speed and efficiency of genomic data analysis.

A genomic interval \\(r\\) is defined by two coordinates that represent the start and end locations of a feature on a chromosome.
The general interval search problem is defined as follows (Feng, 2019):

Given a set of \\(N\\) intervals \\(R = \\{r_1, r_2, \dots, r_N\\}\\) where \\(N \gg 1\\), and a query interval \\(q\\), find the subset \\(S\\) of \\(R\\) that intersects \\(q\\).
If we define all intervals to be half-open, \\(S\\) can be represented as:

$$
        S(q) = \\{ r \in  R \\;| \\; (r.start < q.end \wedge r.end > q.start)\\}
$$

I implemented the optimized COITree in Rust.
To evaluate its performance, I used two genomic interval datasets (A and B) from GA4GH.
Datasets A and B contain 4,816,112 and 44,426,501 genomic intervals, respectively.
I compared the performance with and without NEON instructions, as well as against existing tools including BEDTools (v2.30.0), Augmented Interval List (v0.1.1), and Bedtk (v0.0-r25dirty).
I queried every genomic interval from dataset A against dataset B, resulting in a total of 35,032,849 overlapping genomic intervals.
Since BEDTools and Bedtk provide enriched features, I used the `coverage` subcommand of BEDTools and the `cov` subcommand of Bedtk to find overlapping intervals.
Other tools are specifically designed for this problem, so no subcommands were required.
I used [hyperfine](https://github.com/sharkdp/hyperfine), a command-line benchmarking tool, to evaluate the performance.

For each tool, I performed three warm-up runs before executing it ten times.
All experiments were run on a computer with macOS 12.6 (ARM64 architecture) and 32 GB of memory.
For sorted datasets, the optimized COITree outperformed all other tools, as shown in Table 1.

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

Since sorted datasets reduce the complexity of the problem, significant speedups may not be apparent.
Therefore, I shuffled interval dataset B and repeated the experiment.
As shown in Table 2, the optimized COITree demonstrated the best performance, achieving approximately 46× speedup compared to BEDTools.
These results demonstrate substantial performance improvements when using the NEON instruction set, especially on unsorted datasets.
The tests also showed that performance gains were particularly noticeable when working with large datasets.

## Conclusion

Incorporating SIMD instructions in COITree significantly enhances its performance.
This optimization strategy can be applied to other data structures, providing a general approach to performance improvement.
By leveraging specialized instruction sets such as NEON, we can achieve more efficient and performant algorithms for genomic data analysis.
The optimized COITree empowers researchers to analyze genomic data more efficiently and effectively.
The complete implementation in Rust is freely available as open source.

{{< github repo="cauliyang/coitrees"  >}}

For more details, check out my [presentation slides](https://yangyangli.top/coitree-slide.html) on this work.

## References

Feng, J., Ratan, A., & Sheffield, N. C. (2019). Augmented interval list: A novel data structure for efficient genomic interval search. *Bioinformatics*, 35(23), 4907–4911.
