### [0.2.26](https://github.com/vzhd1701/enex2notion/compare/v0.2.25...v0.2.26) (2023-05-06)

### Bug Fixes

- update dependencies to prevent 403 error ([78d9339](https://github.com/vzhd1701/enex2notion/commit/78d93398d5052c5a29125f9f5c246705ff7464da))
- update Notion SDK ([d688a95](https://github.com/vzhd1701/enex2notion/commit/d688a95e092dbe5b64214dabe79e53c3ad10c593))

### [0.2.25](https://github.com/vzhd1701/enex2notion/compare/v0.2.24...v0.2.25) (2022-12-06)

### Bug Fixes

- update notion SDK ([3e46fda](https://github.com/vzhd1701/enex2notion/commit/3e46fda66c416d720d7c3e09efb5496c70fd2bb7))

### [0.2.24](https://github.com/vzhd1701/enex2notion/compare/v0.2.23...v0.2.24) (2022-10-18)

### Bug Fixes

- improve yinxiang markdown block filtering ([497940b](https://github.com/vzhd1701/enex2notion/commit/497940b01a1a47fd2241550960ceda851eedd9af))

### [0.2.23](https://github.com/vzhd1701/enex2notion/compare/v0.2.22...v0.2.23) (2022-10-15)

### Bug Fixes

- skip Yinxiang hidden markdown appendix ([aa5989e](https://github.com/vzhd1701/enex2notion/commit/aa5989eb4b7d15da78d1460a3f394304d40072df))

### [0.2.22](https://github.com/vzhd1701/enex2notion/compare/v0.2.21...v0.2.22) (2022-10-12)

### Bug Fixes

- parse media ignoring hash case ([b1744ce](https://github.com/vzhd1701/enex2notion/commit/b1744ced7c5134efab93f56cfea195fe6fedde70)), closes [#53](https://github.com/vzhd1701/enex2notion/issues/53)

### [0.2.21](https://github.com/vzhd1701/enex2notion/compare/v0.2.20...v0.2.21) (2022-09-24)

### Bug Fixes

- add xpi to banned extensions ([a75b566](https://github.com/vzhd1701/enex2notion/commit/a75b566fd3578a06848f7e3c80bde2282a359a0b))

### [0.2.20](https://github.com/vzhd1701/enex2notion/compare/v0.2.19...v0.2.20) (2022-09-24)

### Bug Fixes

- add more banned extensions ([6a8c614](https://github.com/vzhd1701/enex2notion/commit/6a8c614c221b12dcc910af20e8138837eaea13ea))
- upload attachments with banned extensions as .bin files ([79e0be5](https://github.com/vzhd1701/enex2notion/commit/79e0be598c5c046ebe2e5b29b563cfd274977572))

### [0.2.19](https://github.com/vzhd1701/enex2notion/compare/v0.2.18...v0.2.19) (2022-09-22)

### Bug Fixes

- ignore jar file attachments ([ce066cc](https://github.com/vzhd1701/enex2notion/commit/ce066cceae72e8f27d8ed066e898680e65fb6020)), closes [#50](https://github.com/vzhd1701/enex2notion/issues/50)

### [0.2.18](https://github.com/vzhd1701/enex2notion/compare/v0.2.17...v0.2.18) (2022-08-20)

### Bug Fixes

- fix crash for notes with empty resource ([844e95c](https://github.com/vzhd1701/enex2notion/commit/844e95c14fa77bdb37bf87f3b4459adb752ed63a)), closes [#48](https://github.com/vzhd1701/enex2notion/issues/48)

### [0.2.17](https://github.com/vzhd1701/enex2notion/compare/v0.2.16...v0.2.17) (2022-07-28)

### Bug Fixes

- update notion SDK to avoid rate limit errors ([c5458da](https://github.com/vzhd1701/enex2notion/commit/c5458da992d3d74d59d7696dd060772bf82e298e))

### [0.2.16](https://github.com/vzhd1701/enex2notion/compare/v0.2.15...v0.2.16) (2022-06-19)

### Bug Fixes

- update PyMuPDF version ([88f3213](https://github.com/vzhd1701/enex2notion/commit/88f32138771e8347a3f216ae30c1fbe9a7531800))

### [0.2.15](https://github.com/vzhd1701/enex2notion/compare/v0.2.14...v0.2.15) (2022-06-14)

### Bug Fixes

- skip bad data uri images on parsing ([2b6060a](https://github.com/vzhd1701/enex2notion/commit/2b6060a52bfcdd7d2d7404ee94098aa0e251f015)), closes [#36](https://github.com/vzhd1701/enex2notion/issues/36)
- skip with an error instead of crashing when note parse failed ([e2cd4a7](https://github.com/vzhd1701/enex2notion/commit/e2cd4a755c91acdfa136fe58af33407b3b50cbcf))

### [0.2.14](https://github.com/vzhd1701/enex2notion/compare/v0.2.13...v0.2.14) (2022-06-03)

### Bug Fixes

- avoid warning when uploading tables ([d0aa9ea](https://github.com/vzhd1701/enex2notion/commit/d0aa9ead85fb1c073169b05189edaa204fce277f))
- log only warning messages from notion with --verbose flag ([9b74b15](https://github.com/vzhd1701/enex2notion/commit/9b74b159542b7b6d56987baa0d9cbb92d619c765))
- prevent network error when uploading files ([c6bacc0](https://github.com/vzhd1701/enex2notion/commit/c6bacc0a9fb5c20f096785bace02b61894f285d9))

### [0.2.13](https://github.com/vzhd1701/enex2notion/compare/v0.2.12...v0.2.13) (2022-05-25)

### Bug Fixes

- show better progress bar ([cb7699e](https://github.com/vzhd1701/enex2notion/commit/cb7699ee2da6493ff40260f1c8c2e0f847272ea1))
- show processed notes count during upload ([0546956](https://github.com/vzhd1701/enex2notion/commit/05469560063be5635cf068ae2d747845977b6a63)), closes [#33](https://github.com/vzhd1701/enex2notion/issues/33)

### [0.2.12](https://github.com/vzhd1701/enex2notion/compare/v0.2.11...v0.2.12) (2022-05-11)

### Bug Fixes

- avoid BeautifulSoup warning ([5ebb85d](https://github.com/vzhd1701/enex2notion/commit/5ebb85d3de4aa3451fd6554ad0337584975c10f1))

### [0.2.11](https://github.com/vzhd1701/enex2notion/compare/v0.2.10...v0.2.11) (2022-05-11)

### Bug Fixes

- set note update time to created time if missing ([8f3f5b1](https://github.com/vzhd1701/enex2notion/commit/8f3f5b15fba91d54748965b6168597337306ac6b))

### [0.2.10](https://github.com/vzhd1701/enex2notion/compare/v0.2.9...v0.2.10) (2022-05-10)

### Bug Fixes

- update note last edit time after upload ([d5dfa95](https://github.com/vzhd1701/enex2notion/commit/d5dfa95a8ea078f7661b764aba9a1f50e99254c7)), closes [#29](https://github.com/vzhd1701/enex2notion/issues/29)

### [0.2.9](https://github.com/vzhd1701/enex2notion/compare/v0.2.8...v0.2.9) (2022-04-11)

### Bug Fixes

- trim paragraphs when condense lines option is used ([9403e47](https://github.com/vzhd1701/enex2notion/commit/9403e470363e18719eded106ba61962e01eb6c38))

### [0.2.8](https://github.com/vzhd1701/enex2notion/compare/v0.2.7...v0.2.8) (2022-04-08)

### Features

- add option to condense lines into paragraphs (sparse) ([58b9a95](https://github.com/vzhd1701/enex2notion/commit/58b9a95f73e36f0d6fcccaf3e2419d8a0f39f62d))
- add option to set custom root page name ([2a7b2ce](https://github.com/vzhd1701/enex2notion/commit/2a7b2cee315703d1fce26a3fda77c4e213eeea60))
- add option to set custom tag for uploaded pages ([1c385e1](https://github.com/vzhd1701/enex2notion/commit/1c385e1b2a42f04a6475c44a8b9c0af3bf2a69d7)), closes [#23](https://github.com/vzhd1701/enex2notion/issues/23)

### Bug Fixes

- avoid empty blocks in malformed enex files ([33b80fa](https://github.com/vzhd1701/enex2notion/commit/33b80fa539785b56944020711eb7631240c6b044))
- rename deprecated functions to avoid warnings ([74246ef](https://github.com/vzhd1701/enex2notion/commit/74246ef453c49c6b1af0b59b75e2bab332588387)), closes [#21](https://github.com/vzhd1701/enex2notion/issues/21)

### [0.2.7](https://github.com/vzhd1701/enex2notion/compare/v0.2.6...v0.2.7) (2022-04-06)

### Features

- add option to condense lines into paragraphs ([7ce4bfe](https://github.com/vzhd1701/enex2notion/commit/7ce4bfe62f29c4b11f4ed15c46b46283f4c28155))

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
