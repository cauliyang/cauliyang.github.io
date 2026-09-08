---
title: "Pybox: A Small Toolbox for Everyday Research Tasks"
description: Pybox is my Python command-line toolbox for recurring chores such as Google Drive downloads, Slack messages, and async downloads.
categories: ["Software Development", "Tools"]
tags: ["Python", "CLI"]
date: 2021-12-03
featured: false
draft: false
heroStyle: thumbAndBackground
---

## Why Pybox

I kept searching for the same commands over and over: how to download a file from Google Drive from the command line, how to post a message to Slack from a script.
**Pybox** is my answer: a Python command-line toolbox that collects these small utilities in one place.
It grows whenever I find another command worth keeping.
Current features:

- Download files from Google Drive, both single files and whole folders
- Send messages to Slack channels
- Download many files asynchronously

{{< alert icon="circle-info" >}}
Downloading a whole Google Drive folder requires authentication through the Google API.
{{< /alert >}}

{{< github repo="cauliyang/pybox" >}}

## Installation

Pybox is published on [PyPI]:

```bash
pip install pyboxes
```

A [Conda] package is planned:

```bash
conda install pyboxes  # Coming soon
```

## Usage

Run `pybox -h` to see the available commands:

```text
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

## Features

- [A simple and easy to download files by sharing link]
- [A simple and easy to send message to Slack Channel]
- [Download multiple files asynchronously]
- ~~Download books from Z-Library by title~~

I plan to keep adding commands as I find them useful, and to keep the existing ones tested and reliable.
If there is a command or feature you would like to see, open an issue and we can discuss it.

## Take a tour

### Download files from Google Drive

Download a single file from a sharing link:

```console
$ pybox gfile <url> <name> <size>
```

Download every file in a folder, given a client ID and folder ID:

```console
$ pybox gfolder <client_id> <folder_id>
```

See the [usage documentation] for details.

### Send a message to a Slack channel

```console
$ pybox slack [options] <webhook-url>
```

See the [usage documentation] for details.

### Download multiple files asynchronously

Download a single file:

```console
$ pybox asyncdown -u <url> -o <output>
```

Download multiple files listed in a text file:

```console
$ pybox asyncdown -f <url-file>
```

For example, suppose `urls.txt` has the file name in the first column and the download URL in the second.
`pybox asyncdown -f urls.txt` downloads all of them in parallel.

```text
ENCFF888ZZV.fastq.gz https://www.encodeproject.org/files/ENCFF888ZZV/@@download/ENCFF888ZZV.fastq.gz
ENCFF883SEZ.fastq.gz https://www.encodeproject.org/files/ENCFF883SEZ/@@download/ENCFF883SEZ.fastq.gz
ENCFF035OMK.fastq.gz https://www.encodeproject.org/files/ENCFF035OMK/@@download/ENCFF035OMK.fastq.gz
ENCFF288CVJ.fastq.gz https://www.encodeproject.org/files/ENCFF288CVJ/@@download/ENCFF288CVJ.fastq.gz
```

## Contributing

Contributions are welcome: fork the project on [GitHub] and read the [contributing guide] before you start.
Please make sure all tests pass before opening a pull request.

{{< signoff >}}

<!-- link -->

[a simple and easy to download files by sharing link]: https://github.com/cauliyang/pybox#a-simple-and-easy-to-download-files-by-sharing-link
[a simple and easy to send message to slack channel]: https://github.com/cauliyang/pybox#a-simple-and-easy-to-send-message-to-slack-channel
[conda]: https://conda.io/
[contributing guide]: https://github.com/cauliyang/pybox/blob/main/CONTRIBUTING.md
[download multiple files asynchronously]: https://github.com/cauliyang/pybox#download-multiple-files-asynchronously
[github]: https://github.com/cauliyang/pybox
[google driver]: https://drive.google.com/
[pypi]: https://pypi.org/project/pyboxes/
[usage documentation]: https://github.com/cauliyang/pybox
