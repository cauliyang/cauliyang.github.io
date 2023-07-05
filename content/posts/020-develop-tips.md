---
title: Development Tips
description: Fast implementation of intervel tree.
tags: ["Development"]
date: 2023-07-05
featured: false
draft: true
---

## Tip1: hidden desktop icons on macOS

```bash
defaults write com.apple.finder CreateDesktop false
killall Finder
```

Otherwise, you want to show the icons again

```bash
defaults write com.apple.finder CreateDesktop true
killall Finder
```
