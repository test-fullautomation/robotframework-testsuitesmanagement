# Cheat sheet

The complete JSONP syntax on one page. Click on a feature to get the details.

## Basics

| Feature | Syntax | Result |
|---|---|---|
| [Line comment](comments.md) | `// comment` | ignored |
| [Block / inline comment](comments.md#block-comments-and-inline-comments) | `/* comment */` | ignored |
| [Boolean, null](boolean-null.md) | `true`, `True`, `false`, `False`, `null`, `None` | `True`, `False`, `None` |
| [Byte sequence](byte-sequences.md) | `b'\x41\x42'` | `b'AB'` |

## Imports

| Feature | Syntax |
|---|---|
| [Import a file](imports.md) | `"[import]" : "./common.jsonp"` |
| [Import into a subkey](imports.md#multiple-imports-of-the-same-file) | `"sub" : { "[import]" : "./common.jsonp" }` |
| [Dynamic import path](imports.md#dynamic-import-paths) | `"[import]" : "${config_dir}/common.jsonp"` |
| [Computed import path](python-inline-code.md#further-examples) | `"[import]" : <<${path_1} if True else ${path_2}>>` |
| [Optional import](imports.md#optional-imports) | `"[import?]" : "./local_overrides.jsonp"` |
| [Conditional import](imports.md#conditional-imports) | `"[import]" : {"file" : "./debug.jsonp", "if" : ${use_debug}, "else" : "./release.jsonp"}` |
| [Optional import object](imports.md#conditional-imports) | `"[import]" : {"file" : "./local.jsonp", "optional" : true}` |

## Read values (right-hand side of the colon)

| Feature | Syntax | Data type of result |
|---|---|---|
| [Parameter](overwriting-parameters.md#access-existing-parameters) | `"b" : ${a}` | type of `a` |
| [Parameter as string](overwriting-parameters.md#with-or-without-quotes) | `"b" : "${a}"` | `str` |
| [Composite string](overwriting-parameters.md#composite-strings) | `"b" : "prefix_${a}_suffix"` | `str` (simple types only) |
| [List element](overwriting-parameters.md#access-a-single-element) | `${list}[0]` | type of element |
| [Dictionary key](overwriting-parameters.md#access-a-single-element) | `${dict}['key']` | type of value |
| [dotdict notation](dotdict-notation.md) | `${dict.key.sub_key}`, `${list.0}` | type of value |
| [Index as parameter](overwriting-parameters.md#dictionary-keys-and-indices-as-parameter) | `${list}[${index}]`, `${dict}[${key}]` | type of value |
| [Python inline code](python-inline-code.md) | `"c" : <<${a} + ${b}>>` | type of expression |

## Write values (left-hand side of the colon, never in quotes)

| Feature | Syntax |
|---|---|
| [Overwrite a parameter](overwriting-parameters.md#overwrite-a-value-defined-in-an-imported-file) | `"a" : 2` or `${a} : 2` |
| [Overwrite a list element](overwriting-parameters.md#overwrite-a-single-element) | `${list}[0] : "new"` |
| [Overwrite / add a dictionary key](overwriting-parameters.md#add-an-element) | `${dict}['key'] : "new"` |
| [Dynamic key name](dynamic-key-names.md) (existing keys only) | `${dict}['${prefix}_2'] : 2` |
| [Implicit creation](implicit-creation.md) (hard coded names only) | `${a.b.c} : 1` or `${a}['b']['c'] : 1` |

## Square brackets

| Expression | Meaning |
|---|---|
| `[1]`, `[${intparam}]` | list index (integer) |
| `['keyname']`, `[${stringparam}]`, `['${stringparam}']` | dictionary key (string) |
| `['${intparam}']` | integer parameter converted to a dictionary key (string) |

## Not allowed

| What | Why / alternative |
|---|---|
| `{"${name}_2" : 1}` | dollar operator in key names of a definition, see [Dynamic key names](dynamic-key-names.md) |
| `"${a}" : 1` | left-hand side expressions must not be quoted |
| `"x ${list} y"` | lists and dictionaries cannot be substituted inside strings |
| `${list}[5] : 1` (index out of range) | lists cannot be extended - overwrite the entire list |
| `"x <<1+1>> y"`, `[<<1+1>>]`, `<<...>> : 1` | Python inline code only as complete value |
| `"[" : 1` | brackets `[ ] { } < >` must not be used within key names |
| `b"..."` | byte sequences require single quotes |
| `${dict.sub.key}` with key `sub.key` | dots in key names require the standard notation `${dict}['sub.key']` |
