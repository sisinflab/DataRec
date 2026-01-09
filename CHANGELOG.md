# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [1.3.0] - 2026-01-09
### Added

### Changed

### Fixed
- Documentation' assets

## [1.3.0] - 2026-01-09
### Added
- New resource class
- New source class
- A novel dataset managment
- Dataset registry
- Example datasets download and usage
- New readers and datasets structure formalism
- New dataset: CiteULike
- New writers
- Pipeline step in rawdata

### Changed
- All the old dataset classes removed
- Old readers and writers removed
- Automatic pipeline step integration

### Fixed
- Doc: fixed 'pipe' page
- pyproject.toml for pypi
- Pipeline export

## [1.2.1] - 2025-10-21
### Added
- Nothing changed

### Changed
- Nothing changed

### Fixed
- Doc: fixed 'pipe' page
- pyproject.toml for pypi


## [1.2.0] - 2025-10-25
### Added
- Ambar dataset
- Automatic doc generation (just for datasets_nav)
- Ambar test set
- Dataset config file (only on Ambar dataset)
- Automatic dataset download from config (only on Ambar dataset)
- Automatic content information download (only on Ambar dataset)
- Datasets registry (only Ambar available in this version)

### Changed
- Readme generator moved to docs/autobuild 
- Readme generator now works with different configurations


### Fixed
- SisInfLab logo in documentation now stored at docs/assets/images
- Fixed requirements. Docs requirements do not need python 3.10 anymore
- Requirements update

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

