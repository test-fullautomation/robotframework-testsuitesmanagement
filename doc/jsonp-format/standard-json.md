# Standard JSON format

The JsonPreprocessor supports JSON files with the standard extension `.json` and standard content.

**JSON file:**

```json
{
   "param1" : "value1",
   "param2" : "value2"
}
```

**Outcome:**

```python
{'param1': 'value1', 'param2': 'value2'}
```

A JSON file with the extension `.jsonp` and the same content produces the same output.

!!! tip "Recommendation"
    Give every JSON file the extension `.jsonp` to have a strict separation between the standard and the extended JSON format.

## Data types

The following example still contains standard JSON content, but with parameters of several different
data types (simple and composite):

```json
{
   "param_01" : "string",
   "param_02" : 123,
   "param_03" : 4.56,
   "param_04" : ["A", "B", "C"],
   "param_05" : {"A" : 1, "B" : 2, "C" : 3}
}
```

**Outcome:**

```python
{'param_01': 'string',
 'param_02': 123,
 'param_03': 4.56,
 'param_04': ['A', 'B', 'C'],
 'param_05': {'A': 1, 'B': 2, 'C': 3}}
```

| JSON | Python |
|---|---|
| string | `str` |
| number (integer) | `int` |
| number (real) | `float` |
| array | `list` |
| object | `dict` (returned as `DotDict`) |

## The returned dictionary type

Dictionaries are returned as **`DotDict`**. A `DotDict` behaves like a normal dictionary, but additionally
allows to access elements with a dot notation. The TestsuitesManagement also converts every dictionary inside
`params` → `global` into a Robot Framework `DotDict`, so both notations work in robot files:

```robotframework
Log    ${param_05}[A]     # standard access
Log    ${param_05.A}      # dot notation
```

Details about the corresponding notation *inside* JSONP files can be found in section [dotdict notation](dotdict-notation.md).
