
# Iceoryx2 Installation

Iceoryx2 is a decentralized inter-process communication (IPC) library designed to enable ultra-fast, "zero-copy" data exchange between applications and processes. Developed by the Eclipse Foundation and ekxide, it is specifically built for data-intensive, real-time systems like robotics and autonomous driving.

Installation directions adapted from: [iceoryx2-cxx README](https://github.com/eclipse-iceoryx/iceoryx2/blob/main/iceoryx2-cxx/README.md)

## Clone Repository

We will be using Iceoryx2 version 0.8.1.  We will be working detached from the live repository.

```bash
cd ~/go2-workspace
git clone https://github.com/eclipse-iceoryx/iceoryx2.git
cd iceoryx2
git checkout v0.8.1
```

## Build Instructions - C++

Assuming you are at the repository root.

First, build the C bindings generated from Rust:

```bash
cargo build --release --package iceoryx2-ffi-c
```

Then install the CMake package.

```bash
cmake -S iceoryx2-cmake-modules -B target/ff/cmake-modules/build
cmake --install target/ff/cmake-modules/build --prefix target/ff/cc/install

cmake -S iceoryx2-c -B target/ff/c/build \
      -DRUST_BUILD_ARTIFACT_PATH="$( pwd )/target/release" \
      -DCMAKE_PREFIX_PATH="$( pwd )/target/ff/cc/install"
cmake --build target/ff/c/build
cmake --install target/ff/c/build --prefix target/ff/cc/install
```

### Build and install `iceoryx2-bb-cxx`

```bash
cmake -S iceoryx2-bb/cxx -B target/ff/bb-cxx/build \
      -DCMAKE_PREFIX_PATH="$( pwd )/target/ff/cc/install"
cmake --build target/ff/bb-cxx/build
cmake --install target/ff/bb-cxx/build --prefix target/ff/cc/install
```

### Putting it together

The C++ bindings can then use the installed artifacts via
`-DCMAKE_PREFIX_PATH`. The C++ bindings can then be installed to be used by
custom projects.

```bash
cmake -S iceoryx2-cxx -B target/ff/cxx/build \
      -DCMAKE_PREFIX_PATH="$( pwd )/target/ff/cc/install"
cmake --build target/ff/cxx/build
cmake --install target/ff/cxx/build --prefix target/ff/cc/install
```


## Install Instructions - Python
**NOTE: Use the exact version for iceoryx2 as specified below:**

```bash
pip install iceoryx2==0.8.1 
```
