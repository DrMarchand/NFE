# Internal Runtime Working Repository

> Public source and working records retained under the repository identifier `DrMarchand/NFE`.

**Legal and operating company:** Design Orchard LLC  
**Repository status:** Working source; no production-runtime claim  
**Public naming status:** Internal execution-system name unresolved

## Naming containment

`NFE` is a legacy compatibility identifier used by this repository and by existing commands, database objects, schemas, paths, logs, or source files. It is not presented here as a public product or brand name.

As of August 26, 2026, public use of the former expanded engine wording is paused after preliminary screening identified a live federal conflict. Existing machine identifiers and historical records remain unchanged to preserve compatibility and provenance.

Do not silently rename:

- the repository;
- database or schema identifiers;
- command names;
- environment variables;
- API routes;
- source symbols;
- file or directory paths;
- quoted historical evidence.

Label those strings as compatibility identifiers when they appear in documentation.

## Repository map

| Surface | Purpose | Boundary |
|---|---|---|
| [`Engine/`](Engine/) | Working Python modules | Source presence is not deployment evidence |
| [`core/`](core/) | Runtime samples, notes, and compatibility files | May contain legacy identifiers |
| [`runtime/`](runtime/) | Working runtime utilities and state samples | Requires environment-specific validation |
| [`DrMarchandsLaboratory.com/`](DrMarchandsLaboratory.com/) | Laboratory working files | See the nested README |
| [`archive/`](archive/) | Historical or packaged material | Preserve as provenance; do not promote as current naming |

## Runtime boundary

The checked-in code may demonstrate implementation details at a specific revision. It does not by itself establish a deployed, reachable, healthy, authorized, or production-ready service.

Public configuration samples must contain no credentials, private hostnames, personal paths, or secret locations. Use private configuration or an approved secret-management system for runtime values.

## Validation

No repository-wide dependency manifest or automated test command is present at the root. Validate individual modules in an isolated environment before execution. Do not run repository code merely to infer architecture or trademark status.

## Authority and rights

Design Orchard LLC is the legal and operating company. Authorship, copyright ownership, publisher status, and license scope are work-specific. See [`RIGHTS.md`](RIGHTS.md) and applicable nested notices.

