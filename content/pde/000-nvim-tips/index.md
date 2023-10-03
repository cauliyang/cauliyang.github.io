---
title: Collections of Amazing Vim Tips
description: Smart Tips make life better
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

This blog will evolve to including more valuable content.
Using `nvim` tag to filter more content about nvim and others.

## 001 Using command mode in visual block.

After you select a visual block in vim, you can execute operation on the block by typing `:normal ops`.
`ops` means the operations you intend to do.
For instance, let's assume that you have a text as shown below, and you have already select them in virtual mode.

After typing `:normal Atest` that mean appends "test" to every line at the end.
You will see:

## 002 Mapping `<C-d>` and `<C-u>` to `<C-d>zz` and `<C-u>zz`.

`<C-d>` is key combinations of `Control` and `d`.
In normal mode, `<C-d>` means half page down and `<C-u>` means half page up.
`zz` is key combinations of double `z`, which help center cursor to middle position of current buffer.
The new mapping is combinations of these two operations.
Even though page is moved to up or down, the focus will always be center.

## 003 Repeat and Reverse Operation [^vim]

{{< figure src= "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-21_15.18.14.png" width=600 >}}

## 004 `daw` or `daW` delete one word and `cW` or `cw` delete one word then

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2011.39.59.gif" width=600 >}}

## 005 `<C-h>` and `<C-w>` to delete words in **insert mode**.

For example, assuming current buffer contains **this is a test**.
`<C-h>` will delete one character and `<C-w>` will delete one word.

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2000.21.58.gif" width=600 >}}

## 006 `<C-o>` enter **Insert normal mode**

**Insert normal Mode** means that the buffer will leave at insert mode after using **Norm mode**.

For example, we assume current buffer is **this is a test**,

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-22%2011.42.57.gif" width=600 >}}

## 007 `gv` select recent visual block

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-30_22.33.26.png" width=500 >}}

## 008 `Vr` + character replace one line with same character

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/2022-12-30%2023.21.39.gif" width=500 >}}

## 009 use `*` to search for each occurrence

You can use `*` to search the word at which the current cursor locate.

## 010 Powerful Command Line Mode

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2023-01-06_09.55.23.png" width=500 >}}

## 011 `read !{cmd}` to load output of `cmd` to current buffer

## 012 `write !{cmd}` to send current buffer to input of `cmd`

## 013 use `<C-o>` as backward jump and `<C-i>` as forward jump

<!-- links -->

[^vim]: [Practical Vim](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
