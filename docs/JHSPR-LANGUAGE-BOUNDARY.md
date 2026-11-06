# JHSPR (Jasper) — polyglot language boundary

> **Architectural intent, not a verified runtime.** This document records how JHSPR is intended to relate to the connected Design Orchard LLC system. It does not claim that a parser, language loader, interpreter, conformance suite, or cross-language execution path has been implemented.

**Recorded:** 2026-11-06  
**Context:** Design Orchard LLC / 🔬 DrMarchand’s Lab⚛︎ratory™  
**Audience:** Public, release-safe engineering documentation  
**Implementation status:** Source and runtime evidence pending

## Responsibility boundaries

| Component | Intended responsibility | Does not establish |
| --- | --- | --- |
| **JHSPR** (pronounced *Jasper*) | Polyglot programming-language layer; load participating language(s) and make their capabilities available in a connected architecture | That each language, adapter, parser, or execution backend already exists |
| **MURI** (Marchand Universal Runtime Interface) | Present code and provide a way to inspect and interact with it | Language loading, independent data authority, or execution permission |
| **DOLSA** | Define applicable language, package, interface, and governance contracts | That implementations conform or that a run is authorized |
| **DrMarchand’s ⚙︎ Nɛuro-Forge Engine** | Validate and orchestrate permitted operations within delegated authority | Ownership of language definitions or self-granted execution authority |
| **External Bridges** | Connect source and target systems through explicit contracts | Membership inside the Engine or automatic transfer of authority |

A programming language, its implementation, the runtime executing it, the interface showing it, the data source, and the permission to operate are **different objects**. They must be identified and verified independently.

Python, Ruby, and PHP have been discussed as possible data retrieval and processing participants; SQLite has been discussed as a storage/query component. These are **architectural examples**, not a verified JHSPR compatibility matrix or list of implemented adapters.

## Relationship, not an automatic execution pipeline

1. An authorized human establishes the permitted operation and scope under Design Orchard LLC.
2. Source evidence establishes which language definitions, implementations, and dependencies actually exist.
3. JHSPR's proposed language-loading role is evaluated independently of MURI's presentation role.
4. DOLSA contracts describe expected interfaces and conformance; tests are needed to show actual compliance.
5. DrMarchand’s ⚙︎ Nɛuro-Forge Engine may execute or orchestrate only within delegated permission.
6. Execution evidence, failures, receipts, and decisions are retained with provenance; accepted permanent records belong in 📚 DrMarchand’s ⚛︎ Library™ and require an authorized-human validation gate.

This is a **responsibility model**. It is not proof that these steps are wired together or have run successfully.

## Evidence available in this repository

- [Engine/core.py](../Engine/core.py) contains Python receipt/ledger synthesis logic. Its existence does **not** demonstrate JHSPR parsing, DOLSA conformance, or a cross-language execution handshake.
- The [Engine README](../README.md) documents the bounded execution role. It is not an implementation receipt for JHSPR.
- No authoritative JHSPR or DOLSA source revision has been reconciled with this document. The absence of a repository from a particular connected GitHub account is **not** evidence that the repository does not exist.

## Evidence required before implementation or promotion claims

- Identify the owning JHSPR and DOLSA repository coordinates, branches, commit SHAs, audience, and publication scope.
- Map real language definitions, loaders, parsers, adapters, entry points, and their provenance without inventing helpers.
- Specify the JHSPR–DOLSA and JHSPR–Engine contracts, including error, failure, and unauthorized-operation behavior.
- Verify positive and negative conformance tests without bypassing execution boundaries; do not treat a JSON handshake prototype as proof of language execution.
- Tie any tested runtime behavior to an exact source revision, environment, receipt, and permanent custody record.
- Obtain authorized-human review before claiming integration, runtime readiness, or public release.

**Disposition:** JHSPR's intended role is documented here. Implementation, compatibility, conformance, and deployment are **not verified** by this documentation change.
