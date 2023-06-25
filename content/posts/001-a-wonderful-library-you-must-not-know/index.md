---
title: A Python Toolbox - Pybox
description: A toolbox including a batch of useful commands for annoying tasks.
tags: ["Develop"]
categories: ["Python"]
date: 2021-12-03T00:03:50-06:00
featured: false
draft: false
# image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/logo.png"
heroStyle: thumbAndBackground
---

## 0. Changes

- [x] Add usage

## 1. Introduction

I have been considering a collection of useful commands for everyday tasks, as many have requested such a tool.
In order to make this collection as user-friendly as possible, I have decided to develop a project, which I hope will prove valuable for others as well.
As I come across new commands that I find useful, I will continue to add them to this toolbox.
Currently, the toolbox includes a command for downloading files from [Google Driver], which can download both individual files and those within a folder, though downloading files within a folder requires authentication through the Google API.
Additionally, this project, dubbed **Pybox**, as it is based on Python, includes other features listed below.

## 2. Installation

The library is available on [pypi] so that you can install it with `pip` or `pip3` by typing `pip install pyboxes`.
I also have plan to publish this library on [Conda] so that you can install it with `conda install pyboxes`.

## 3. Usage

```shell
$ pybox -h # show help
Usage: pybox [options] <command>

  This tool include a bunch of useful commands:

  1. Download single file or all files in a folder for Google Driver
  2. Send message to Slack
  3. more to come...

Options:
  -h, --help  Show this message and exit.

Commands:
  asAyncdown  Download files in terms of links asynchronously.
  gfile      Download file in Google Driver.
  gfolder    Download files in folders in Google Drive.
  slack      Send message to Slack.

  Yangyang-Li https://yangyangli.top/ 2022
```

## 4. Features

- [A simple and easy to download files by sharing link]
- [A simple and easy to send message to Slack Channel]
- [Download multiple files asynchronously]
- ~~Download Books from Zlib in terms of Title Will come!~~

I intend to continually expand the functionality of this toolbox by adding new commands as I discover their utility.
Furthermore, I am committed to ensuring the quality and reliability of this toolbox.
Please let me know if there i s specific command or feature you would like to see, and we can discuss it further.

## 5. 🚌 Take a tour

### A simple and easy to download files by sharing link

#### 1. Download single file by sharing link of Google Driver.

```console
$ pybox gfile <url> <name> <size>
```

#### 2. Download files in a folder by client id and folder id.

```console
$ pybox gfolder <client_id> <folder_id>
```

Detailed usage please see [Usage Documentation]

### A simple and easy to send message to Slack Channel

```console
$ pybox slack [options] <webhook-url>
```

Detailed usage please see [Usage Documentation]

### Download multiple files asynchronously

#### 1. Download single file.

```console
$ pybox asyncdown -u <url> -o <output>
```

#### 2. Download multiple files.

```console
$ pybox asyncdown -f <url-file>
```

For example, suppose `urls.txt` in which the first column is the file name and the second column is the download url.
`pybox asyncdown -f urls.txt` will download all files in parallel.

```txt
ENCFF888ZZV.fastq.gz https://www.encodeproject.org/files/ENCFF888ZZV/@@download/ENCFF888ZZV.fastq.gz
ENCFF883SEZ.fastq.gz https://www.encodeproject.org/files/ENCFF883SEZ/@@download/ENCFF883SEZ.fastq.gz
ENCFF035OMK.fastq.gz https://www.encodeproject.org/files/ENCFF035OMK/@@download/ENCFF035OMK.fastq.gz
ENCFF288CVJ.fastq.gz https://www.encodeproject.org/files/ENCFF288CVJ/@@download/ENCFF288CVJ.fastq.gz
```

## 5. Contributing

If you would like to contribute to this toolbox, please feel free to fork it on [GitHub].
Please make sure you read the [contributing guide] before you start.
Also, please make sure you pass all the tests before you pull request.

<!-- link -->

[a simple and easy to download files by sharing link]: https://github.com/cauliyang/pybox#a-simple-and-easy-to-download-files-by-sharing-link
[a simple and easy to send message to slack channel]: https://github.com/cauliyang/pybox#a-simple-and-easy-to-send-message-to-slack-channel
[conda]: https://conda.io/
[contributing guide]: https://github.com/cauliyang/pybox/blob/main/CONTRIBUTING.md
[download multiple files asynchronously]: https://github.com/cauliyang/pybox#download-multiple-files-asynchronously
[github]: https://github.com/cauliyang/pybox
[google driver]: https://drive.google.com/
[pypi]: https://pypi.org/project/pyboxes/
