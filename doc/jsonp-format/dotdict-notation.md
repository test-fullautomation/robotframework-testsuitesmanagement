# dotdict notation

## Two notations for the same thing

Up to now we have accessed dictionary keys in the **standard notation**:

```json
${dictionary}['key']['sub_key']
```

Additionally, the JsonPreprocessor supports the so called **dotdict notation** where keys are handled as attributes:

```json
${dictionary.key.sub_key}
```

| | Standard notation | dotdict notation |
|---|---|---|
| Syntax | `${dictionary}['key']['sub_key']` | `${dictionary.key.sub_key}` |
| Position of keys | in square brackets, **outside** the curly brackets | separated by dots, **inside** the curly brackets |
| Dots in key names | allowed | **not allowed** |
| List indices | `[0]` | `.0` |
| Readability of deeply nested expressions | good | decreases quickly |

## Dots inside key names

In standard notation key names are allowed to contain dots:

```json
${dictionary}['key']['sub.key']
```

In dotdict notation this would cause ambiguities:

```json
${dictionary.key.sub.key}
```

Therefore this is not possible! If you need dots inside key names, you must use the standard notation.

!!! tip "Recommendation"
    Prefer underscores as separator inside key names - like done in all examples in this documentation.
    *Do you really need dots inside key names?*

## Example

In the following example we create a composite data structure and access single elements in both notations:

```json
{
   // composite data structure
   "params" : [{"dict_1_key_1" : "dict_1_key_1 value",
                "dict_1_key_2" : ["dict_1_key_2 value 1", "dict_1_key_2 value 2"]},
               //
               {"dict_2_key_1" : "dict_2_key_1 value",
                "dict_2_key_2" : {"dict_2_A_key_1" : "dict_2_A_key_1 value",
                                  "dict_2_A_key_2" : ["dict_2_A_key_2 value 1", "dict_2_A_key_2 value 2"]}}],
   //
   // access to single elements of composite data structure
   //
   // a) standard notation
   "dict_1_key_2_value_2_standard" : ${params}[0]['dict_1_key_2'][1],
   // b) dotdict notation
   "dict_1_key_2_value_2_dotdict" : ${params.0.dict_1_key_2.1},
   //
   // c) standard notation
   "dict_2_A_key_2_value_2_standard" : ${params}[1]['dict_2_key_2']['dict_2_A_key_2'][1],
   // d) dotdict notation
   "dict_2_A_key_2_value_2_dotdict" : ${params.1.dict_2_key_2.dict_2_A_key_2.1}
}
```

**Outcome:**

```python
{'dict_1_key_2_value_2_dotdict': 'dict_1_key_2 value 2',
 'dict_1_key_2_value_2_standard': 'dict_1_key_2 value 2',
 'dict_2_A_key_2_value_2_dotdict': 'dict_2_A_key_2 value 2',
 'dict_2_A_key_2_value_2_standard': 'dict_2_A_key_2 value 2',
 'params': [{'dict_1_key_1': 'dict_1_key_1 value',
             'dict_1_key_2': ['dict_1_key_2 value 1', 'dict_1_key_2 value 2']},
            {'dict_2_key_1': 'dict_2_key_1 value',
             'dict_2_key_2': {'dict_2_A_key_1': 'dict_2_A_key_1 value',
                              'dict_2_A_key_2': ['dict_2_A_key_2 value 1',
                                                 'dict_2_A_key_2 value 2']}}]}
```

!!! warning "Keep it readable"
    The dotdict notation is a reduced one. Because parts are missing (e.g. the single quotes around key names),
    the outcome can be code that is hard to understand. When the data structure becomes more and more nested
    (and if also the key names contain numbers), expressions like `${params.1.dict_2_key_2.dict_2_A_key_2.1}`
    become challenging. In such cases prefer the standard notation.

## dotdict access in Robot Framework

Independent from the notation inside the JSONP file, dictionaries defined in `params` → `global` are available as
`DotDict` in Robot Framework. Therefore the dot notation can also be used in robot files:

```robotframework
Log    ${dictionary.key.sub_key}
Log    ${dictionary}[key][sub_key]
```

!!! warning "Top level key `params` in TestsuitesManagement configurations"
    The example above uses `params` as a plain JSONP key. In a TestsuitesManagement parameter configuration file the
    top level key `params` is reserved and must contain the dictionary `global`. Use other key names for your own data.
