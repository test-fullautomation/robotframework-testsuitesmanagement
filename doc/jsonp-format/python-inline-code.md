# Python inline code

## Motivation

It might be required to have access to Python builtin functions, e.g. for combining multiple lists into a single list.
In pure Python:

```python
A = [1,2,3]
B = [4,5,6]
C = A + B
print(C)      # [1, 2, 3, 4, 5, 6]
```

In JSONP files, the implementation looks as follows:

```json
"A" : [1,2,3],
"B" : [4,5,6],
"C" : <<${A} + ${B}>>
```

The expression `${A} + ${B}` is handled as **Python inline code**. Dollar operator expressions can be used inside
Python inline code to access any other parameter defined in the JSONP files.

## Syntax

```text
<<(Python expression)>>
```

The result of the expression must be of a data type that is supported by JSON: `str`, `int`, `float`, `bool`,
`None`, `list` or `dict`.

## Limitations

| Not allowed | Example |
|---|---|
| Inside strings | `"param" : "The value is <<1 + 1>>"` |
| In key names (left-hand side of the colon) | `<<"key" + "1">> : 1` |
| Directly as index of a value to be overwritten | `${param}[<<0 if True else 1>>] : 4` |
| As element of a list | `"param" : [<<1 + 1>>, 3]` |
| Inside a dollar operator expression | `${<<"name">>}` |

The usage of Python inline code is limited to the **right-hand side of the colon** (key values).

**Workaround for indices:** compute the index in a separate parameter first:

```json
"param" : [1,2,3],
"index" : <<0 if True else 1>>,
${param}[${index}] : 4
```

## Further examples

*Create a list of dictionary keys:*

```json
"dict"     : {"kA" : "vA", "kB" : "vB"},
"key_list" : <<list(${dict}.keys())>>
```

**Outcome:**

```python
{'dict': {'kA': 'vA', 'kB': 'vB'}, 'key_list': ['kA', 'kB']}
```

*Define an import path:*

```json
"path_1" : "./file_1.jsonp",
"path_2" : "./file_2.jsonp",
//
"[import]" : <<${path_1} if True else ${path_2}>>
```

*Extend a list:*

```json
"testlist" : [1, 2],
${testlist} : <<${testlist} + [3]>>
```

!!! danger "Security"
    Python inline code is **executed** by the JsonPreprocessor. Only load JSONP files from **trusted sources** -
    a JSONP file is as powerful as a Python script.
