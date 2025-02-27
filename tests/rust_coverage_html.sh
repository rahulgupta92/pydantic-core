#!/usr/bin/env bash

rust-profdata merge -sparse default.profraw -o default.profdata
rust-cov show -Xdemangler=rustfilt $(ls pydantic_core/*.so) \
    -instr-profile=default.profdata \
    --ignore-filename-regex='/.cargo/registry' \
    --ignore-filename-regex='library/std' \
    -format=html -o htmlcov/rust

rm default.profraw default.profdata
