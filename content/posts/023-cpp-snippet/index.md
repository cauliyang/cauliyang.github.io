---
title: Code Snippets I Keep Reaching For
description: A growing reference of small, reusable C++, Rust, Python, and shell snippets that I keep copying between projects.
categories: ["Software Development"]
tags: ["C++", "Rust"]
date: 2022-09-22
lastmod: 2023-10-04
featured: false
draft: false
---

This is my personal scratchpad of snippets that I keep looking up: mostly C++, with a few Rust, Python, shell, and LaTeX entries mixed in.

## Generate random numbers with the standard library

Seed a Mersenne Twister from `std::random_device` and draw from a uniform distribution; this is the modern replacement for `rand()`.

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <random>

int main() {
  std::random_device rd;
  std::mt19937 rng(rd());
  std::uniform_int_distribution<int> dist6(1, 6);
  std::generate_n(std::ostream_iterator<int>(std::cout, " "), 10,
                  [&dist6, &rng]() { return dist6(rng); });
  return 0;
}
```

## Generate a random integer in a range with rand()

When you are stuck with `std::rand()`, this maps its output evenly onto `[min, max]` without the modulo bias.

```cpp
// Generate a random number between min and max (inclusive)
// Assumes std::srand() has already been called
// Assumes max - min <= RAND_MAX
int getRandomNumber(int min, int max)
{
    static constexpr double fraction { 1.0 / (RAND_MAX + 1.0) };  // static used for efficiency, so we only calculate this value once
    // evenly distribute the random number across our range
    return min + static_cast<int>((max - min + 1) * (std::rand() * fraction));
}
```

## Recover from a failed input extraction

After a failed `std::cin >> x`, the stream stays in an error state; clear it and discard the rest of the line before reading again.

```cpp
if (std::cin.fail()) // has a previous extraction failed or overflowed?
{
    // yep, so let's handle the failure
    std::cin.clear(); // put us back in 'normal' operation mode
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // and remove the bad input
}
```

## Compare floating-point numbers

Combine an absolute epsilon (for values near zero) with Knuth's relative comparison to test whether two doubles are approximately equal.

```cpp
#include <algorithm>
#include <cmath>

bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    double diff{ std::abs(a - b) };
    if (diff <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return (diff <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}
```

## Measure elapsed time

A minimal stopwatch built on `std::chrono::steady_clock` that reports elapsed seconds as a double.

```cpp
#include <chrono> // for std::chrono functions

class Timer
{
private:
	// Type aliases to make accessing nested type easier
	using clock_type = std::chrono::steady_clock;
	using second_type = std::chrono::duration<double, std::ratio<1> >;

	std::chrono::time_point<clock_type> m_beg { clock_type::now() };

public:
	void reset()
	{
		m_beg = clock_type::now();
	}

	double elapsed() const
	{
		return std::chrono::duration_cast<second_type>(clock_type::now() - m_beg).count();
	}
};
```

## Python script header

The shebang and module docstring I start every Python script with.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: YangyangLi
@contact: yangyang.li@northwestern.edu
@version: 0.0.1
@license: MIT Licence
@file: cli.py.py
@time: 2020/12/28 10:21 PM
"""
```

## Bash script header

Strict mode for shell scripts: exit on error, treat unset variables as errors, and fail a pipeline if any stage fails.

```bash
#!/bin/bash
set -e
set -u
set -o pipefail
```

## Command-line parsing in Rust with clap

A `clap` derive skeleton with a verbosity flag, `env_logger`, and `human_panic` wired together.

```rust
#[allow(unused)]
use clap::Parser;
use env_logger::Builder;
use human_panic::setup_panic;
use log::info;


#[derive(Parser, Debug)]
#[command(name = "sv2gf")]
#[command(version = "0.1.0")]
struct Args {
    /// The input file of svs
    #[arg(short = 's', long)]
    sv: PathBuf,

    /// The input file of gfs
    #[arg(short = 'g', long)]
    gf: PathBuf,

    /// The Distance threshold
    #[arg(short = 'd', long, default_value = "1000000")]
    dis_threshold: u32,

    #[clap(flatten)]
    verbose: clap_verbosity_flag::Verbosity,
}

fn cli() -> (PathBuf, PathBuf, u32) {
    let args = Args::parse();
    let sv = args.sv;
    let gf = args.gf;
    let dis_threshold = args.dis_threshold;
    info!("sv: {:?}, gf: {:?}", sv, gf);
    (sv, gf, dis_threshold)
}

fn main() {
    setup_panic!();
    let args = Args::parse();

    Builder::new()
        .filter_level(args.verbose.log_level_filter())
        .init();

    let (input_sv, input_gf, dis) = cli();
}
```

## Forward a port through a jump host

Chain two SSH tunnels to reach a port on a compute node that is only accessible from a login node.

```bash
ssh -L 8899:localhost:8899 quest ssh -N -L 8899:localhost:8899 qgpu0101
```

## Gradient clipping in PyTorch

Rescale all gradients so that their global L2 norm does not exceed `theta`.

```python
def grad_clipping(net, theta):
  if isinstance(net, nn.Module):
    params = [p for p in net.parameters() if p.requires_grad]
  else:
    params = net.params

  norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params )) # include all parameters

  if norm > theta:
    for param in params:
      param.grad[:] *= theta / norm
```

## reStructuredText docstring directives

The Sphinx directives I use most often inside docstrings.

```python
:Example:

>>> print("hello world!")
hello world!

.. note:: can be useful to emphasize
.. seealso:: :class:`MainClass2`
.. warning:: arg2 must be non-zero.
.. todo:: check that arg2 is non zero.
```

## Remove large files from Git history

Strip every blob over 100 MB from the repository history with `git-filter-repo`.

```bash
git filter-repo --force --strip-blobs-bigger-than 100M
```

## Keep a Colab session alive

Run this in the browser console to click the connect button every minute so the runtime does not disconnect.

```javascript
function KeepClicking() {
  console.log("Clicking");
  document.querySelector("colab-connect-button").click();
}
setInterval(KeepClicking, 60000);
```

## Add an "Open in Colab" badge

Markdown for a badge that opens a GitHub-hosted notebook in Colab.

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)
```

## Start an interactive Slurm shell on a GPU node

Request one GPU for an hour and drop into a shell on the allocated node.

```bash
srun -n 1 -t 1:00:00 -p gpu --gres=gpu:tesla:1 --pty bash
```

## Slurm batch script header

The `#SBATCH` preamble I use for GPU jobs.

```bash
#!/bin/bash -l
#SBATCH --job-name=MLHW3 # job name
#SBATCH --output=MLHW3_%j.log # log name
#SBATCH --time=8:00:00 # time
#SBATCH --ntasks=1 # tasks number
#SBATCH --cpus-per-task=8 # cpu number
#SBATCH --ntasks-per-node=1 # node number
#SBATCH --mem=30G # total memory
#SBATCH --tmp=30G #
#SBATCH --mail-type=ALL
#SBATCH --mail-user=li002252@umn.edu
#SBATCH --gres=gpu:v100:1 # gpu
#SBATCH -p v100 # partitions
cd $SLURM_SUBMIT_DIR
date;hostname;pwd
```

## Export and recreate a conda environment

Dump the environment without the machine-specific `prefix` line, then rebuild it elsewhere.

```bash
conda env export | grep -v '^prefix' > freeze.yml
conda env create -f freeze.yml
```

## Show every expression result in a Jupyter cell

By default Jupyter only displays the last expression in a cell; this shows all of them.

```python
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```

## Arrange multiple subfigures in LaTeX

A two-by-two grid of images with individual captions using the `subcaption` package.

```latex
\usepackage{subcaption}

\begin{figure}[h]
    \begin{subfigure}{0.5\textwidth}
        \includegraphics[width=0.9\linewidth, height=5cm]{rna_ttest.png}
        \caption{T-test for RNA-Seq data}
        \label{fig:subim1}
    \end{subfigure}
    \begin{subfigure}{0.5\textwidth}
        \includegraphics[width=0.9\linewidth, height=5cm]{rna_ranksum.png}
        \caption{Rank-sum for RNA-Seq data}
        \label{fig:subim2}
    \end{subfigure}

    \begin{subfigure}{0.5\textwidth}
        \includegraphics[width=0.9\linewidth, height=5cm]{micro_ttest.png}
        \caption{T-test for Microarray data}
        \label{fig:subim1}
    \end{subfigure}
    \begin{subfigure}{0.5\textwidth}
        \includegraphics[width=0.9\linewidth, height=5cm]{micro_ranksum.png}
        \caption{Rank-sum for Microarray data}
        \label{fig:subim2}
    \end{subfigure}
\caption{Histogram of the p-values of all genes}
\end{figure}
```

## List available fonts in Jupyter

Render every font Matplotlib knows about in its own face so you can pick one visually.

```python
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])

HTML("<div style='column-count: 2;'>{}</div>".format(code))
```

## Display an image file in Jupyter

Show a local image inline at a fixed size.

```python
from IPython.display import Image
from IPython.core.display import HTML
PATH = "tree_default_max_depth.png"
Image(filename = PATH , width=900, height=900)
```

{{< signoff >}}
