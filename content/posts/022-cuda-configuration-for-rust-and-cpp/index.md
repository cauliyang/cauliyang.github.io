---
title: CUDA for Deep Learning Inference in Rust and C++
description:
tags: ["Rust", "C++", "CUDA"]
date: 2023-08-29
featured: false
draft: false
---

## Deep Learning Inference

Nowadays, Rust and C++ are raising in deep learning due to their efficiency
even though Python is the most popular programming language.
Python still dominates training of models but inferior in inferencing,
especially in cross-platform environment.
Large Language Model (LLM) prevulate since ChatGPT comes out.
Every company and research group are competing and mining "glod" in LLM, which
generates "lots of" so called LLMs.
However, not every LLM is useful and valuable.

In addition, Larger image generation models like stable diffusion attacts
individuals' focus as well.
Both LLMs and Big image generation models share one attributes: billions of
parameters sized with GB unit.

Privacy is another significant concerns for us who want to use LLM.
We do not want our data is "steal" by these models without pay.
Recently, llama is an open source LLM, which aim to compete with ChatGPT.
Considering privacy, the best solution is to run the model in our own device.
Nevertheless, not everyone has a powerful CPU not mentioned GPU.
Hence, the community urgent to achieve extreme speed when running the models.
[llama.cpp], which inference framework written in C/C++ and use optimized skills, including SIMD, quantization, mixed precision, GPU, and **cross-platform**, as many as
possible, handle the necessity
The open source community contributes popular models inferenced via [llama.cpp],
which allows everyone run LLM in our own devices.

[llama.cpp] and C++ are great, but Rust still has its own space.
Rust is super suitable for WebAssembly and create Web Application or GUI
application [^1].
Additionally, there are some excellent pure Rust deep learning framework including [dfdx], [burn], and [candle], and they are
envoled quickly and are able to be cross-platform with different accerlated
backend.

In summary, we can use [llama.cpp] or Rust to deploy the model when we finish training
steps.
It enables large deep learning models to be accessible for everyone and every device.

## Check your CUDA driver version

Unfortunately, I still meet some problems when I try to config CUDA environment in a high processing computer (HPC).
The blog will record how I resolve the problems without admin right.

To configure CUDA for Rust and C++, we need to ensure that the necessary CUDA libraries and headers are properly installed.
The build system is set up to link against them.
Additionally, we may need to specify the appropriate compiler flags and paths for CUDA integration.
To configure CUDA for Rust and C++, make sure to install CUDA libraries and headers properly.
Also, set up your build system to link against them and specify the necessary compiler flags and paths for CUDA integration.

```bash
nvidia-smi
```

## Use CONDA to install CUDA and gcc/g++

```bash
mamba create -n cuda python=3.10
mamba activate cuda
```

```bash
mamba install cuda -c nvidia/label/cuda-11.7.0
```

## Install compiler

```bash
mamba install gcc=11.0 gxx=11.0
```

## Test for candle

```bash
cargo new test_candle
cd test_candle
```

```bash
cargo add candle_core --features cuda
```

```rust
use candle_core::{Device, Tensor};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;

    let a = Tensor::randn(0f32, 1., (2, 3), &device)?;
    let b = Tensor::randn(0f32, 1., (3, 4), &device)?;

    let c = a.matmul(&b)?;
    println!("{c}");
    Ok(())
}
```

```rust
use candle_core::{Device, Tensor};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::new_cuda(0)?;
    let a = Tensor::randn(0f32, 1., (2, 3), &device)?;
    let b = Tensor::randn(0f32, 1., (3, 4), &device)?;

    let c = a.matmul(&b)?;
    println!("{c}");
    Ok(())
}
```

```rust
git clone https://github.com/huggingface/candle.git
cd candle
CUDA_ROOT="/home/mambaforge/env/cuda" CC="/home/mambaforge/env/cuda/bin/gcc" CXX="/home/mambaforge/env/cuda/bin/g++" RUSTFLAGS="-L/home/mambaforge/env/cuda/lib/stubs" cargo run --examples whisper --features cuda --realease
```

## add CUDA to libpath

```
= note: /usr/bin/ld: /projects/b1171/ylk4626/project/candle/target/release/deps/libring-bbeca6a1d29bfb40.rlib(aesni-x86_64-elf.o): unable to initialize decompress status for section .debug_line
          /usr/bin/ld: /projects/b1171/ylk4626/project/candle/target/release/deps/libring-bbeca6a1d29bfb40.rlib(aesni-x86_64-elf.o): unable to initialize decompress status for section .debug_line
          /projects/b1171/ylk4626/project/candle/target/release/deps/libring-bbeca6a1d29bfb40.rlib: error adding symbols: File format not recognized
          collect2: error: ld returned 1 exit status
```

```bash
export RUSTFLAGS="-L/home/mambaforge/env/cuda/lib/stubs"
```

## set CUDA_ROOT as CONDA_PREFIX

```
CUDA_ROOT="/home/mambaforge/env/cuda"
```

## Bonus

```bash
#!/bin/bash
set -e
set -u
set -o pipefail

# Set default values
use_gpu=0
gpu_number=1

# Display help message
display_help() {
        local script_name=$(basename "$0")
        echo "Usage: $script_name <time> <memory> [gpu_number]"
        echo
        echo "   time         The time parameter value in hours"
        echo "   memory       The memory parameter value in GB"
        echo "   gpu_number   The number of GPUs (default: 1)"
        exit 1
}

# Check if both parameters are provided
if [ "$#" -lt 2 ]; then
        display_help
fi

time="$1"
memory="$2"

# If third parameter exists, assign its value to gpu_number and set the use_gpu flag
if [ "$#" -ge 3 ]; then
    gpu_number="$3"
    use_gpu=1
fi

echo "Time: $time hours"
echo "Memory: $memory GB"

if [ "$use_gpu" -eq 1 ]; then
    echo "Using GPU with GPU Number: $gpu_number"
    srun -n 8 -p b1171 --account=b1171 -t ${time}:00:00 --gres=gpu:a100:$gpu_number --mem ${memory}g --pty bash
else
    echo "Using CPU only"
    srun -n 8 -p b1171 --account=b1171 -t ${time}:00:00 --mem ${memory}g --pty bash
fi

```

## Canveat

### Do not use slurm

[^1]: https://github.com/flosse/rust-web-framework-comparison

<!-- links -->

[llama.cpp]: https://github.com/ggerganov/llama.cpp
[candle]: https://github.com/huggingface/candle
[burn]: https://github.com/burn-rs/burn
[dfdx]: https://github.com/coreylowman/dfdx
