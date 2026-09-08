---
title: Development Tips
description: Short, copy-and-paste development tricks I keep reaching for, starting with hiding the macOS desktop icons.
categories: ["Tools"]
tags: ["macOS", "Development"]
date: 2023-07-05
featured: false
draft: false
---

A running list of small tricks that are too short for their own post.

## Hide desktop icons on macOS

A clean desktop is one less distraction during screen sharing and recording. Finder can stop drawing the icons entirely:

```bash
defaults write com.apple.finder CreateDesktop false
killall Finder
```

To show them again:

```bash
defaults write com.apple.finder CreateDesktop true
killall Finder
```
