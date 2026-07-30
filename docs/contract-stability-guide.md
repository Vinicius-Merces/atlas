# Contract Stability Guide

## Stable meaning

A contract may gain clarification or optional capabilities without changing its
core responsibility.

## Breaking changes

Removing required behavior, changing ownership, changing required outputs, or
moving canonical paths may be breaking.

## Test both structure and semantics

Automated tests protect required files and fields. Review protects meaning.

## Extend carefully

Prefer optional extension points over duplicating or replacing stable contracts.
