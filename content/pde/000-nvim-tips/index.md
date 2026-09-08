---
title: A Collection of Useful Vim Tips
description: A growing list of small Vim and Neovim tricks I use daily, from visual-block commands to insert-mode shortcuts and jump lists.
categories: ["Tools"]
tags: ["Neovim"]
date: 2022-12-21
lastmod: 2023-07-15
featured: false
draft: false
# image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2011.42.57.gif"
showTableOfContents: false
series: ["Personal Development Environment"]
series_order: 1
---

## Why

This post is a running list of Vim and Neovim tricks that I find myself using every day.
It grows over time; the `Neovim` tag collects related posts.

## 001: Run a command on a visual block

After selecting a visual block, you can run a normal-mode operation on every line of it with `:normal <ops>`, where `<ops>` is the key sequence you would type by hand.
For example, with a block selected, `:normal Atest` appends `test` to the end of every selected line.

## 002: Map `<C-d>` and `<C-u>` to `<C-d>zz` and `<C-u>zz`

`<C-d>` is `Control` + `d`.
In normal mode, `<C-d>` scrolls half a page down and `<C-u>` scrolls half a page up.
`zz` recenters the current line in the window.
Combining them means the cursor line stays centered no matter how far you scroll.

## 003: Repeat and reverse operations [^vim]

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-21_15.18.14.png" width=600 alt="Table of Vim repeatable actions and how to reverse them, from Practical Vim" >}}

## 004: `daw`/`daW` delete a word, `cw`/`cW` change it

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2011.39.59.gif" width=600 alt="Animation of daw, daW, cw, and cW acting on words" >}}

## 005: `<C-h>` and `<C-w>` delete backwards in insert mode

Suppose the buffer contains **this is a test** and the cursor is at the end.
In insert mode, `<C-h>` deletes one character and `<C-w>` deletes one word.

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2000.21.58.gif" width=600 alt="Animation of Ctrl-h and Ctrl-w deleting text in insert mode" >}}

## 006: `<C-o>` enters insert-normal mode

Insert-normal mode runs a single normal-mode command and then returns to insert mode.
Starting again from **this is a test**:

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2011.42.57.gif" width=600 alt="Animation of Ctrl-o running one normal-mode command from insert mode" >}}

## 007: `gv` reselects the last visual selection

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-30_22.33.26.png" width=500 alt="Screenshot of gv restoring the previous visual selection" >}}

## 008: `Vr` + a character fills the line with that character

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-30%2023.21.39.gif" width=500 alt="Animation of Vr replacing every character on a line" >}}

## 009: `*` searches for the word under the cursor

Press `*` to jump to the next occurrence of the word under the cursor; `n` and `N` continue the search.

## 010: Command-line mode is powerful

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2023-01-06_09.55.23.png" width=500 alt="Cheat sheet of Ex commands available in command-line mode" >}}

## 011: `:read !{cmd}` inserts the output of `cmd`

The output of the shell command is inserted below the cursor in the current buffer.

## 012: `:write !{cmd}` pipes the buffer into `cmd`

The current buffer (or a range) is sent to the standard input of the shell command.

## 013: `<C-o>` jumps back and `<C-i>` jumps forward

These move through the jump list, so you can retrace your steps after a search, a tag jump, or a `G`.

{{< signoff >}}

<!-- links -->

[^vim]: [Practical Vim](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
