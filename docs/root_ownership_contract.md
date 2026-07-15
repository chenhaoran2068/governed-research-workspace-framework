# Root Ownership Contract

## Purpose

A compatible workspace separates ownership from system capability. Root names
are a contract for where a class of material belongs; they are not permission
grants and are not required to contain every possible system module.

## Recommended Roots

| Root | Owns | Does not own by default |
| --- | --- | --- |
| `Systems/` | System control planes, runtime contracts, system-local templates, validators, and tests. | Real project authority, general shared libraries, or raw data holdings. |
| `Skills/` | Reusable skill packages and registry records. | Project outputs, installed runtime caches, or duplicated system content. |
| `Shared/` | Cross-project rules, approved shared references, stable memory, promotion queues, and shared utilities. | Active project state, final conclusions, or project release decisions. |
| `Knowledge/` | Source-backed knowledge records, provenance, curation, and bounded retrieval surfaces. | General memory, unbounded source dumping, or project-specific interpretation. |
| `Methods/` | Method workbenches, reusable pipelines, and method validation. | Lifecycle ownership for every project using a method. |
| `Instances/` | Real project and program workspaces. | Cross-project authority or public release source. |
| `Papers/` | Cross-project paper rules and retained special paper workspaces. | Default new-project execution space. |
| `Data_Raw/` | Retained source-data holdings. | Analysis-ready project data, result authority, or public-release approval. |
| `Github/` | Local worktrees for public repositories and release surfaces. | Private workspace authority. |
| `Ops/` | Caches, temporary operations, and machine support. | Durable research knowledge or project authority. |
| `Archive/` | Retained historical material. | Current authority unless explicitly designated. |

## Placement Rules

1. Every artifact has one owner root, even when multiple systems use it.
2. A shared pointer is preferred to copying a reusable object into multiple
   system trees.
3. A real project keeps its facts, data, analysis, results, manuscript, and
   audit in its own instance workspace.
4. A public worktree may contain a reviewed derivative, but cannot replace the
   private source of truth.
5. A root-role contract does not authorize access to material stored there.

The [reference workspace tree](reference_workspace_tree.md) defines the
cross-system second-level placement points. Concrete systems and projects own
all deeper domain-specific layout.
