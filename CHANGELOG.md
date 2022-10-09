## 1.5.0 (2022-10-09)

### Feat

- Added command interface
- Added standalone command to generate QR code
- Added make test command

### Fix

- Added missing fill rule

### Refactor

- Removed default padding

## 1.4.0 (2022-10-08)

### Fix

- Fill color is not needed in mask mode
- Fixed bezier curves

### Feat

- Added mask support
- Enhanced path algorithm

### Refactor

- Simplefield turn checks
- More flexible way to parse parameters
- Don't use shortcut to build qr instance
- Using constant instead of hardcoded value

## 1.3.1 (2022-10-07)

### Fix

- Set fill mode for path
- Removed useless attribute

### Feat

- Testing round corners

## 1.3.0 (2022-10-02)

### Feat

- Added invert color support
- Allow change x/y coordinates using parameters in RML

## 1.2.2 (2022-10-02)

### Fix

- Updated image links

## 1.2.1 (2022-10-02)

## 1.2.0 (2022-10-02)

### Refactor

- Renamed project

## 1.1.0 (2022-09-25)

### Feat

- Added python API

### Fix

- Argument start of array.index is availablo only from python 3.10
- Changed example page size to standard A4

### Refactor

- Instad of consume segment use high level get_segments

## 1.0.1 (2022-09-18)

## 1.0.0 (2022-09-18)

### Refactor

- Place shapes using transform
- Removed unused code

## 0.2.1 (2022-09-17)

### Fix

- Removed unused branches

## 0.2.0 (2022-09-17)

### Fix

- Close line after each segment

### Feat

- Render QR code using large paths

## 0.1.1 (2022-09-04)

### Fix

- Added missing setuptools_scm

## 0.1.0 (2022-09-04)

### Fix

- Replaced wrong badge syntax
- Removed not working configurations
- Removed unused poetry
- RML is not detected, removing from pre-commit

### Feat

- Added CI configuration
- Added pylint configuration
- Added tests
- Added commitizen
- Added setuptools support
- Added pre-commit hook
