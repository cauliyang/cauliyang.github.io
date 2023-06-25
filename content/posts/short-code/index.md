---
title: Short Code Example
description: showing all available short codes
date: 2023-06-24
featured: false
draft: false
tags: ["macOS", "Development"]
showAuthor: true
showAuthorsBadges: false
showComments: true
---

## Alert

```md
{{</* alert */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}
```

{{< alert >}}
**Warning!** This action is destructive!
{{< /alert >}}

---

```md
{{</* alert cardColor="red" */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}
```

{{< alert cardColor="red" >}}
**Warning!** This action is destructive!
{{< /alert >}}

---

```md
{{</* alert textColor="red" */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}
```

{{< alert textColor="red" >}}
**Warning!** This action is destructive!
{{< /alert >}}

---

```md
{{</* alert  "twitter" */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}
```

{{< alert "twitter" >}}
Do not forget to follow me
{{< /alert >}}

---

```md
{{</* alert  icon="fire" cardColor="#e63946" iconColor="#1d3557" textColor="#f1faee"  */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}
```

{{< alert icon="fire" cardColor="#e63946" iconColor="#1d3557" textColor="#f1faee" >}}
Do not forget to follow me
{{< /alert >}}

## Article

```md
{{</* article link="/posts/002-macos-configuration/" */>}}
```

{{< article link="/posts/002-macos-configuration/" >}}

## Badge

```md
{{</* badge */>}}
New article!
{{</* /badge */>}}
```

{{< badge >}}
New article!
{{< /badge >}}

## Button

```md
{{</* button href="#button" target="_self" */>}}
Call to action
{{</* /button */>}}
```

{{< button href="#button" target="_self" >}}
Call to action
{{< /button >}}

---

```md
{{</* button href="https://blowfish.page/docs/shortcodes/#icon" target="_self" */>}}
Call to action
{{</* /button */>}}
```

{{< button href="https://blowfish.page/docs/shortcodes/#icon" target="_self" >}}
Open external links
{{< /button >}}

## Carousel

`carousel` is used to showcase multiple images in an interactive and visually appealing way. This allows a user to slide through multiple images while only taking up the vertical space of a single one. All images are displayed using the full width of the parent component and using one of the predefined aspect ratios of `16:9`, `21:9` or `32:9`.

<!-- prettier-ignore-start -->
| Parameter     | Description                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| `images`      | **Required.** A regex string to match image names.                                                                |
| `aspectRatio` | **Optional.** The aspect ratio for the carousel. Either `16-9`, `21-9` or `32-9`. It is set to `16-9` by default. |
| `interval`    | **Optional.** The interval for the auto-scrooling, specified in milliseconds. Defaults to `2000` (2s)             |
<!-- prettier-ignore-end -->

```md
{{</* carousel images="{gallery/03.jpg, gallery/01.jpg, gallery/02.jpg, gallery/04.jpg}" */>}}
```

{{< carousel images="{gallery/03.jpg,gallery/01.jpg,gallery/02.jpg,gallery/04.jpg}" >}}

**Example 2:** 21:9 aspect ratio and regex-ed list of images

```md
{{</* carousel images="gallery/*" aspectRatio="21-9" interval="2500" */>}}
```

{{< carousel images="gallery/*" aspectRatio="21-9" interval="2500" >}}

## Chart

`chart` uses the Chart.js library to embed charts into articles using simple structured data. It supports a number of [different chart styles](https://www.chartjs.org/docs/latest/samples/) and everything can be configured from within the shortcode. Simply provide the chart parameters between the shortcode tags and Chart.js will do the rest.

Refer to the [official Chart.js docs](https://www.chartjs.org/docs/latest/general/) for details on syntax and supported chart types.

```js
{{</* chart */>}}
type: 'bar',
data: {
  labels: ['Tomato', 'Blueberry', 'Banana', 'Lime', 'Orange'],
  datasets: [{
    label: '# of votes',
    data: [12, 19, 3, 5, 3],
  }]
}
{{</* /chart */>}}
```

<!-- prettier-ignore-start -->
{{< chart >}}
type: 'bar',
data: {
  labels: ['Tomato', 'Blueberry', 'Banana', 'Lime', 'Orange'],
  datasets: [{
    label: '# of votes',
    data: [12, 19, 3, 5, 3],
  }]
}
{{< /chart >}}
<!-- prettier-ignore-end -->

## Figure

Blowfish includes a `figure` shortcode for adding images to content. The shortcode replaces the base Hugo functionality in order to provide additional performance benefits.

When a provided image is a page resource, it will be optimised using Hugo Pipes and scaled in order to provide images appropriate to different device resolutions. If a static asset or URL to an external image is provided, it will be included as-is without any image processing by Hugo.

The `figure` shortcode accepts six parameters:

<!-- prettier-ignore-start -->
| Parameter | Description                                                                                                                                                                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src`     | **Required.** The local path/filename or URL of the image. When providing a path and filename, the theme will attempt to locate the image using the following lookup order: Firstly, as a [page resource](https://gohugo.io/content-management/page-resources/) bundled with the page; then an asset in the `assets/` directory; then finally, a static image in the `static/` directory. |
| `alt`     | [Alternative text description](https://moz.com/learn/seo/alt-text) for the image.                                                                                                                                                                                                                                                                                                         |
| `caption` | Markdown for the image caption, which will be displayed below the image.                                                                                                                                                                                                                                                                                                                  |
| `class`   | Additional CSS classes to apply to the image.                                                                                                                                                                                                                                                                                                                                             |
| `href`    | URL that the image should be linked to.                                                                                                                                                                                                                                                                                                                                                   |
| `default` | Special parameter to revert to default Hugo `figure` behaviour. Simply provide `default=true` and then use normal [Hugo shortcode syntax](https://gohugo.io/content-management/shortcodes/#figure).                                                                                                                                                                                       |
<!-- prettier-ignore-end -->

Blowfish also supports automatic conversion of images included using standard Markdown syntax. Simply use the following format and the theme will handle the rest:

```md
![Alt text](image.jpg "Image caption")
```

**Example:**

```md
{{</* figure
    src="abstract.jpg"
    alt="Abstract purple artwork"
    caption="Photo by [Jr Korpa](https://unsplash.com/@jrkorpa) on [Unsplash](https://unsplash.com/)"
    */>}}
```

{{< figure src="abstract.jpg" alt="Abstract purple artwork" caption="Photo by [Jr Korpa](https://unsplash.com/@jrkorpa) on [Unsplash](https://unsplash.com/)" >}}

---

```md
![Abstract purple artwork](abstract.jpg "Photo by [Jr Korpa](https://unsplash.com/@jrkorpa) on [Unsplash](https://unsplash.com/)")
```

![Abstract purple artwork](abstract.jpg "Photo by [Jr Korpa](https://unsplash.com/@jrkorpa) on [Unsplash](https://unsplash.com/)")

## Gallery

`gallery` allows you to showcase multiple images at once, in a responsive manner with more varied and interesting layouts.

In order to add images to the gallery, use `img` tags for each image and add `class="grid-wXX"` in order for the gallery to be able to identify the column width for each image. The widths available by default start at 10% and go all the way to 100% in 5% increments. For example, to set the width to 65%, set the class to `grid-w65`. Additionally, widths for 33% and 66% are also available in order to build galleries with 3 cols. You can also leverage tailwind's responsive indicators to have a reponsive grid.

```md
{{</* gallery */>}}
<img src="gallery/01.jpg" class="grid-w33" />
<img src="gallery/02.jpg" class="grid-w33" />
<img src="gallery/03.jpg" class="grid-w33" />
<img src="gallery/04.jpg" class="grid-w33" />
<img src="gallery/05.jpg" class="grid-w33" />
<img src="gallery/06.jpg" class="grid-w33" />
<img src="gallery/07.jpg" class="grid-w33" />
{{</* /gallery */>}}
```

{{< gallery >}}
<img src="gallery/01.jpg" class="grid-w33" />
<img src="gallery/02.jpg" class="grid-w33" />
<img src="gallery/03.jpg" class="grid-w33" />
<img src="gallery/04.jpg" class="grid-w33" />
<img src="gallery/05.jpg" class="grid-w33" />
<img src="gallery/06.jpg" class="grid-w33" />
<img src="gallery/07.jpg" class="grid-w33" />
{{< /gallery >}}

## GitHub Card

`github` allows you to quickly link a github repository, all while showing and updating in realtime stats about it, such as the number of stars and forks it has.

| Parameter | Description                                           |
| --------- | ----------------------------------------------------- |
| `repo`    | [String] github repo in the format of `username/repo` |

```md
{{</* github repo="cauliyang/cauliyang" */>}}
```

{{< github repo="cauliyang/cauliyang" >}}

## GitLab Card

`gitlab` allows you to quickly link a GitLab Project (GitLab's jargon for repo).
It displays realtime stats about it, such as the number of stars and forks it has.
Unlike `github` it can't display the main programming language of a project.
Finally custom GitLab instance URL can be provided, as long as the `api/v4/projects/` endpoint is available, making this shortcode compatible with most self-hosted / entreprise deployments.

<!-- prettier-ignore-start -->
| Parameter   | Description                                                            |
|-------------|------------------------------------------------------------------------|
| `projectID` | [String] gitlab numeric ProjectID                                      |
| `baseURL`   | [String] optional gitlab instance URL, default is `https://gitlab.com/` |
<!-- prettier-ignore-end -->

```md
{{</* gitlab projectID="278964" */>}}
```

{{< gitlab projectID="278964" >}}

## Icon

`icon` outputs an SVG icon and takes the icon name as its only parameter. The icon is scaled to match the current text size.

**Example:**

```md
{{</* icon "github" */>}}
```

**Output:** {{< icon "github" >}}

Icons are populated using Hugo pipelines which makes them very flexible. Blowfish includes a number of built-in icons for social, links and other purposes.
Check the [icon samples](https://blowfish.page/samples/icons/) page for a full list of supported icons.
Custom icons can be added by providing your own icon assets in the `assets/icons/` directory of your project. The icon can then be referenced in the shortcode by using the SVG filename without the `.svg` extension.
Icons can also be used in partials by calling the [icon partial](https://blowfish.page/docs/shortcodes/#icon).

<br/><br/><br/>

## Katex

The `katex` shortcode can be used to add mathematical expressions to article content using the KaTeX package.
Refer to the online reference of [supported TeX functions](https://katex.org/docs/supported.html) for the available syntax.
To include mathematical expressions in an article, simply place the shortcode anywhere with the content.
It only needs to be included once per article and KaTeX will automatically render any markup on that page.
Both inline and block notation are supported.
Inline notation can be generated by wrapping the expression in `\\(` and `\\)` delimiters.
Alternatively, block notation can be generated using `$$` delimiters.

**Example:**

```md
{{</* katex */>}}
\\(f(a,b,c) = (a^2+b^2+c^2)^3\\)
```

{{< katex >}}
\\(f(a,b,c) = (a^2+b^2+c^2)^3\\)

## Lead

`lead` is used to bring emphasis to the start of an article.
It can be used to style an introduction, or to call out an important piece of information.
Simply wrap any Markdown content in the `lead` shortcode.

**Example:**

```md
{{</* lead */>}}
When life gives you lemons, make lemonade.
{{</* /lead */>}}
```

{{< lead >}}
When life gives you lemons, make lemonade.
{{< /lead >}}

## List

`List` will display a list of recent articles. This shortcode requires a limit value to constraint the list. Additionally, it supports a `where` and a `value` in order to filter articles by their parameters. Note that this shortcode will not display its parent page but it will count for the limit value.

<!-- prettier-ignore-start -->
| Parameter | Description                                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `limit`   | **Required.** the number of recent articles to display.                                                                                                 |
| `title`   | Optional title for the list, default is `Recent`                                                                                                        |
| `where`   | The variable to be used for the query of articles e.g. `Type`                                                                                           |
| `value`   | The value that will need to match the parameter defined in `where` for the query of articles e.g. for `where` == `Type` a valid value could be `sample` |

{{< alert >}}
The `where` and `value` values are used in the following query `where .Site.RegularPages $where $value` in the code of the shortcode. Check [Hugo docs](https://gohugo.io/variables/page/) to learn more about which parameters are available to use.
{{</ alert >}}

<!-- prettier-ignore-end -->

```md
{{</* list limit=2 */>}}
```

{{< list limit=2 >}}

---

```md
{{</* list title="Samples" limit=5 where="Type" value="sample" */>}}
```

{{< list title="Posts" limit=5 where="Type" value="posts">}}

## Mermaid

`mermaid` allows you to draw detailed diagrams and visualisations using text. It uses Mermaid under the hood and supports a wide variety of diagrams, charts and other output formats.

Simply write your Mermaid syntax within the `mermaid` shortcode and let the plugin do the rest.

Refer to the [official Mermaid docs](https://mermaid-js.github.io/) for details on syntax and supported diagram types.

**Example:**

```md
{{</* mermaid */>}}
graph LR;
A[Lemons]-->B[Lemonade];
B-->C[Profit]
{{</* /mermaid */>}}
```

{{< mermaid >}}
graph LR;
A[Lemons]-->B[Lemonade];
B-->C[Profit]
{{< /mermaid >}}

## Swatches

`swatches` outputs a set of up to three different colors to showcase color elements like a color palette.
This shortcode takes the `HEX` codes of each color and creates the visual elements for each.

```md
{{</* swatches "#64748b" "#3b82f6" "#06b6d4" */>}}
```

**Output**
{{< swatches "#64748b" "#3b82f6" "#06b6d4" >}}

<br/><br/><br/>

## Timeline

The `timeline` creates a visual timeline that can be used in different use-cases, e.g. professional experience, a project's achievements, etc. The `timeline` shortcode relies on the `timelineItem` sub-shortcode to define each item within the main timeline. Each item can have the following properties.

<!-- prettier-ignore-start -->
| Parameter   | Description                                  |
| ----------- | -------------------------------------------- |
| `icon`      | the icon to be used in the timeline visuals. |
| `header`    | header for each entry                        |
| `badge`     | text to place within the top right badge      |
| `subheader` | entry's subheader                            |

<!-- prettier-ignore-end -->

**Example:**

```md
{{</* timeline */>}}

{{</* timelineItem icon="github" header="header" badge="badge test" subheader="subheader" */>}}
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non magna ex. Donec sollicitudin ut lorem quis lobortis. Name ac ipsum libero. Sed a ex eget ipsum tincidunt venenatis quis sed nisl. Pellentesque sed urna vel odio consequat tincidunt id ut purus. Name sollicitudin est sed dui interdum rhoncus.
{{</* /timelineItem */>}}

{{</* timelineItem icon="code" header="Another Awesome Header" badge="date - present" subheader="Awesome Subheader" */>}}
With html code

<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>
{{</* /timelineItem */>}}

{{</* timelineItem icon="star" header="Shortcodes" badge="AWESOME" */>}}
With other shortcodes
{{</* gallery */>}}
<img src="gallery/01.jpg" class="grid-w33" />
<img src="gallery/02.jpg" class="grid-w33" />
<img src="gallery/03.jpg" class="grid-w33" />
<img src="gallery/04.jpg" class="grid-w33" />
<img src="gallery/05.jpg" class="grid-w33" />
<img src="gallery/06.jpg" class="grid-w33" />
<img src="gallery/07.jpg" class="grid-w33" />
{{</* /gallery */>}}
{{</* /timelineItem */>}}

{{</* /timeline */>}}
```

{{< timeline >}}

{{< timelineItem icon="github" header="header" badge="badge test" subheader="subheader" >}}
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non magna ex. Donec sollicitudin ut lorem quis lobortis. Name ac ipsum libero. Sed a ex eget ipsum tincidunt venenatis quis sed nisl. Pellentesque sed urna vel odio consequat tincidunt id ut purus. Name sollicitudin est sed dui interdum rhoncus.
{{</ timelineItem >}}

{{< timelineItem icon="code" header="Another Awesome Header" badge="date - present" subheader="Awesome Subheader">}}
With html code

<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>
{{</ timelineItem >}}

{{< timelineItem icon="star" header="Shortcodes" badge="AWESOME" >}}
With other shortcodes
{{< gallery >}}
<img src="gallery/01.jpg" class="grid-w33" />
<img src="gallery/02.jpg" class="grid-w33" />
<img src="gallery/03.jpg" class="grid-w33" />
<img src="gallery/04.jpg" class="grid-w33" />
<img src="gallery/05.jpg" class="grid-w33" />
<img src="gallery/06.jpg" class="grid-w33" />
<img src="gallery/07.jpg" class="grid-w33" />
{{< /gallery >}}
{{</ timelineItem >}}

{{</ timeline >}}

## TypeIt

[TypeIt](https://www.typeitjs.com) is the most versatile JavaScript tool for creating typewriter effects on the planet.
With a straightforward configuration, it allows you to type single or multiple strings that break lines, delete & replace each other, and it even handles strings that contain complex HTML.

Blowfish implements a sub-set of TypeIt features using a `shortcode`.
Write your text within the `typeit` shortcode and use the following parameters to configure the behavior you want.

<!-- prettier-ignore-start -->
| Parameter          | Description                                                                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tag`              | [String] `html` tag that will be used to render the strings.                                                                                       |
| `classList`        | [String] List of `css` classes to apply to the `html` element.                                                                                     |
| `initialString`    | [String] Initial string that will appear written and will be replaced.                                                                             |
| `speed`            | [number] Typing speed, measured in milliseconds between each step.                                                                                 |
| `lifeLike`         | [boolean] Makes the typing pace irregular, as if a real person is doing it.                                                                        |
| `startDelay`       | [number] The amount of time before the plugin begins typing after being initialized.                                                               |
| `breakLines`       | [boolean] Whether multiple strings are printed on top of each other (true), or if they're deleted and replaced by each other (false).              |
| `waitUntilVisible` | [boolean] Determines if the instance will begin when loaded or only when the target element becomes visible in the viewport. The default is `true` |
| `loop`             | [boolean] Whether your strings will continuously loop after completing                                                                             |

<!-- prettier-ignore-end -->

**Example 1:**

```md
{{</* typeit */>}}
Lorem ipsum dolor sit amet
{{</* /typeit */>}}
```

{{< typeit >}}
Lorem ipsum dolor sit amet
{{< /typeit >}}

**Example 2:**

```md
{{</* typeit tag=h1 lifeLike=true */>}}
Lorem ipsum dolor sit amet,
consectetur adipiscing elit.
{{</* /typeit */>}}
```

<!-- prettier-ignore-start -->
{{< typeit
  tag=h1
  lifeLike=true
>}}
Lorem ipsum dolor sit amet,
consectetur adipiscing elit.
{{< /typeit >}}



**Example 3:**

```md
{{</* typeit
  tag=h3
  speed=50
  breakLines=false
  loop=true
*/>}}
Lorem ipsum dolor sit amet,
consectetur adipiscing elit.
{{</* /typeit */>}}
```

{{< typeit
  tag=h3
  speed=50
  breakLines=false
  loop=true
>}}
"Frankly, my dear, I don't give a damn." Gone with the Wind (1939)
"I'm gonna make him an offer he can't refuse." The Godfather (1972)
"Toto, I've a feeling we're not in Kansas anymore." The Wizard of Oz (1939)
{{< /typeit >}}

<!-- prettier-ignore-end -->
