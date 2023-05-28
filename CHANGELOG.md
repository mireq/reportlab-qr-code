## 1.7.0 (2023-05-28)

### Feat

- Small optimalization - don't do masking if we need draw all
- Allow draw command with = sign
- Implemented partial draw for command line
- Allow hightight align patterns
- Added alignment pattern calculation
- Added QR parts masking support
- Added drawing stack
- Parsing draw parts

### Fix

- Correctly combine graadients in commandline mode
- Replaced fixed drawing fragment
- Correct hole position
- Don't throw exception without hole parameter
- Consistent area naming
- Partial draw fixes
- Don't parse global and part params exactly same

### Refactor

- Reorganized conditions
- Removing old commented code
- Moved color parsing

## 1.6.1 (2023-05-27)

### Feat

- Allow --hole commandline parameter
- Implemented hole support
- Implemented area to pixels conversion
- Added area parsing

### Fix

- Fixed tests
- Typo
- Dont allow mixed units in area definition

### Refactor

- Canged Length to dataclass

## 1.6.0 (2022-10-23)

### Fix

- Don't open file if arguments are not successfully parsed

### Feat

- Added negative command line argument
- Added alpha channel support
- Added negative image support

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
