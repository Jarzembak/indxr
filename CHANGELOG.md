# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-25

### Added

- Per-book color coding across all generated PDFs. Each book is assigned a
  distinct, readable color from a curated default palette: per-book PDFs get a
  themed header and a left color bar, the master index shows a color swatch for
  each entry, the compact index prefixes every `B#:P#` reference with a colored
  swatch, and the master/compact title pages include a "Book Color Key" legend.
- `book_colors` option in `indxr.toml` to override the color of specific books.
- Single-source project version: `pyproject.toml` reads the version dynamically
  from `indxr/__init__.py`, and `indxr --version` reports it.

### Changed

- Default Book 5 color changed from orange to yellow so it no longer looks too
  similar to Book 1's red.
- Enlarged the per-book swatches before each `B#:P#` reference in the compact
  index (~2.5x) for better visibility.

### Fixed

- Corrected the hatchling wheel build-target table name in `pyproject.toml`
  (`[tool.hatchling.build.targets.wheel]` → `[tool.hatch.build.targets.wheel]`),
  which was previously ignored.

## [0.1.0] - Initial release

### Added

- Per-book content PDFs, a master alphabetical index, and a compact two-column
  index generated from markdown index files.
- Configurable input/output paths, parsing patterns, and titles via CLI flags
  and an optional `indxr.toml` config file.

[0.2.0]: https://github.com/Jarzembak/indxr/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Jarzembak/indxr/releases/tag/v0.1.0
