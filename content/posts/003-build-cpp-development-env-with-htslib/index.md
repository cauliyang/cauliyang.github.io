---
title: Building a C++ Development Environment With htslib
description: How I set up a productive C++ environment for bioinformatics work, including htslib, build tools, and dependency management without root access.
categories: ["Bioinformatics", "Software Development"]
tags: ["C++"]
date: 2022-06-15
featured: false
draft: false
---

## Configure the compile environment

I am planning to develop a tool in C++ that runs on both Linux and macOS.
The recurring obstacle is that I usually lack root access, so I cannot simply run `apt-get install` for dependencies on Ubuntu.
Working through the dependency chain and compiling each library by hand takes anywhere from a night to a week.

One solution is a package manager such as [Conda], best known in data science but with good support for C++, Rust, and R as well.
Package names change over time, so always search for the current name before installing.
Conda is a practical way to install C++ dependencies, particularly in bioinformatics.
Other C++ dependency managers exist too, such as [Vcpkg] and [Conan]; I use [CPM] as an alternative.

### Install GCC or Clang

You first need a compiler, and [GCC] or [Clang] are the usual choices.
Linux systems ship with GCC, but the version may be old (4.9, for example), which rules out recent C++ features, and again you may not have root access.
With Conda you can install any version of GCC or Clang without root.

{{< steps >}}
{{< step number="1" title="Find the right package" >}}
Search for GCC or Clang on [Conda cloud](https://anaconda.org/) first so you install the proper version.
{{< /step >}}
{{< step number="2" title="Install the compiler" >}}

```bash
conda install -c conda-forge gcc
# or
conda install -c conda-forge clang
```

{{< /step >}}
{{< step number="3" title="Check the compiler flags" >}}
After installation, Conda may set three important variables for you: `CFLAGS`, `CXXFLAGS`, and `LDFLAGS`. Check with `echo $CFLAGS`. If they are missing, set them in `~/.bashrc` or `~/.zshrc`.
{{< /step >}}
{{< /steps >}}

Here are the values from my setup:

```bash
export CXXFLAGS="-fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /your_conda_absolute_path/miniconda3/include"
```

```bash
export CFLAGS="-march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /your_conda_absolute_path/include"
```

```bash
export LDFLAGS="-Wl,-O2 -Wl,--sort-common -Wl,--as-needed -Wl,-z,relro -Wl,-z,now -Wl,--disable-new-dtags -Wl,--gc-sections -Wl,--allow-shlib-undefined -Wl,-rpath,/your_conda_absolute_path/miniconda3/lib -Wl,-rpath-link,/your_conda_absolute_path/miniconda3/lib -L/your_conda_absolute_path/miniconda3/lib"
```

{{< alert icon="triangle-exclamation" >}}
Replace `/your_conda_absolute_path` with the absolute path of your own Conda installation.
{{< /alert >}}

I installed these in the base environment, and I recommend installing GCC or Clang there as well.

## Add htslib dependencies

[Htslib] is the classic library for reading and writing bioinformatics file formats, including BAM, SAM, VCF, and BCF.

Htslib is implemented in C to meet high performance requirements.
Many popular tools, such as [samtools] and [bcftools], are built on it.
Wrappers exist for other languages, including [pysam] for Python, [rhtslib] for R, and rust-htslib for Rust, so htslib can be used from whichever language you prefer.

[Zlib] is the only hard dependency of htslib.
The remaining dependencies are optional and each unlocks extra features; I will not go through them here, but the [Htslib] website documents them in detail.
Conda installs htslib in one step with `conda install htslib`, and you can pin a version with `conda install htslib=1.15.1`.
If samtools or bcftools are already installed in your environment, htslib is likely there too.

### CMake scripts

I use [CMake] as the build system, and the following scripts have fixed most of my htslib dependency problems.
You are welcome to use them in your own project.

- [htslib.cmake]
- [FindHTSlib.cmake]
- [FindDeflate.cmake]
- [zlib.cmake]

I assume your directory structure looks like this:

```text
.
├── CMakeLists.txt
├── build
├── cmake
├── include
└── source
```

Put the scripts in the `cmake` directory and include them from `CMakeLists.txt`:

```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(htslib)
```

If htslib is found in your environment, CMake defines `HTSlib_FOUND`, `HTSlib_INCLUDE_DIRS`, and `HTSlib_LIBRARIES`.
Otherwise, CMake builds a static htslib from source, checking for each optional dependency in turn.
If a dependency exists, CMake enables the corresponding htslib feature; if not, it disables the related configure flag.
Zlib is the one dependency that must exist, so if it is missing, CMake builds it from source as well.

`FindHTSlib.cmake` does the actual search for htslib.
`htslib.cmake` is shown below with comments explaining how it works.

```cmake
include(ExternalProject)

# find htslib by using FindHTSlib.cmake
find_package(HTSlib)
if(HTSlib_FOUND)
  message(STATUS "HTSlib_USE_STATIC_LIBS: ${HTSlib_USE_STATIC_LIBS}")

  # not found, try to build it to static libs from source
else()
  set(htslib_PREFIX ${CMAKE_BINARY_DIR}/cmake-ext/htslib-prefix)
  set(htslib_INSTALL ${CMAKE_BINARY_DIR}/cmake-ext/htslib-install)

  if(CMAKE_GENERATOR STREQUAL "Unix Makefiles")
    set(MAKE_COMMAND "$(MAKE)")
  else()
    find_program(MAKE_COMMAND NAMES make gmake)
  endif()

  message(STATUS "Building static htslib from source")
  message(NOTICE "Set ENV CFLAGS and CXXFLAGS if you use conda environment!")

  set(disable_flags --disable-gcs --disable-s3 --disable-plugins)

  # find lzma; if not found, disable the compiler flags
  find_package(LibLZMA)
  if(LIBLZMA_FOUND)
    include_directories(SYSTEM ${LIBLZMA_INCLUDE_DIRS})
    list(APPEND deps_LIB ${LIBLZMA_LIBRARIES})
  else()
    list(APPEND disable_flags --disable-lzma)
  endif()

  # find curl; if not found, disable the compiler flags
  find_package(CURL)
  if(CURL_FOUND)
    include_directories(SYSTEM ${CURL_INCLUDE_DIRS})
    list(APPEND deps_LIB ${CURL_LIBRARIES})
  else()
    list(APPEND disable_flags --disable-libcurl)
  endif()

  # find bzip2; if not found, disable the compiler flags
  find_package(BZip2)
  if(BZIP2_FOUND)
    include_directories(SYSTEM ${BZIP2_INCLUDE_DIRS})
    list(APPEND deps_LIB ${BZIP2_LIBRARIES})
  else()
    list(APPEND disable_flags --disable-bz2)
  endif()

  # find deflate; if not found, disable the compiler flags
  find_package(Deflate)
  if(Deflate_FOUND)
    include_directories(SYSTEM ${Deflate_INCLUDE_DIRS})
    list(APPEND deps_LIB ${Deflate_LIBRARIES})
  endif()

  message(STATUS " dependencies: ${deps_LIB}")
  # compile and install htslib from source
  ExternalProject_Add(
    htslib
    PREFIX ${htslib_PREFIX}
    URL https://github.com/samtools/htslib/releases/download/1.15.1/htslib-1.15.1.tar.bz2
    BUILD_IN_SOURCE 1
    UPDATE_COMMAND ""
    CONFIGURE_COMMAND autoreconf -i && ./configure --prefix=${htslib_PREFIX} ${disable_flags}
    BUILD_COMMAND ${MAKE_COMMAND} lib-static
    INSTALL_COMMAND ${MAKE_COMMAND} install prefix=${htslib_INSTALL}
  )

  # user-defined variable (-DZLIB_BUILD=ON) controls whether zlib is built from source
  message(STATUS "ZLIB_BUILD: ${ZLIB_BUILD}")
  if(ZLIB_BUILD)
    include(cmake/zlib.cmake)
    add_dependencies(htslib zlib)
  else()
    find_package(ZLIB)
    if(ZLIB_FOUND)
      include_directories(SYSTEM ${ZLIB_INCLUDE_DIRS})
      list(APPEND deps_LIB ${ZLIB_LIBRARIES})
    else()
      # build zlib from source
      message(STATUS "Building zlib from source")
      include(cmake/zlib.cmake)
      add_dependencies(htslib zlib)
      list(APPEND deps_LIB ${zlib_LIBRARIES})
    endif()
  endif()
  list(APPEND deps_LIB ${zlib_LIBRARIES})

  # define two variables for downstream use
  set(HTSlib_INCLUDE_DIRS ${htslib_INSTALL}/include)
  set(HTSlib_LIBRARIES ${htslib_INSTALL}/lib/libhts.a ${deps_LIB})
  message(STATUS "HTSlib_INCLUDE_DIRS: ${HTSlib_INCLUDE_DIRS}")
  message(STATUS "HTSlib_LIBRARIES: ${HTSlib_LIBRARIES}")

endif()
```

Now you can link against htslib like this:

```cmake
add_library(test test.h test.cpp)

# if htslib is not in your environment
if(NOT HTSlib_FOUND)
  # if htslib is built from source you need to add this
  add_dependencies(${PROJECT_NAME} htslib)
endif()

target_link_libraries(test PRIVATE ${HTSlib_LIBRARIES})
target_include_directories(test PRIVATE ${HTSlib_INCLUDE_DIRS} ${HTSlib_INCLUDE_DIRS}/htslib)
```

Change `PRIVATE` to `PUBLIC` if you want to export htslib to dependents of your target.

## Recommended practices

Start with a sensible directory structure. A few good templates:

- <https://github.com/TheLartians/ModernCppStarter>
- <https://github.com/cpp-best-practices/gui_starter_template>
- <https://github.com/filipdutescu/modern-cpp-template>

I prefer the first one.
A good template also introduces you to the surrounding tooling, and once you dig into one you will learn more than you expect.

## Summary

This post covered how to install C++ dependencies without root access and how to configure htslib in your development environment.
The CMake scripts linked above should resolve most htslib dependency problems.
If you have any questions, feel free to reach out.

{{< signoff >}}

<!---link--->

[bcftools]: http://samtools.github.io/bcftools/bcftools.html
[clang]: https://clang.llvm.org/
[cmake]: https://cmake.org/
[conan]: https://conan.io/
[conda]: https://docs.conda.io/en/latest/
[conda cloud]: https://anaconda.org/
[cpm]: https://github.com/cpm-cmake/CPM.cmake
[finddeflate.cmake]: https://gist.github.com/cauliyang/a39f3b10ed3d85d2ca13645d81dd829e
[findhtslib.cmake]: https://gist.github.com/cauliyang/01f360df26fa287a1e111dd00bb076e4
[gcc]: https://gcc.gnu.org/
[htslib]: https://github.com/samtools/htslib
[htslib.cmake]: https://gist.github.com/cauliyang/c6d69c43a8a05266c6d05bc2c5324f45
[pysam]: https://github.com/pysam-developers/pysam
[rhtslib]: https://bioconductor.org/packages/release/bioc/html/Rhtslib.html
[samtools]: http://www.htslib.org/
[vcpkg]: https://vcpkg.io/en/index.html
[zlib]: https://zlib.net/
[zlib.cmake]: https://gist.github.com/cauliyang/0aa4487e58a0e5c830915ddbade5ce71
