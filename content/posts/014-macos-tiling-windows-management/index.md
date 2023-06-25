---
title: Tiling Windows Management in macOS
description: yabai, skhd, stackline  and sketchybar to manage windows.
tags: ["Tool", "macOS"]
date: 2022-12-20
featured: false
draft: false
# image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/iShot_2022-12-20_20.27.10.png"
---

## 1. Aims

The philosophy of Vim's motion has had a profound influence on me, leading me to fully embrace [Neovim].
The notion of having to reposition windows using a mouse is anathema to me.
I greatly value the experience of utilizing solely the keyboard.
As such, I set out to find a tool to aid me in managing windows seamlessly.
Eventually, I discovered a quartet of exceptional tools that I highly recommend giving a try.
To this day, they continue to surpass my expectations and enhance my productivity.

**WARN!!!: Configuration is time-consuming, and you can give up if you do not like that.**
However, that means you have already missed one amazing thing.

## 2. Tools

### [yabai]

[Yabai] is tiling windows manager akin to [i3], falling under the category of BSP window managers.
Its capabilities are robust enough to provide a fluid experience.
It can be tailored to your preferences through binding any key to execute commands in [yabai].
You can view the video linked below to witness the power of [yabai].
Another notable tool, [Skhd], was developed by the same talented individual who created [yabai].

[![YTB](https://img.youtube.com/vi/AdwhjIg_Xe4/0.jpg)](https://www.youtube.com/watch?v=AdwhjIg_Xe4&ab_channel=StephenHuan)

### [Skhd]

[Skhd] is key mapping tool that can allow you bind keys to execute command line tool.
For example `ctrl + alt - left: yabai -m display --focus west || yabai -m display --focus recent`, it means that `ctrl + alt - left` will cause [ yabai ] to move focus to difference monitors.

More importantly, [skhd] allows for the creations of multiple modes, similar to Vim's modal editing.
Each mode can have its won set of motion commands, distinguished by their unique prefix.
This is an incredibly powerful feature, as it reduces the need for memorizing a plethora of complex key combination.
You need only remember the prefix of the mode you're currently in.
[Skhd] seamlessly integrates with [Yabai] and [sketchybar], resulting in an unparalleled user experience.

### [Stackline]

[Stackline] is a tool that enables the visualization of stack indicators, allowing you to easily discern which program is currently at the top of the stack and make changes accordingly.
The read arrow serves as the [stackline] indicator.

{{< figure src= "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/20221220213154.png" numbered="true" width="533" >}}

### [SketchyBar]

[SketchyBar] is menu bar tool that can be paired with [yabai] and [skhd] to display a wealth of information.
As seen in the top portion of the previous screenshot, it can be customized to include any pertinent information you desire.

## 3. Take home message

I must acknowledge that the configuration process can be both tedious and frustrating, a necessary trade-off for attaining a high degree of customization.
These tools all possess an array of fancy features, made possible through their high degrees of customization.
I will share [my personal configuration] and their documentation also provide ample information to assist in the process.
Patience is key, as the time invested in configuring these tools will ultimately pay off in terms of the enhanced functionality they provide.
If you have any other recommendations or alternatives, please do not hesitate to share them.

<!-- links -->

[yabai]: https://github.com/koekeishiya/yabai
[neovim]: https://neovim.io/
[skhd]: https://github.com/koekeishiya/skhd/
[stackline]: https://github.com/AdamWagner/stackline/
[sketchybar]: https://github.com/FelixKratz/SketchyBar/
[i3]: https://i3wm.org/
[my personal configuration]: https://github.com/cauliyang/dot-files/
