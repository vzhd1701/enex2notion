### [0.2.6](https://github.com/vzhd1701/enex2notion/compare/v0.2.5...v0.2.6) (2022-04-04)

### Bug Fixes

- filter out unsupported file extensions for upload ([e6e6fba](https://github.com/vzhd1701/enex2notion/commit/e6e6fba7815ab7de727ffd2a3feec8d5ba00ef33))
- get rid of recursion when splitting blocks for weblcips ([b5e8b19](https://github.com/vzhd1701/enex2notion/commit/b5e8b190f251187f341dced6c020536dc10fe3c8)), closes [#17](https://github.com/vzhd1701/enex2notion/issues/17)
- handle bad token error ([437208f](https://github.com/vzhd1701/enex2notion/commit/437208f136d9b46a1c347fe4adb833db63198468))
- skip root page search for empty accounts ([807b04c](https://github.com/vzhd1701/enex2notion/commit/807b04caa464abfef3e6745870c4f48682c5a658))

### [0.2.5](https://github.com/vzhd1701/enex2notion/compare/v0.2.4...v0.2.5) (2022-01-12)

### Features

- add option to include previews for PDF weblcips ([458e3be](https://github.com/vzhd1701/enex2notion/commit/458e3beb42512146720177b191d3013f06147a4b))

### Bug Fixes

- handle special css colors ([8fbc393](https://github.com/vzhd1701/enex2notion/commit/8fbc39381bd44a207e977a8767353935e0d8e266))
- prevent resources from having empty extensions ([9a30823](https://github.com/vzhd1701/enex2notion/commit/9a308233b2b686880b1e82b5cbe244fd6db6c016))
- retry on server side errors during upload ([2891a57](https://github.com/vzhd1701/enex2notion/commit/2891a57d975f97729089d042e9f25f6f7e45ba8a))

### [0.2.4](https://github.com/vzhd1701/enex2notion/compare/v0.2.3...v0.2.4) (2022-01-04)

### Bug Fixes

- add missing dataclasses dependency for python 3.6 ([601b1d2](https://github.com/vzhd1701/enex2notion/commit/601b1d2793004fa9fdfbb8ed23ece0f72ca76ee0))
- convert inline newline tags in paragraphs ([b6cb781](https://github.com/vzhd1701/enex2notion/commit/b6cb78102ad6fca424c1c867a0c070d477971b2d))
- prevent error when parsing empty tables ([2397971](https://github.com/vzhd1701/enex2notion/commit/239797196b84b71c19ea511ee52acf8e899d8d52))
- split paragraphs before parsing line by line ([b692136](https://github.com/vzhd1701/enex2notion/commit/b692136b36cbb2aa4eabefa4281ec947a649464a))

### [0.2.3](https://github.com/vzhd1701/enex2notion/compare/v0.2.2...v0.2.3) (2021-12-25)

### Features

- add option to log output into file ([f50bb58](https://github.com/vzhd1701/enex2notion/commit/f50bb5899fe2f697a95f2c378a11e4f7cc93c673))

### Bug Fixes

- log note title on exception ([95d7796](https://github.com/vzhd1701/enex2notion/commit/95d77967bf46b956d6a69e4503a81b5d515e1a93))

### [0.2.2](https://github.com/vzhd1701/enex2notion/compare/v0.2.1...v0.2.2) (2021-12-25)

### Bug Fixes

- fix crash on parsing nested spaces in webclips ([0c389ed](https://github.com/vzhd1701/enex2notion/commit/0c389edead0510c5ea87f0165e20d06b9555382a))

### [0.2.1](https://github.com/vzhd1701/enex2notion/compare/v0.2.0...v0.2.1) (2021-12-21)

### Bug Fixes

- parse images as children elements in lists ([c214bd4](https://github.com/vzhd1701/enex2notion/commit/c214bd43ea83ff700286be5068b8700c1fcf486e))
- remove original size parsing for images to avoid oversized image blocks ([e72752e](https://github.com/vzhd1701/enex2notion/commit/e72752eab99200e7282c116291c0e2a6ea58a38f))
- revert back to html.parser, html5lib can't parse ENML properly ([441cc74](https://github.com/vzhd1701/enex2notion/commit/441cc74814b2856bfd52270d02ba530462987975))

## [0.2.0](https://github.com/vzhd1701/enex2notion/compare/v0.1.8...v0.2.0) (2021-12-20)

### Features

- add support for webclips ([6370bac](https://github.com/vzhd1701/enex2notion/commit/6370bace153c129f50c682e9701b19c373694aef))

### Bug Fixes

- cleanup empty databases before creating new one ([fc594f1](https://github.com/vzhd1701/enex2notion/commit/fc594f18e8d9b5975bf1f88e52f4748ae7132dfc))
- fix webclip detection ([bb64e3c](https://github.com/vzhd1701/enex2notion/commit/bb64e3c8ff6ae0c99a0cc75d3ab5a1904f6ffd11))
- move some harmless warnings into debug log ([ec53bad](https://github.com/vzhd1701/enex2notion/commit/ec53bad586f60968bb7b120fa0188ec07e70cd32))
- set fixed size for sizeless SVG images ([b94419f](https://github.com/vzhd1701/enex2notion/commit/b94419ffe8e8abadd091dd922405345b165024c3))

### [0.1.8](https://github.com/vzhd1701/enex2notion/compare/v0.1.7...v0.1.8) (2021-12-14)

### Bug Fixes

- handle embedded lists at the start of other lists ([f3b83ac](https://github.com/vzhd1701/enex2notion/commit/f3b83ace963ede55a40e520bcbc0138624e67ce9))

### [0.1.7](https://github.com/vzhd1701/enex2notion/compare/v0.1.6...v0.1.7) (2021-12-13)

### Bug Fixes

- add proper parsing for missing note attributes ([562ddc6](https://github.com/vzhd1701/enex2notion/commit/562ddc640f559f53b8c4d2e004d41ae7bfe8c852))

### [0.1.6](https://github.com/vzhd1701/enex2notion/compare/v0.1.5...v0.1.6) (2021-12-07)

### Bug Fixes

- add todo parsing for paragraphs ([f3e9871](https://github.com/vzhd1701/enex2notion/commit/f3e987148c2e5dbd091eecc87e2252dfe46be64f))

### [0.1.5](https://github.com/vzhd1701/enex2notion/compare/v0.1.4...v0.1.5) (2021-12-06)

### Bug Fixes

- parse unexpected elements in lists as text ([952feb2](https://github.com/vzhd1701/enex2notion/commit/952feb2b6905ecd65e0c2ba491bef16cd2f24ea9))
- skip webclip notes before parsing ([9af7912](https://github.com/vzhd1701/enex2notion/commit/9af79120707d17a6410085305b54c8ea97a8ede9))

### [0.1.4](https://github.com/vzhd1701/enex2notion/compare/v0.1.3...v0.1.4) (2021-12-06)

### Bug Fixes

- prevent crash for notes with empty resource ([157ace7](https://github.com/vzhd1701/enex2notion/commit/157ace73934a780b6a4a88411178d6e49ccb7173))

### [0.1.3](https://github.com/vzhd1701/enex2notion/compare/v0.1.2...v0.1.3) (2021-12-05)

### Bug Fixes

- add % escaping to prevent progress bar crash ([9c24c94](https://github.com/vzhd1701/enex2notion/commit/9c24c94eaaba43a3c0d38bbd5d2244a7b496c83b))

### [0.1.2](https://github.com/vzhd1701/enex2notion/compare/v0.1.1...v0.1.2) (2021-12-05)

### Bug Fixes

- add proper css style parsing for colors ([ffbbd69](https://github.com/vzhd1701/enex2notion/commit/ffbbd69a9f532fad5a35821375a3a4e3d5923f5a))

### [0.1.1](https://github.com/vzhd1701/enex2notion/compare/v0.1.0...v0.1.1) (2021-12-03)

### Bug Fixes

- add proper data uri parsing ([1532e8a](https://github.com/vzhd1701/enex2notion/commit/1532e8abb8f4985baac1a7a7867b8b7720465c6c))
- avoid wrong css when parsing color ([62e339d](https://github.com/vzhd1701/enex2notion/commit/62e339d0a41f9f85462c5fb25f7b15f145d2922e))
- skip webclips embedded content ([c8f45b4](https://github.com/vzhd1701/enex2notion/commit/c8f45b4a9ae6f1b4dbb5e9c4d41f137a7da78cc0))

## 0.1.0 (2021-11-30)
