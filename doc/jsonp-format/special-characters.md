# Special characters within key names

Basically, the JsonPreprocessor follows the JSON naming convention for key names: within JSONP files allowed is what
JSON allows - with one limitation:

The JSONP format uses square, curly and angle brackets as syntax elements: `[`, `]`, `{`, `}`, `<`, `>`.

!!! danger "These brackets must not be used within key names!"

This JSONP code:

```json
{
    "[" : 1,
    "B" : ${[}
}
```

causes an error, because the brackets inside the dollar operator expression cannot be interpreted.

## Other special characters

All other special characters can be used:

```json
{
    "$" : 1,
    "B" : ${$}
}
```

**Result:**

```python
DotDict({'$': 1, 'B': 1})
```

## Backslashes

Strings are handled as raw strings. Therefore masking has no effect:

```json
{
    "\\$" : 1,
    "B" : ${\\$}
}
```

The backslashes are part of the key name:

```python
DotDict({'\\$': 1, 'B': 1})
```

!!! note
    The masking requires **two** backslashes. A single backslash causes a JSON syntax error.

!!! info "Format deviation in the TestsuitesManagement"
    In opposite to the JsonPreprocessor, the **TestsuitesManagement** is more restrictive: the keys inside
    `params` → `global` become Robot Framework variables and therefore must not contain any special characters.
    Names are limited to letters, digits and underscores. Details: [Naming convention](../user-guide/naming-convention.md).
