---
title: "Pybox: A Python Toolbox for Common Development Tasks"
description: A collection of useful command-line utilities to streamline everyday development workflows.
tags: ["Python", "Development", "CLI", "Tools"]
categories: ["Python"]
date: 2021-12-03T00:03:50-06:00
featured: false
draft: false
heroStyle: thumbAndBackground
---

## Introduction

Have you ever found yourself repeatedly searching for commands to download files from Google Drive or send messages to Slack? I created **Pybox** to solve this problem - a Python-based command-line toolbox that consolidates useful utilities for common development tasks.

This project continues to evolve as I discover new commands worth sharing. Current features include:
- Downloading files from Google Drive (both individual files and entire folders)
- Sending messages to Slack channels
- Asynchronous file downloads
- And more utilities being added regularly

**Note:** Downloading files from Google Drive folders requires authentication through the Google API.

## Installation

Pybox is available on PyPI for easy installation:

```bash
pip install pyboxes
```

Future plans include publishing to Conda for alternative installation:

```bash
conda install pyboxes  # Coming soon
```

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
