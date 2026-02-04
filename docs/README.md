---
audience: user
---

# Documentation Index

Welcome to the NFL Head Coach '09 CSV Editor documentation. This index helps you find the right documentation for your needs.

## Quick Links

- **New users:** Start with [Installation](user/getting-started/installation.md) → [Quick Start](user/getting-started/quickstart.md)
- **Experienced users:** Jump to [Usage Guide](user/guides/usage.md) for operation details
- **Troubleshooting:** See [Common Issues](user/guides/troubleshooting.md) for problem resolution
- **Advanced editing:** Reference [CSV Fields](user/reference/csv-fields.md) for custom operations

## Documentation Structure

This documentation is organized by audience:

```
docs/
├── user/           # User-facing documentation (you are here)
├── ops/            # Operational documentation (deployment, maintenance)
└── internal/       # Internal development documentation
```

## User Documentation

### Getting Started

New to the tool? Start here:

| Document | Purpose | Time |
|----------|---------|------|
| [Installation](user/getting-started/installation.md) | Install and verify the tool | 5 min |
| [Quick Start](user/getting-started/quickstart.md) | Your first editing session | 10 min |

### Guides

Task-oriented guides for accomplishing specific goals:

| Document | Purpose |
|----------|---------|
| [Usage Guide](user/guides/usage.md) | Complete operation reference for all roster types |
| [Troubleshooting](user/guides/troubleshooting.md) | Solutions to common problems |

### Reference

Comprehensive reference documentation:

| Document | Purpose |
|----------|---------|
| [CSV Fields Reference](user/reference/csv-fields.md) | Complete field codes and safe value ranges |

### Concepts

Understanding how the tool works:

*No concept docs yet. Check back for architecture and design explanations.*

### Examples

Practical examples and use cases:

*No examples yet. Check back for common scenario walkthroughs.*

## Path by Experience Level

### Beginner

1. **Install the tool:** [Installation Guide](user/getting-started/installation.md)
2. **Learn the basics:** [Quick Start Guide](user/getting-started/quickstart.md)
3. **Try standard operations:** Use menu options 1-3 in [Quick Start](user/getting-started/quickstart.md#step-4-make-your-first-edit)
4. **Explore all operations:** Review [Player Operations](user/guides/usage.md#player-operations) in Usage Guide

### Intermediate

1. **Master bulk operations:** See [Bulk vs Individual Editing](user/guides/usage.md#bulk-vs-individual-editing)
2. **Learn all roster types:** Review [Coach](user/guides/usage.md#coach-operations), [GM](user/guides/usage.md#gm-operations), [Trainer](user/guides/usage.md#trainer-operations) operations
3. **Apply advanced techniques:** Try [Creating Custom Draft Classes](user/guides/usage.md#creating-custom-draft-classes)

### Advanced

1. **Custom field editing:** Study [CSV Fields Reference](user/reference/csv-fields.md)
2. **Use "Change Key Value":** See [Change Key Value operation](user/guides/usage.md#7-change-key-value)
3. **Multi-file workflows:** Learn [Multi-File Workflows](user/guides/usage.md#multi-file-workflows)
4. **Contribute:** Read [CLAUDE.md](../CLAUDE.md) development conventions

## Path by Task

### I want to...

**...boost my favorite team's potential**
→ [Bulk Operations](user/guides/usage.md#bulk-vs-individual-editing) → Option 3 → Maximize Potential

**...fix injured players**
→ [Maximize Health operation](user/guides/usage.md#2-maximize-health)

**...manage salary cap**
→ [Resign for Peanuts operation](user/guides/usage.md#3-resign-for-peanuts)

**...create superstar rookies**
→ [Creating Custom Draft Classes](user/guides/usage.md#creating-custom-draft-classes)

**...randomize names**
→ [Name Randomization](user/guides/usage.md#name-randomization-uses)

**...edit a specific stat**
→ [Change Key Value](user/guides/usage.md#7-change-key-value) + [CSV Fields Reference](user/reference/csv-fields.md)

**...understand errors**
→ [Troubleshooting Guide](user/guides/troubleshooting.md)

**...contribute code**
→ [CLAUDE.md](../CLAUDE.md) (development conventions)

## Operations Documentation

Not covered here. This is a single-file tool with minimal operational complexity.

*If deployment/automation is needed, see `docs/ops/` (currently empty).*

## Internal Documentation

Developer documentation is in `docs/internal/`:

- **Architecture:** System design documents
- **Plans:** Implementation plans and roadmaps
- **Audit:** Code quality and security audits
- **History:** Archived artifacts and completed work

**For contributors:** Start with [CLAUDE.md](../CLAUDE.md) for coding standards and project structure.

## Document Conventions

All documentation follows these standards:

### Frontmatter

Each document has YAML frontmatter indicating audience:

```yaml
---
audience: user | ops | internal
---
```

- **user:** End users of the CSV editor
- **ops:** Operations teams (deployment, maintenance)
- **internal:** Contributors and developers

### Folder Inheritance

Documents inherit audience from their folder:
- `docs/user/**` → audience: user
- `docs/ops/**` → audience: ops
- `docs/internal/**` → audience: internal

### Navigation

Use relative links to navigate between docs:
- Same folder: `[link](filename.md)`
- Parent folder: `[link](../filename.md)`
- Sibling folder: `[link](../sibling/filename.md)`

## Contributing to Documentation

When adding or updating documentation:

1. **Place in correct folder:**
   - User-facing → `docs/user/`
   - Operational → `docs/ops/`
   - Internal → `docs/internal/`

2. **Add frontmatter:** Include `audience` field if overriding folder default

3. **Update this index:** Add entry to relevant section above

4. **Follow conventions:** See [LLM Native Markdown Style Guide](../.claude/shared/concepts/LLM_Native_Markdown_Style_Guide.md) for formatting

5. **Cross-link:** Reference related documents for navigation

## Additional Resources

- **Project README:** [README.md](../README.md) - Project overview and features
- **Development Guide:** [CLAUDE.md](../CLAUDE.md) - Coding conventions and architecture
- **Research Library:** `research/` - Technical patterns and best practices
- **GitHub Repository:** [hc09-db-csv-editor](https://github.com/Cyonx818/hc09-db-csv-editor)

## Need Help?

1. **Search this index** for relevant documentation
2. **Check troubleshooting** for common issues
3. **Review examples** for similar use cases
4. **Create GitHub issue** if problem persists

---

**Last Updated:** 2026-02-04

This documentation index is maintained to help you find the right information quickly. If you notice missing or outdated information, please open an issue or submit a pull request.
