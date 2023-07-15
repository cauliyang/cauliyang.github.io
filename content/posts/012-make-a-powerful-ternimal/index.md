---
title: Make A Powerful Terminal Workspace
description: Using Alacritty, Zellij, and Fish to empower the terminal
tags: ["Terminal"]
categories: ["macOS"]
date: 2022-12-15
featured: false
draft: false
# image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-17_01.41.16.png"
---

I recently made a change to my terminal setup, switching from using iTerm2 + Zsh + Tmux to Alacritty + Fish + Zellij.
Now I use Wezterm + Fish + Zellij.
I discovered that my new combination is extremely powerful and versatile.
The flexibility to highly customize each of these tools was a significant factor in my decision to keep them.

{{< alert  icon="fire" cardColor="#e63946" iconColor="#1d3557" textColor="#f1faee"  >}}
configuring these tools can be a time-consuming and frustrating process.
{{< /alert >}}

If you're interested in trying them out for yourself, you can click on the links provided to download the relevant tools.
It's worth noting that these tools are open-source :rocket:

## 0. Wezterm

Welcome to the world of command-line interfaces and terminal emulators.
If you're a developer, system administrator, or a tech enthusiast, you're likely no stranger to the terminal.
But did you know that not all terminals are created equal? In this article, we'll introduce Wezterm,
a modern, GPU-accelerated terminal emulator that takes your command-line work to the next level.

![wezterm](https://wezfurlong.org/wezterm/screenshots/wezterm-vday-screenshot.png "from wezerm website")

Wezterm is a fast, highly customizable, and cross-platform terminal emulator that focuses on delivering a seamless user experience.
It's built with a slew of features that make it a standout choice for those seeking a high-performance terminal emulator.
Wezterm is developed in Rust and uses both OpenGL and DirectWrite for GPU acceleration to achieve its impressive performance.

Here are some of the most compelling features of Wezterm:

1. **Cross-Platform Support:** Wezterm works on various platforms, including Windows, macOS, Linux, and FreeBSD. This versatility makes it an excellent choice for those who work across different operating systems.
2. **GPU-Accelerated Rendering:** Leveraging the power of your GPU, Wezterm ensures smooth scrolling and typing, even under heavy loads.
3. **Highly Configurable:** Wezterm allows you to tailor your terminal environment to your liking, offering various customization options, including colors, fonts, transparency, and key bindings.
4. **Multiplexer Support:** Wezterm includes built-in support for terminal multiplexing, similar to popular tools like tmux, allowing you to run and manage multiple terminal sessions within a single window.
5. **Shell Integration:** With Wezterm's shell integration, you can enjoy features like automatic directory changing and local echo.

Installing Wezterm is straightforward.
For example, on macOS, you can use Homebrew to install Wezterm by running the following command in your terminal:

```bash
brew install wezterm
```

For other platforms like Windows, Linux, and FreeBSD, you can download the appropriate installer or package from the [Wezterm GitHub releases page](https://github.com/wez/wezterm/releases).
Once installed, you can launch Wezterm just like any other terminal emulator.
Simply type `wezterm` in your existing terminal, or find it in your system's application menu.
Wezterm's configuration file is written in Lua and typically resides in your home directory.
You can customize various aspects of Wezterm by editing this configuration file.
For example, to change the default font size, you can add the following to your configuration file:

```lua
wezterm = {
  font_size = 11.0,
}
```

Wezterm represents the next generation of terminal emulators, offering a slew of features that go above and beyond the capabilities of traditional terminals.
Whether you're seeking better performance, more customization, or just a more pleasant terminal experience, Wezterm is worth checking out.
Get ready to explore the world of command-line interfaces like never before with Wezterm!

## 1. Alacritty

![alacritty](https://alacritty.org/alacritty_example.png)

After installing Alacritty, you can create a configuration file ~/.alacritty.yml, which is used to configure the terminal emulator.
I use GitHub to host all of my configurations, including Alacritty's.
My configuration file includes detailed comments to assist others in understanding the various options available.

One important aspect to keep in mind is that you may need to change the key mapping in order to map the `alt` key to the `option` or `meta` key on macOS.
Information on how to address this issue can be found in [This issue].
Fortunately, alacrity release new version (0.12.0) now, and we do not need to remapping keys one by one to use `alt` as `option`.
We just use the following configuration simply.

```yml
window:
  option_as_alt: Both
```

Additionally, you can also change the color theme to your preference.
I enjoy using [base 16] themes.

## 2. Zellij

Previously, I was using Tmux, which is a widely popular tool for managing terminal windows.
Recently, I've been learning Rust and have been drawn to tools implemented using this language.
[Zellij] is one such tool that caught my attention due to its user-friendliness compared to Tmux, which offers built-in key-mapping and helpful tips directly in the terminal.
This eliminates the need to constantly reference a cheat-sheet.
The configuration file for [Zellij] can be found at `~/.config/zellij/config.kdl.`
To be honest, you may not need to add any configurations at all.
Similar to [Alacritty], you can also change the color theme of [Zellij] as per your preference.

{{< carousel images="gallery/*" interval="2500" >}}

## 3. Fish

I have grown to truly appreciate [Fish], it has saved me a lot of time.
In comparison to Zsh, Fish does not require the installation of numerous plugins to access powerful features.
Fish provides out-of-the-box features such as auto-suggestion, searching through command history and fancy completion making it much more user-friendly.
Of course, if desired, you can install plugins, but I find that it is not necessary.
[Fisher] is a plugins' management tool for [Fish] shell, and you can look it up to find recommended plugins.
Fish also allows for high degree of customization, such as changing the prompt and greeting message according to your preference.
I use [Tide] prompt, it is a clean and visually appealing prompt.

{{< carousel images="gallery/fish/*" interval="2500" >}}

## 4. Summary

The provided documentation for these tools should be sufficient to get you started on using them.
You can use [my configuration] as a reference for modifying your own.

{{< github repo="cauliyang/dotfiles" >}}

I use a lot of powerful and fancy terminal applications and I have shared my setup in my blog, specifically in my [desktop setup] post.

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
