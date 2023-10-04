---
title: Code Snippets
description:
tags: ["C++", "Rust", "Develop"]
date: 2022-09-22
lastmod: 2023-10-04
featured: false
draft: false
---

## Get Random numbers

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

## Get random numbers between min and max

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

## Clear Input Stream

```cpp
if (std::cin.fail()) // has a previous extraction failed or overflowed?
{
    // yep, so let's handle the failure
    std::cin.clear(); // put us back in 'normal' operation mode
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // and remove the bad input
}
```

## Compare Float Number

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

## Shelang for Python

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

## Shelang for Bash

```bash
#!/bin/bash
set -e
set -u
set -o pipefail
```

## CLI for Rust

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

## Export port from two layers nodes

```bash
ssh -L 8899:localhost:8899 quest ssh -N -L 8899:localhost:8899 qgpu0101
```

## Timer for C++

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

## Gradient Clipping

```python
def grad_clipping(net, theta):
  if isinstance(net, nn.Module):
    params = [p for p in net.parameters() if p.requires_grad]
  else:
    params = net.params

  norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params )) # include all parameters

  if norm > theta:
    for param in params:
      param.grad[:] *= theta/nor
```

## RST Docstring directive

```python
:Example:

>>> print("hello world!")
hello world!

.. note:: can be useful to emphasize
.. seealso:: :class:`MainClass2`
.. warning:: arg2 must be non-zero.
.. todo:: check that arg2 is non zero.
```

## Git remove large files

```bash
git filter-repo --force --strip-blobs-bigger-than 100M
```

## Stop Colab Disconnect

```javascript
function KeepClicking() {
  console.log("Clicking");
  document.querySelector("colab-connect-button").click();
}
setInterval(KeepClicking, 60000);
```

## Open Colab

```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)
```

## Srun for interactive shell

```bash
srun -n 1 -t 1:00:00 -p gpu --gres=gpu:tesla:1 --pty bash
```

## Bash info for Slurm

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

## Conda export env

```bash
conda env export | grep -v '^prefix' > freeze.yml
conda env create -f freeze.yml
```

## Multiple output in Jupyter

```python
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```

## Multiple Images in Latex

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

## Show fonts in Jupyter

```python
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])

HTML("<div style='column-count: 2;'>{}</div>".format(code))
```

## Display image in Jupyter

```python
from IPython.display import Image
from IPython.core.display import HTML
PATH = "tree_default_max_depth.png"
Image(filename = PATH , width=900, height=900)
```
