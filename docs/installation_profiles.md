# Installation Profiles

## Standalone

A concrete system can operate from its own package root using only bundled
public resources and user-provided project inputs.

Requirements:

- no dependency on a named private workspace;
- no assumption about a drive or absolute path;
- no silent search for shared services;
- clear stop behavior when an optional capability is unavailable; and
- documented host/runtime requirements.

## Framework Integrated

A concrete system is installed into a compatible workspace and reads the
workspace manifest plus its own system manifest.

Requirements:

- declare the supported framework version;
- register a workspace-relative system path;
- declare every required and optional shared service;
- document intended project-root behavior;
- use only explicitly configured paths; and
- retain standalone-equivalent safety boundaries when an optional service is
  missing.

## Private Lab Extended

A private organization may add internal rules, source libraries, connectors,
or runtime integrations. These are outside this public framework's release
claim and must not be assumed by a public system package.
