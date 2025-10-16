# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [x.x.x] - yy-mm-dd
### Added
- Nothing major


### Changed
- Nothing major


### Fixed
- Nothing major

---

## [1.1.0] - 2025-10-16
### Added
- CHANGELOG.md file.
- docs folder in the main branch.
- requirements files for virtual environment setup.
- pyproject.toml file for package management.
- docs/assets/images folder for documentation images.
- LICENSE file.

### Changed
- README.md file including the datarec logo
- Removed setup.py file in favor of pyproject.toml

### Fixed
- Nothing major

---

## [1.0.4] - 2025-09-20
### Added
- Structured documentation 
- Documentation hosting with GitHub Pages

### Changed
- Nothing major

### Fixed
- Adjusting files for RecSys 2025 tutorial "[Standard Practices for Data Processing and Multimodal Feature Extraction in Recommendation with DataRec and Ducho (D&D4Rec]"(https://sites.google.com/view/dd4rec-tutorial/home) 

---

## [1.0.3] - 2025-06-12
### Added
- Introduced new `DataRecBuilder` paradigm for dataset preparation and loading.
- Added `torch_dataloader` integration.
- New datasets and documentation files.

### Changed
- Refactored caching mechanism for improved speed and modularity.
- Updated documentation and examples.

### Fixed
- Bug in `prepare_and_load()` method when caching partial data.
- Minor typo in `AmazonBeauty2023` dataset metadata.

---

## [1.0.1] - 2025-06-01
### Added
- New datasets versions and documentation files.

### Changed
- Refactored caching mechanism for improved speed and modularity.
- Updated documentation and examples.

### Fixed
- Fixing datasets bugs

---

## [1.0.0] - 2025-02-10
### Added
- Initial public release of DataRec.
- Support for dataset builders, preprocessing, and standard pipeline.
- Integration with common datasets (MovieLens, Amazon Beauty, etc.).

