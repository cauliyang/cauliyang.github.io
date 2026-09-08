---
title: My TikZ Learning Journey
description: A growing gallery of TikZ diagrams and their LaTeX source, collected while I learn to draw technical figures with TikZ.
categories: ["Writing"]
tags: ["LaTeX", "TikZ"]
date: 2023-06-02
featured: true
draft: false
# image: "https://github.com/cauliyang/learn_tikz/blob/main/gallery/colored_diagram.pdf"
series: ["LaTex Typesetting"]
series_order: 2
---

## Overview

{{< embed-pdf url="./gallery/tikz.pdf" hidePaginator="true" renderPageNum="3" >}}

## Why

LaTeX is the standard typesetting system for scientific and technical documents in academia and industry.
Among its many packages, the one I have been most absorbed in lately is TikZ, a versatile package for drawing detailed, publication-quality diagrams.

This post and the accompanying [open-source repository][repo] are where I collect the TikZ code I write along the way.
The collection grows gradually, and it is meant to show not just the finished figures but the process of learning and experimenting with TikZ.
Whether you are new to LaTeX and TikZ or an experienced user looking for examples, I hope it is useful.

## What is TikZ

TikZ is a high-level drawing language built on top of LaTeX.
It produces complex, precise graphics directly inside a LaTeX document, from simple geometric figures to flowcharts, network diagrams, and logic circuits.
That breadth is also what makes TikZ daunting to learn.

## What to expect from the repository

The repository documents my progress as I go deeper into TikZ: the code, the problems I ran into, and how I solved them.
Over time it should show the progression from simple drawings to more intricate, multi-part diagrams.

I try to annotate the code and explain my reasoning where I can, but the project is a record of self-directed learning rather than a structured course or guide.
Seeing TikZ commands applied to real figures, and how small changes alter the output, is still a practical way to build intuition for the package.
Feel free to take the code, tweak it, and make it your own.

{{< github repo="cauliyang/learn_tikz" >}}

{{< alert icon="circle-info" >}}
This post is updated periodically as my work with TikZ progresses, so check back for new figures and code.
{{< /alert >}}

{{< signoff >}}

<!-- links -->

[repo]: https://github.com/cauliyang/learn_tikz/
