---
title: macOS Setup for Development and Research
description: The tools I install on a fresh Mac for bioinformatics and software work, from Homebrew and the terminal to editors and everyday apps.
date: 2022-11-26
lastmod: 2023-09-02
featured: false
draft: false
categories: ["Tools"]
tags: ["macOS", "Development"]
---

## Gallery

{{< carousel images="gallery/*" interval="2500" >}}

## TLDR

|                  |                          |                    |               |
| ---------------- | ------------------------ | ------------------ | ------------- |
| [Alacritty]      | [Office]                 | [AlDente]          | [One Switch]  |
| [Alfred]         | [PDF Expert]             | [AltTab]           | [PicGo]       |
| [Bartender]      | [PyCharm]                | [cheat.sh]         | [Rectangle]   |
| [Chrome]         | [Reeder 5]               | [CLion]            | [Rust]        |
| [Conda]          | [SnippetsLab]            | [Default Folder X] | [SoundSource] |
| [Docker]         | [SpaceVim]               | [dust]             | [Time Sink]   |
| [Ferdi]          | [tldr]                   | [fish]             | [tmux]        |
| [Git]            | [tmuxinator]             | [hyperfine]        | [Vim]         |
| [Imagine]        | [Xcode]                  | [iShot]            | [Xmind]       |
| [iTerm2]         | [Zellij]                 | [LunarVim]         | [Zoom]        |
| [Magnet]         | [Zotero]                 | [Mamba]            | [zsh]         |
| [Micromamba]     | [fisher]                 | [Miniforge]        | [ouch]        |
| [MonitorControl] | [topgrade]               | [Monodraw]         | [ImageMagick] |
| [Neovim]         | [youtube-dl][youtobe-dl] | [Notion]           | [JetBrains]   |
| [Google Drive]   | [Transmit]               | [Homebrew]         | [tree]        |
| [Fluent Reader]  | [WezTerm]                | [IINA]             | [VS Code]     |

## Why I keep this list

Migrating a development setup to a new machine takes a surprising amount of time, so I started documenting the whole process when I moved to a MacBook Pro with the M1 chip.
This post covers the software I use every day; the configuration files themselves live in my dotfiles.
It is a living document: tools I have retired stay in the list, struck through or marked as replaced, so the history of the setup is still visible.

## Package manager

### Homebrew

[Homebrew] is the package manager for macOS. Almost everything else in this post is installed through it, so it goes first.

{{< steps >}}
{{< step number="1" title="Install Homebrew" >}}
Open Terminal (Applications → Utilities) and run the installer. It will ask for your password once to set up the required directories.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

{{< /step >}}
{{< step number="2" title="Install a package" >}}
Homebrew resolves and installs dependencies for you.

```bash
brew install vim
```

{{< /step >}}
{{< step number="3" title="Keep everything current" >}}

```bash
brew update && brew upgrade
```

{{< /step >}}
{{< /steps >}}

## Terminal workspace

My terminal stack has changed over time:

- [iTerm2] → [Alacritty] → [WezTerm]
- [zsh] → [fish]
- [tmux] → [Zellij]

I keep the notes on the earlier tools below for reference. The move to the current setup has its own post:

{{< article link="/posts/012-make-a-powerful-ternimal/">}}

### Alacritty

[Alacritty] is a fast, GPU-accelerated terminal emulator written in Rust. It runs on macOS, Linux, and Windows and deliberately does very little beyond rendering text quickly, which is exactly what I want when a multiplexer handles the rest.

```bash
brew install --cask alacritty
```

Configuration lives in `~/.config/alacritty/alacritty.yml`, where you set the font, color scheme, and key bindings. The [official documentation][alacritty] covers every option.

### Zellij

[Zellij] is a terminal workspace: it manages panes, tabs, and sessions inside one window. It fills the same role as [tmux], but its default key bindings and on-screen hints make it much friendlier to start with.

```bash
brew install zellij
```

Key bindings, themes, and layouts are configured in `~/.config/zellij/config.kdl`.

### Fish

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2023-02-18_22.55.20.png" alt="Fish shell showing inline autosuggestions in Alacritty" width=900 >}}

[fish], the Friendly Interactive Shell, ships with autosuggestions from your history, syntax highlighting, and sensible completions out of the box. Getting the same experience in [zsh] takes a stack of plugins; with fish I need almost no configuration.

```bash
brew install fish
```

Run `fish` to start a session. Configuration goes in `~/.config/fish/config.fish`, and I manage plugins with [fisher].

## Command-line tools

### Git

[Git] is the distributed version control system behind nearly every project I touch and the way I move code to and from GitHub. macOS ships an older Git, so I install a current one with Homebrew:

```bash
brew install git
```

### Conda

[Conda] manages packages, dependencies, and isolated environments for any language: Python, R, C/C++, and more. It started as a Python tool, but I use it to install compiled bioinformatics software just as often.

On Apple Silicon I install [Miniforge], a minimal Conda installer that defaults to the conda-forge channel and supports the arm64 architecture. For speed, I use [Mamba] or [Micromamba] as a drop-in replacement for the `conda` command when installing packages.

### tree

[tree] prints a directory as an indented listing of files. With no arguments it lists the current directory; given paths, it lists each in turn and reports the total number of files and directories.

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/20210610190826.png" alt="Output of the tree command showing a nested directory listing" caption="tree" numbered="true" width="500" >}}

```bash
brew install tree
```

### cheat.sh

[cheat.sh] is a community-maintained cheat sheet service for programming languages and command-line tools, reachable from any terminal with `curl cheat.sh/<command>`. It is the fastest way I know to look up a forgotten flag.

{{< figure src="http://cheat.sh/files/big-logo-v2-fixed.png" alt="cheat.sh logo" numbered="true" width="500" >}}

### dust

[dust] is `du` written in Rust. Instead of a flat list of numbers it prints a tree sorted by size, so the directories eating your disk are obvious at a glance.

```bash
brew install dust
```

{{< figure src="https://raw.githubusercontent.com/bootandy/dust/master/media/snap.png" alt="dust output showing disk usage as a size-sorted tree" numbered="true" width="500" >}}

### hyperfine

[hyperfine] is a command-line benchmarking tool. It runs a command repeatedly, handles warmup, and reports the mean with a confidence interval, which is far more trustworthy than a single `time` run.

```bash
brew install hyperfine
```

{{< figure src="https://i.imgur.com/z19OYxE.gif" alt="hyperfine comparing the run time of two commands" numbered="true" width="500" >}}

Run `hyperfine --help` for the options on run count, warmup iterations, and exporting results.

### ouch

[ouch] (Obvious Unified Compression Helper) gives one interface to tar, zip, gz, xz, lzma, bz2, lz4, sz, and zst, and picks the format from the file extension. `ouch decompress a.zip` extracts an archive; `ouch compress one.txt two.txt archive.zip` creates one.

```bash
cargo install ouch
```

### topgrade

[topgrade] upgrades everything on the machine in one command: Homebrew, Cargo, Conda, plugin managers, and more. It replaces the handful of update commands I used to run by hand.

{{< figure src="https://raw.githubusercontent.com/topgrade-rs/topgrade/main/doc/topgrade_demo.gif" alt="topgrade upgrading several package managers in sequence" width=500 >}}

```bash
brew install topgrade
```

### ImageMagick

{{< figure src="https://imagemagick.org/image/wizard.png" alt="ImageMagick wizard logo" width=250 >}}

[ImageMagick] is the command-line toolkit for converting and editing images. I use it mostly to resize and convert figures for slides and blog posts.

```bash
brew install imagemagick
```

The `convert` command takes an input file, optional operations, and an output file:

```bash
convert input.jpg -resize 800x600 output.jpg
```

Other useful commands are `identify` for image metadata, `composite` for layering images, and `montage` for contact sheets. `man convert` and the official documentation cover the rest, and the same functionality is exposed as a library for C, Perl, Python, and Ruby.

### youtube-dl

[youtube-dl][youtobe-dl] downloads videos from YouTube and many other sites.

```bash
brew install youtube-dl
```

Pass it a URL and it picks the best available format and saves the file to the current directory:

```bash
youtube-dl https://www.youtube.com/watch?v=VIDEO_ID
```

Options cover format selection, audio-only downloads, subtitles, and whole playlists or channels; see `youtube-dl --help`.

## Window management

For keyboard-driven window management I use [yabai], [skhd], and [SketchyBar]: a tiling window manager, a hotkey daemon, and a status bar that work together.

{{< figure src="https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-20_20.27.10.png" alt="macOS desktop with tiled windows managed by yabai and a SketchyBar status bar" width=600 >}}

I describe the setup in detail in a separate post:

{{< article link="/posts/014-macos-tiling-windows-management/" >}}

Install all three with Homebrew:

```bash
brew install koekeishiya/formulae/yabai
brew install koekeishiya/formulae/skhd

brew tap FelixKratz/formulae
brew install sketchybar
```

After installation, yabai and skhd each need a configuration file that defines the layout rules and the keyboard shortcuts. Both tools are flexible, so expect to iterate on the configuration for a while.

Tools I used before switching to yabai:

- ~~[Magnet]~~ snaps windows to screen regions with shortcuts
- ~~[Rectangle]~~ moves and resizes windows with keyboard shortcuts
- ~~[AltTab]~~ brings a Windows-style window switcher to macOS

## Editors

Each of the three editors I use has a clear strength, and the choice comes down to the task and personal preference.

### Neovim

[Neovim] is a fork of Vim that modernizes the codebase, adds Lua configuration, and exposes a plugin API that has produced a huge ecosystem. It is fast, runs anywhere a terminal does, and rewards the steep learning curve with a keyboard-driven workflow. Neovim is my primary editor, and I have written a [series]({{< ref "/pde" >}}) about my personal development environment.

### VS Code

[VS Code] is Microsoft's open-source editor built on Electron. It supports nearly every language through extensions, has strong debugging features, and needs little configuration to be productive. Its main cost is resources: it is noticeably heavier than a terminal editor.

### JetBrains

[JetBrains] builds full IDEs such as IntelliJ IDEA, [PyCharm], and [CLion]. They ship with a refactoring engine, a debugger, and deep language understanding that no plugin stack quite matches, which makes them my choice for large codebases. The trade-offs are licence cost and resource usage.

In short: Neovim for speed and customization, VS Code for ease of use and breadth, JetBrains for heavyweight refactoring and debugging.

## Applications

Everything else I install on a new Mac, with a one-line note on why. Many of these are available as Homebrew casks; my install scripts and config files are in my dotfiles on GitHub.

- [Alfred] launcher, clipboard history, and workflows that replace Spotlight
- [Default Folder X] adds recent and favorite folders to every open and save dialog
- [Docker] isolated environments for development and deployment
- [Chrome] my browser
- [IINA] a modern video player for macOS
- [Imagine] compresses images before I upload them anywhere; small and effective
- [Office] for documents that have to be Word or PowerPoint
- [MonitorControl] controls brightness and volume of external monitors from the keyboard
- [Monodraw] draws ASCII diagrams
- [PDF Expert] the best PDF reader I have used on a Mac
- [PicGo] uploads images to hosts such as GitHub; essential for writing this blog
- [SnippetsLab] my code snippet manager; integrates with Alfred
- [Xcode] Apple's IDE and developer toolchain
- [Zoom] meetings
- [Xmind] mind maps for organizing ideas
- [Transmit] file transfer client for servers and cloud storage
- [Time Sink] records how long each app is in use
- [SoundSource] per-application audio control
- [Reeder 5] RSS reader
- [Notion] notes and project planning
- ~~[One Switch]~~ one-click toggles for keep awake, hide desktop icons, and similar
- [iShot] screenshot and screen recording tool
- [Google Drive] cloud storage and file sharing
- [Ferdi] collects Gmail, Slack, and other messaging services in one window
- [Bartender] hides and organizes menu bar icons
- [AlDente] limits charging to keep the battery healthy
- [Zotero] my reference manager for research papers
- [Fluent Reader] a modern desktop RSS reader

{{< signoff >}}

<!-- link -->

[alacritty]: https://github.com/alacritty/alacritty
[aldente]: https://github.com/davidwernhart/AlDente
[alfred]: https://www.alfredapp.com/
[alttab]: https://alt-tab-macos.netlify.app/
[bartender]: https://www.macbartender.com/
[cheat.sh]: https://github.com/chubin/cheat.sh
[chrome]: https://www.google.com/chrome/?brand=FKPE&geo=US&gclid=Cj0KCQiAy4eNBhCaARIsAFDVtI0QHFokL1RZC_foWkHv92lRIhon6vMSWCm_2Zfe6g5vrkRO-JxOwJcaAsToEALw_wcB&gclsrc=aw.ds
[clion]: https://www.jetbrains.com/clion/
[conda]: https://docs.conda.io/en/latest/
[default folder x]: https://www.stclairsoft.com/DefaultFolderX/
[docker]: https://www.docker.com/?utm_source=google&utm_medium=cpc&utm_campaign=dockerhomepage&utm_content=namer&utm_term=dockerhomepage&utm_budget=growth&gclid=Cj0KCQiAy4eNBhCaARIsAFDVtI1yYmAI5cysoIDN2Vbhs5tplap41qP5MKKybSNbg9nTCA8oPe2yeXAaAofgEALw_wcB
[dust]: https://github.com/bootandy/dust
[ferdi]: https://getferdi.com/
[fish]: https://fishshell.com/
[git]: https://git-scm.com/
[google drive]: https://www.google.com/drive/
[homebrew]: https://brew.sh/
[hyperfine]: https://github.com/sharkdp/hyperfine/
[iina]: https://iina.io/
[imagine]: https://github.com/meowtec/Imagine
[ishot]: https://apps.apple.com/cn/app/ishot-%E4%BC%98%E7%A7%80%E7%9A%84%E6%88%AA%E5%9B%BE%E5%BD%95%E5%B1%8F%E5%B7%A5%E5%85%B7/id1485844094?mt=12
[iterm2]: https://iterm2.com
[lunarvim]: https://github.com/LunarVim/LunarVim
[magnet]: https://apps.apple.com/us/app/magnet/id441258766?mt=12
[mamba]: https://mamba.readthedocs.io/en/latest/
[micromamba]: https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html
[miniforge]: https://github.com/conda-forge/miniforge/
[monitorcontrol]: https://github.com/MonitorControl/MonitorControl
[monodraw]: https://monodraw.helftone.com/
[neovim]: https://neovim.io/
[notion]: https://www.notion.so/product
[office]: https://www.office.com/
[one switch]: https://fireball.studio/oneswitch
[pdf expert]: https://pdfexpert.com/?utm_source=google&utm_medium=cpc&utm_campaign=brand-hp&utm_google-campaign=brand-hp&utm_content=264692671625&utm_term=pdf%20expert&gclid=Cj0KCQiAy4eNBhCaARIsAFDVtI2Mb-84Xo5XJBQWkPHxGL-G11BnR8iF65B4kGDm2huhRRUa0wJy5VMaAjoREALw_wcB
[picgo]: https://picgo.github.io/PicGo-Doc/en/guide/
[pycharm]: https://www.jetbrains.com/pycharm/
[rectangle]: https://rectangleapp.com/
[reeder 5]: https://reederapp.com/
[rust]: https://www.rust-lang.org/
[snippetslab]: https://www.renfei.org/snippets-lab/
[soundsource]: https://rogueamoeba.com/soundsource/
[spacevim]: https://www.google.com/search?q=spacevim
[time sink]: https://manytricks.com/timesink/
[tldr]: https://tldr.sh/
[tmux]: https://github.com/tmux/tmux/wiki
[tmuxinator]: https://github.com/tmuxinator/tmuxinator
[transmit]: https://panic.com/transmit/
[tree]: https://www.geeksforgeeks.org/tree-command-unixlinux/
[vim]: https://vimawesome.com/
[vs code]: https://code.visualstudio.com/
[xcode]: https://developer.apple.com/xcode/
[xmind]: https://www.xmind.net/download/
[zellij]: https://zellij.dev/documentation/introduction.html
[zoom]: https://zoom.us/download
[zotero]: https://www.zotero.org/
[zsh]: https://ohmyz.sh/
[fisher]: https://github.com/jorgebucaran/fisher
[ouch]: https://github.com/ouch-org/ouch
[topgrade]: https://github.com/topgrade-rs/topgrade
[imagemagick]: https://github.com/imagemagick/imagemagick
[youtobe-dl]: https://github.com/ytdl-org/youtube-dl
[jetbrains]: https://www.jetbrains.com
[fluent reader]: https://github.com/yang991178/fluent-reader
[wezterm]: https://wezfurlong.org/wezterm
[yabai]: https://github.com/koekeishiya/yabai
[skhd]: https://github.com/koekeishiya/skhd/
[sketchybar]: https://github.com/FelixKratz/SketchyBar/
