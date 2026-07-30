# Runtime Adapter Guide

## Keep canonical definitions canonical

Runtime adapters should reference or transform canonical ATLAS assets rather
than forking their meaning.

## Document capability gaps

Different runtimes expose different tools, memory behavior, invocation models,
and file conventions. Unsupported behavior must be explicit.

## Test semantic parity

A valid adapter should produce equivalent task classification, ownership,
workflow sequencing, review expectations, and delivery evidence.

## Version compatibility

Adapters should declare both their own version and the compatible ATLAS
framework versions.
