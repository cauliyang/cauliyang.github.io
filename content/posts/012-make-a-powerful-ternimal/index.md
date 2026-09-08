---
title: Make a Powerful Terminal Workspace
description: How I built a fast, keyboard-driven terminal workspace from Wezterm, Fish, and Zellij, with notes on Alacritty.
categories: ["Tools"]
tags: ["Terminal", "macOS"]
date: 2022-12-15
featured: false
draft: false
---

My terminal setup has gone through two changes.
I first moved from iTerm2 + Zsh + Tmux to Alacritty + Fish + Zellij, and later swapped Alacritty for Wezterm.
Today my stack is Wezterm + Fish + Zellij.
The combination is fast and versatile, and the ability to customize each tool in depth is the main reason I have kept it.
All of these tools are open source; the links below point to their download pages.

{{< alert icon="triangle-exclamation" >}}
Configuring these tools can be time-consuming and occasionally frustrating.
{{< /alert >}}

## Wezterm

![Wezterm running with split panes and a tab bar](https://wezterm.org/screenshots/wezterm-vday-screenshot.png "From the Wezterm website")

[Wezterm] is a fast, highly customizable, cross-platform terminal emulator.
It is written in Rust and uses OpenGL and DirectWrite for GPU-accelerated rendering.
The features that matter most to me:

1. **Cross-platform support.** Wezterm runs on Windows, macOS, Linux, and FreeBSD, so the same configuration follows me across machines.
2. **GPU-accelerated rendering.** Scrolling and typing stay smooth even under heavy output.
3. **Extensive configuration.** Colors, fonts, transparency, and key bindings are all adjustable.
4. **Built-in multiplexing.** Wezterm can run and manage multiple terminal sessions in a single window, much like tmux.
5. **Shell integration.** Features such as automatic directory tracking and local echo come with it.

On macOS, Homebrew installs it in one command:

```bash
brew install wezterm
```

For Windows, Linux, and FreeBSD, download the installer or package from the [Wezterm GitHub releases page](https://github.com/wez/wezterm/releases).
Once installed, launch it by typing `wezterm` in an existing terminal or from your application menu.

The configuration file is written in Lua and lives in your home directory.
For example, to change the default font size:

```lua
wezterm = {
  font_size = 11.0,
}
```

If you want better performance, more customization, or simply a more pleasant terminal, Wezterm is worth trying.

## Alacritty

![Alacritty terminal window](https://alacritty.org/alacritty_example.png)

After installing [Alacritty], create a configuration file at `~/.alacritty.yml`.
I keep all of my configurations, including Alacritty's, on GitHub, and the file is commented to explain the available options.

One thing to watch for on macOS: the `alt` key needs to be mapped to `option` (meta).
The background is in [this issue].
Since Alacritty 0.12.0 there is no need to remap keys one by one; a single option does it:

```yml
window:
  option_as_alt: Both
```

You can also change the color theme.
I like the [base 16] themes.

## Zellij

I used Tmux for a long time, but since learning Rust I have been drawn to tools written in it.
[Zellij] is one of them.
It is friendlier than Tmux: key bindings are built in and hints are displayed directly in the terminal, so there is no need to keep a cheat sheet open.
The configuration file lives at `~/.config/zellij/config.kdl`, and honestly you may not need to add anything to it.
As with Alacritty, the color theme is easy to change.

{{< carousel images="gallery/*" interval="2500" >}}

## Fish

[Fish] has saved me a lot of time.
Unlike Zsh, it does not need a pile of plugins to be useful: autosuggestions, history search, and rich completions work out of the box.
Plugins are available if you want them; [Fisher] is the plugin manager for Fish, and its README lists recommended plugins.
Fish is also easy to customize, from the prompt to the greeting message.
I use the Tide prompt, which is clean and visually appealing.

{{< carousel images="gallery/fish/*" interval="2500" >}}

## Summary

The official documentation for each tool is enough to get started, and you can use [my configuration] as a reference when adapting your own.

{{< github repo="cauliyang/dotfiles" >}}

I rely on many other terminal applications as well; the full setup is described in my [desktop setup] post.

{{< signoff >}}

<!-- link -->

[zellij]: https://zellij.dev/documentation/introduction.html
[alacritty]: https://github.com/alacritty/alacritty
[fish]: https://fishshell.com/
[fisher]: https://github.com/jorgebucaran/fisher
[my configuration]: https://github.com/cauliyang/dotfiles
[this issue]: https://github.com/alacritty/alacritty/issues/93
[base 16]: https://github.com/chriskempson/base16
[wezterm]: https://wezfurlong.org/wezterm

[desktop setup]: {{< ref "002-macos-configuration" >}}
