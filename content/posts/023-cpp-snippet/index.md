---
title: Code Snippets
description:
tags: ["C++", "Rust", "Python"]
date: 2022-09-22
lastmod: 2023-09-02
featured: false
draft: false
---

## 1. Get Random numbers

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
