---
title: How to Use the Noodles Library in Rust
description: A practical walkthrough of the Rust noodles crate for reading BAM files, with benchmarks and the pitfalls I wish I had known earlier.
categories: ["Bioinformatics", "Software Development"]
tags: ["Rust"]
date: 2023-03-04
featured: false
draft: false
image: "https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/8181fb89117181.5df79fa1c59fb.png"
---

## Introduction

[Noodles] and [rust-htslib] are the two most widely used Rust libraries for working with genomic data.
Both target the same file formats, but they take different approaches.
This post walks through noodles, compares it with [rust-htslib], and collects the pitfalls I ran into along the way.

Noodles is a pure-Rust library built on the standard library's I/O and byte-manipulation tools for reading, writing, and manipulating genomic data files.
It is fast, scalable, and highly modular, and it leans on Rust idioms such as iterators and closures, which makes it flexible across different use cases.

[rust-htslib], on the other hand, is a high-level Rust interface to the HTSlib C library.
It focuses on BAM and VCF files and offers a robust, battle-tested set of functions for those formats.

{{< github repo="zaeleus/noodles" >}}

## Setup

Add noodles as a dependency with `cargo add noodles --features bam sam bgzf core`, or edit `Cargo.toml` directly:

```toml
noodles = { version = "0.32.0", features = ["bam", "sam", "bgzf", "core"] }
```

## Reading a BAM file

Noodles offers several ways to read a BAM file: eagerly, lazily, and, combined with the rayon crate, in parallel.
The following function opens a BAM file and prints the name of every record:

```rust
use noodles::bam;
use noodles::sam;
use std::fs::File;

fn read_bam(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut reader = File::open(path).map(bam::Reader::new)?;
    let header: sam::Header = reader.read_header()?.parse()?;
    reader.read_reference_sequences()?;

    reader
        .records(&header)
        .map(|r| r.unwrap())
        .for_each(|record| {
            println!("read name: {}", record.read_name().unwrap());
        });

    Ok(())
}
```

Before reading records, we have to consume the **header** and the **reference sequences** so that the file handle points at the first record.

The next version does the same job with lazy records.
I named these functions `*_async` when I wrote them, but note that they use noodles' `lazy_records()` rather than async I/O:

```rust
use noodles::bam;
use noodles::sam;
use std::fs::File;

fn read_bam_async(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut reader = File::open(path).map(bam::Reader::new)?;
    let header: sam::Header = reader.read_header()?.parse()?;
    reader.read_reference_sequences()?;

    reader
        .lazy_records()
        .map(|r| r.unwrap())
        .for_each(|record| {
            println!("read name: {}", record.read_name().unwrap().unwrap());
        });

    Ok(())
}
```

I benchmarked both with [hyperfine].
On a BAM file with 144,309 records, `read_bam_async()` is 1.5 times faster than `read_bam()`.

![hyperfine benchmark comparing read_bam_async with read_bam](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/20230303222130.png)

Two things differ from the first version: `lazy_records()` replaces `records()`, and the read name now needs `read_name().unwrap().unwrap()` instead of `read_name().unwrap()`.
The reason is that `lazy_records()` yields `noodles::bam::reader::LazyRecords`, whereas `records()` yields `noodles::sam::reader::Records`.
The two types expose different methods, and `Records` has far more of them.
For instance, the `cigar` returned by a lazy record is not directly usable, unlike the one returned by `Records`.
Consequently, we have to rebuild some `sam::record` data structures from the lazy record.
The following example reconstructs `Data`, `Cigar`, and `Sequence` from each lazy record:

```rust
// File: read_bam_async
use anyhow::Context;
use noodles::bam;
use noodles::sam;
use std::fs::File;
use sam::record::cigar::Cigar;
use sam::record::data::Data;


fn read_bam_async(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut reader = File::open(path).map(bam::Reader::new)?;
    let header: sam::Header = reader.read_header()?.parse()?;
    reader.read_reference_sequences()?;

    reader
        .lazy_records()
        .map(|r| r.unwrap())
        .for_each(|record| {
            let read_name = record.read_name().unwrap().unwrap();
            let data = Data::try_from(record.data())
                .with_context(|| format!("failed to get data {}", read_name))
                .unwrap();

            let cigar = Cigar::try_from(record.cigar())
                .with_context(|| format!("failed to get cigar {}", read_name))
                .unwrap();

            let sequence = sam::record::Sequence::try_from(record.sequence())
                .with_context(|| format!("failed to get sequence {}", read_name))
                .unwrap();

            println!("read name: {}, cigar: {}", read_name, cigar);
        });

    Ok(())
}
```

The reconstructed `Data` and `Cigar` give us access to tags and fields that the lazy versions do not expose.
Another useful trick is to convert the `Sequence` returned by either reader into `noodles::fasta::record::Sequence`, which makes the reverse complement a one-liner: `let rev_comp: Sequence = sequence.complement().rev().collect::<Result<_, _>>()?;`
Running this on a sample input produces the following output:

![Terminal output listing read names and CIGAR strings](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/202303032236655.png)

Note the use of `anyhow::Context` to attach a descriptive message to any error.
[Anyhow] makes error handling in Rust application code considerably easier.

## Processing records in parallel

Rust's ownership model enables fearless concurrency, and the rayon crate builds on it to provide parallel iterators with almost no ceremony.
Add it with `cargo add rayon`.
The example below is the lazy reader from above with a single `par_bridge()` call that turns the record iterator into a parallel one; the `sleep` simulates real work so that the speedup is measurable:

```rust
// File: read_bam_async_rayon
use anyhow::Context;
use noodles::bam;
use noodles::sam;
use rayon::prelude::*;
use std::fs::File;
use sam::record::cigar::Cigar;
use sam::record::data::Data;
use std::thread::sleep;

fn read_bam_async_rayon(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut reader = File::open(path).map(bam::Reader::new)?;
    let header: sam::Header = reader.read_header()?.parse()?;
    reader.read_reference_sequences()?;

    reader
        .lazy_records()
        .par_bridge() // convert to parallel iterators
        .map(|r| r.unwrap())
        .for_each(|record| {
            let read_name = record.read_name().unwrap().unwrap();
            let data = Data::try_from(record.data())
                .with_context(|| format!("failed to get data {}", read_name))
                .unwrap();

            let cigar = Cigar::try_from(record.cigar())
                .with_context(|| format!("failed to get cigar {}", read_name))
                .unwrap();

            let sequence = sam::record::Sequence::try_from(record.sequence())
                .with_context(|| format!("failed to get sequence {}", read_name))
                .unwrap();

            sleep(std::time::Duration::from_millis(1000)); // for benchmarking
            println!("read name: {}, cigar: {}", read_name, cigar,);
        });

    Ok(())
}
```

With four threads and an input of three records, the parallel version is about three times faster than the sequential one, which is what you would expect once the overhead of launching and joining threads is taken into account.

![hyperfine benchmark comparing the parallel and sequential lazy readers](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/202303032324255.png)

For comparison, I also benchmarked reading records without the lazy reader:

![hyperfine benchmark of reading records with the non-lazy reader](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/202303032320110.png)

## Querying a region

Querying records in a specific region requires an index file.
Like rust-htslib, noodles provides an indexed reader for this.
The following program counts the records that overlap `chr17:79778148-79778149`:

```rust
use anyhow::{Context, Result};
use noodles::bam;
use noodles::sam;
use std::path::Path;

fn query<T>(path: T) -> Result<()>
where
    T: AsRef<Path>,
{
    let mut reader = bam::indexed_reader::Builder::default()
        .build_from_path(path.as_ref())
        .with_context(|| {
            format!(
                "failed to read bam file and index not existed {:?} ",
                path.as_ref()
            )
        })?;

    let header: sam::Header = reader
        .read_header()
        .context("failed to read bam reader")?
        .parse()
        .context("failed to parse bam rader")?;

    let reference = reader
        .read_reference_sequences()
        .context("failed to read reference sequences")?;

    let region = "chr17:79778148-79778149"
        .parse()
        .expect("failed to parse region");

    let count = reader.query(&header, &region).unwrap().count();
    println!("{} records found", count);

    Ok(())
}

fn main() {
    let path = std::env::args().nth(1).unwrap();
    query(path).unwrap();
}
```

{{< alert icon="triangle-exclamation" >}}
`IndexedReader` expects the index to be named `file_name.bam.bai`, not `file_name.bai`.
If your index does not follow this convention, you will get an error such as _file does not exist_.
{{< /alert >}}

The query iterator also works with rayon; a single `par_bridge()` parallelizes the count:

```rust
let count = reader.query(&header, &region).unwrap().par_bridge().count();
// let count = reader.query(&header, &region).unwrap().count();
```

## Pitfalls

### BAM/SAM header format

Noodles is much stricter than rust-htslib about the [SAM format] specification when parsing headers.
A non-compliant header fails with an error such as "Invalid ReadGroup for PL".
In that case the _PL_ value of the _RG_ tag is not one of the values the specification allows; _PACBIO_, for example, is valid.
The strictness of header parsing has been discussed in a noodles [issue].
The fix is to rewrite the _RG_ tag in place with `samtools addreplacerg -r "@RG\tID:test\tSM:hs\tLB:ga\tPL:PACBIO" -w input.bam -o output.bam` before processing the file.
**Do not forget** to re-index the new file if you want to query regions.

### IndexedReader

As mentioned above, `IndexedReader` loads the index for you.
However, it does not expose the same API as `Reader`, and its `Cigar` and `Data` types differ from those used by `Reader`.
The workaround is the same reconstruction shown earlier.

### Reading a file twice

Seeking back to the first record is necessary if you want to iterate over the whole file again, but not if you only want to run another region query.
Iterating over all records moves the file handle to the end of the file, so a second pass over the same handle yields nothing.
Before reading records again, the header and reference sequences must be consumed once more to position the handle at the first record.

There are two ways around this.
The first is to reopen the file and consume the header and reference sequences again.
The second is to seek the existing handle back to the start of the file.
Noodles does not expose an API for the latter, so the following extension trait implements it on top of the underlying BGZF reader:

```rust
use noodles::bam;
use noodles::sam;
use noodles::bgzf;

use std::io::{self, Read, Seek};

pub trait NoodleBamIndexReaderExt {
    fn seek_to_first_record(&mut self) -> io::Result<bgzf::VirtualPosition>;
}

impl<R> NoodleBamIndexReaderExt for bam::indexed_reader::IndexedReader<bgzf::Reader<R>>
where
    R: Read + Seek,
{
    fn seek_to_first_record(&mut self) -> io::Result<bgzf::VirtualPosition> {
        // seek to first record
        let areader = self.get_mut();
        areader.seek(bgzf::VirtualPosition::default())?;
        self.read_header()?;
        self.read_reference_sequences()?;
        Ok(self.get_ref().virtual_position())
    }
}
```

This trait adds a `seek_to_first_record()` method to `IndexedReader`.
To see why it is needed, the following function counts the records twice with the same reader:

```rust
fn count<T>(path: T) -> Result<()>
where
    T: AsRef<Path>,
{
    let mut reader = bam::indexed_reader::Builder::default()
        .build_from_path(path.as_ref())
        .with_context(|| {
            format!(
                "failed to read bam file and index not existed {:?} ",
                path.as_ref()
            )
        })?;

    let header: sam::Header = reader
        .read_header()
        .context("failed to read bam reader")?
        .parse()
        .context("failed to parse bam rader")?;

    let reference = reader
        .read_reference_sequences()
        .context("failed to read reference sequences")?;

    let count1 = reader.lazy_records().count();
    println!("first count: {}", count1);

    let count2 = reader.lazy_records().count();
    println!("second count: {}", count2);

    Ok(())
}
```

The second count is zero:

![Terminal output showing a non-zero first count and a zero second count](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/202303032358259.png)

With the extension trait, a single call between the two passes resets the reader:

```rust
fn count<T>(path: T) -> Result<()>
where
    T: AsRef<Path>,
{
    let mut reader = bam::indexed_reader::Builder::default()
        .build_from_path(path.as_ref())
        .with_context(|| {
            format!(
                "failed to read bam file and index not existed {:?} ",
                path.as_ref()
            )
        })?;

    let header: sam::Header = reader
        .read_header()
        .context("failed to read bam reader")?
        .parse()
        .context("failed to parse bam rader")?;

    let reference = reader
        .read_reference_sequences()
        .context("failed to read reference sequences")?;

    let count1 = reader.lazy_records().count();
    println!("first count: {}", count1);

    reader.seek_to_first_record().unwrap(); // important

    let count2 = reader.lazy_records().count();
    println!("second count: {}", count2);
    Ok(())
}
```

After the reset, the records can be iterated again as before.
No reset is needed between region queries.

![Terminal output showing two identical counts after resetting the reader](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/202303040001670.png)

### Off-by-one errors

Noodles uses 1-based positions and a closed range, `[start, end]`, when retrieving a sequence.
Rust uses 0-based positions, and its default range is half-open, `[start, end)`.
You therefore have to add 1 to the start position when retrieving a sequence with noodles; otherwise you will get an off-by-one error.

### Getting a reference name

Getting the reference sequence name of a record is not intuitive in noodles.
This helper looks the name up by index in the header's reference sequences:

```rust
fn get_reference_name(references: &ReferenceSequences, reference_sequence_id: usize) -> String {
    references
        .get_index(reference_sequence_id)
        .map(|(name, _)| name.as_str())
        .unwrap()
        .to_owned()
}
```

The index comes from `record.reference_sequence_id()`.

## Conclusion

Noodles is much younger than rust-htslib, which has been around longer and is used in many projects.
Noodles may therefore still contain undiscovered bugs, whereas rust-htslib has been tested extensively and has proven to be a reliable, high-performance option.

Both are valuable libraries for working with genomic data in Rust, and each has its trade-offs.
The right choice depends on the project: noodles, as a pure-Rust implementation, is the better option when flexibility and adaptability matter most.
The sample code for this post lives in the repository below.

{{< github repo="cauliyang/noodles_blog" >}}

<!-- links -->

[noodles]: https://github.com/zaeleus/noodles
[rust-htslib]: https://github.com/rust-bio/rust-htslib
[sam format]: https://samtools.github.io/hts-specs/SAMv1.pdf
[issue]: https://github.com/zaeleus/noodles/issues/111
[hyperfine]: https://crates.io/crates/hyperfine
[anyhow]: https://docs.rs/anyhow/latest/anyhow/
[repository]: https://github.com/cauliyang/noodles_blog

{{< signoff >}}
