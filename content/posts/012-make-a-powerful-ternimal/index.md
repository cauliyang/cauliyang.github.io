---
title: Make A Powerful Terminal Workspace
description: Using Alacritty, Zellij, and Fish to empower the terminal
tags: ["Tool", "macOS"]
date: 2022-12-15
featured: false
draft: false
# image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-17_01.41.16.png"
---

I recently made a change to my terminal setup, switching from using iTerm2 + Zsh + Tmux to Alacritty + Fish + Zellij.
I discovered that my new combination is extremely powerful and versatile.
The flexibility to highly customize each of these tools was a significant factor in my decision to keep them.
However, configuring these tools can be a time-consuming and frustrating process.
If you're interested in trying them out for yourself, you can click on the links provided to download the relevant tools.
It's worth noting that all of these tools are open-source :rocket:

## 1. [Alacritty]

After installing Alacritty, you can create a configuration file ~/.alacritty.yml, which is used to configure the terminal emulator.
I use GitHub to host all of my configurations, including Alacritty's.
My configuration file includes detailed comments to assist others in understanding the various options available.

One important aspect to keep in mind is that you may need to change the key mapping in order to map the `alt` key to the `option` or `meta` key on macOS.
Information on how to address this issue can be found in [This issue].
Fortunately, alacrity release new version (0.12.0) now, and we do not need to remapping keys one by one to use `alt` as `option`.
We just use the following configuration simply.

```bash
window:
  option_as_alt: Both
```

Additionally, you can also change the color theme to your preference.
I enjoy using [base 16] themes.

## 2. [Zellij]

Previously, I was using Tmux, which is a widely popular tool for managing terminal windows.
Recently, I've been learning Rust and have been drawn to tools implemented using this language.
[Zellij] is one such tool that caught my attention due to its user-friendliness compared to Tmux, which offers built-in key-mapping and helpful tips directly in the terminal.
This eliminates the need to constantly reference a cheat-sheet.
The configuration file for [Zellij] can be found at `~/.config/zellij/config.kdl.`
To be honest, you may not need to add any configurations at all.
Similar to [Alacritty], you can also change the color theme of [Zellij] as per your preference.

## 3. [Fish]

I have grown to truly appreciate [Fish], it has saved me a lot of time.
In comparison to Zsh, Fish does not require the installation of numerous plugins to access powerful features.
Fish provides out-of-the-box features such as auto-suggestion, searching through command history and fancy completion making it much more user-friendly.
Of course, if desired, you can install plugins, but I find that it is not necessary.
[Fisher] is a plugins' management tool for [Fish] shell, and you can look it up to find recommended plugins.
Fish also allows for high degree of customization, such as changing the prompt and greeting message according to your preference.
I use [Tide] prompt, it is a clean and visually appealing prompt.

## 4. Summary

The provided documentation for these tools should be sufficient to get you started on using them.
In addition, you can use [my configuration] as a reference for modifying your own.
I use a lot of powerful and fancy terminal applications and I have shared my setup in my blog, specifically in my [desktop setup] post.

<!-- link -->

[zellij]: https://zellij.dev/documentation/introduction.html
[alacritty]: https://github.com/alacritty/alacritty
[fish]: https://fishshell.com/
[fisher]: https://github.com/jorgebucaran/`fisher`
[my configuration]: https://github.com/cauliyang/dot-files/blob/main/.alacritty.yml
[this issue]: https://github.com/alacritty/alacritty/issues/93
[base 16]: https://github.com/chriskempson/base16
[desktop setup]: ../../posts/002-macos-configuration
