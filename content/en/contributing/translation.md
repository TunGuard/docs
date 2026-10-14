---
title: Translation
---

The documentation is available in several languages. Each language is built as
its own site and published under its own path:

| Language | Code | Path        | Content            | Config              |
| -------- | ---- | ----------- | ------------------ | ------------------- |
| English  | `en` | `/docs/`    | `content/en/`      | `zensical.toml`     |
| French   | `fr` | `/docs/fr/` | `content/fr/`      | `zensical.fr.toml`  |
| Spanish  | `es` | `/docs/es/` | `content/es/`      | `zensical.es.toml`  |

A language selector in the header links the languages together. It is
configured with the `alternate` list under `[project.extra]` in every config
file, so English is served from the site root and every other language from a
subdirectory named after its language code.

## Translate an existing language

Edit the Markdown files under `content/<code>/`. The directory mirrors
`content/en/` one to one, so a translated page keeps the same path as its
English counterpart.

New languages start as untranslated copies of English. Translate file by file;
a partially translated language is fine, and untranslated pages simply keep
their English text until someone gets to them.

/// note | Keep files in sync
When a page is added or renamed in `content/en/`, mirror the change in the
other language directories so the navigation stays the same everywhere.
///

## Add a new language

1. Copy the English content and translate it:

   ```sh
   cp -r content/en content/<code>
   ```

2. Copy an existing language config and adjust it:

   ```sh
   cp zensical.fr.toml zensical.<code>.toml
   ```

   In the new file, set `docs_dir = "content/<code>/"`, `site_dir =
   "site-<code>"`, `edit_uri = "edit/main/content/<code>"`, `site_url =
   "https://tunguard.github.io/docs/<code>"`, and `language = "<code>"`.

3. Add the language to the `alternate` list in **every** config file, for
   example in `zensical.toml`, `zensical.fr.toml` and `zensical.es.toml`:

   ```toml
   { name = "Deutsch", link = "/docs/de/", lang = "de" },
   ```

4. Add the code to `LANGUAGES` in `scripts/sync_changelog.py` so the changelog
   is generated for the new language as well.

5. Add build and merge steps for the language to
   `.github/workflows/deploy.yml`, next to the existing `fr` and `es` steps.

The `language` value must be a language code that Zensical ships translations
for. See the [list of supported languages][zensical-languages] for the full set
(English is always used as the fallback).

## Contribute changes

See [Pull Requests](./issues-and-pull-requests.md#pull-requests) on how to
contribute your translation.

[zensical-languages]: https://zensical.org/docs/setup/language/
