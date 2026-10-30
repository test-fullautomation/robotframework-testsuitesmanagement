# The JSONP format - overview

All configuration files of the TestsuitesManagement are written in the **JSONP** format - an extended JSON format.
The JSONP format is computed by the Python package **JsonPreprocessor**
([GitHub](https://github.com/test-fullautomation/python-jsonpreprocessor)), which is called internally by the
TestsuitesManagement during the `testsuite_setup`.

This chapter explains the format of JSONP files in detail - step by step, from plain JSON to the advanced features.
We concentrate on the content of the JSONP files and the corresponding results, available as Python dictionary.

!!! tip "Where do JSONP values end up in Robot Framework?"
    The examples in this chapter show the resulting Python dictionary. In a TestsuitesManagement configuration
    all keys below `params` → `global` become Robot Framework variables (`${param1}`), and the top level
    parameters are available in `${CONFIG}`. See [Content of configuration files](../user-guide/configuration-files.md).

## Learning path

The sections build on each other. If you are new to JSONP, read them in this order:

```mermaid
flowchart LR
    subgraph basics["Basics"]
        direction TB
        A[Standard JSON] --> B[Boolean and null values] --> C[Comments]
    end
    subgraph structure["Structuring"]
        direction TB
        D[Import of JSON files] --> E[Overwriting parameters]
    end
    subgraph advanced["Advanced"]
        direction TB
        F[dotdict notation] --> G[Dynamic key names] --> H[Implicit creation of dictionaries] --> I[Python inline code]
    end
    subgraph details["Details"]
        direction TB
        J[Special characters] --> K[Byte sequences]
    end
    basics --> structure --> advanced --> details
```

| Section | You learn ... |
|---|---|
| [Standard JSON format](standard-json.md) | that every valid JSON file is also a valid JSONP file |
| [Boolean and null values](boolean-null.md) | to use `true`/`True`, `false`/`False`, `null`/`None` |
| [Comments](comments.md) | to document your configuration with `//` and `/* */` |
| [Import of JSON files](imports.md) | to split a configuration into several files |
| [Overwriting parameters](overwriting-parameters.md) | to reference and to change existing values with `${...}` |
| [dotdict notation](dotdict-notation.md) | a shorter notation to access nested values |
| [Dynamic key names](dynamic-key-names.md) | to address keys by means of parameters |
| [Implicit creation of dictionaries](implicit-creation.md) | to create nested dictionaries in one line |
| [Python inline code](python-inline-code.md) | to compute values with Python expressions `<<...>>` |
| [Special characters within key names](special-characters.md) | which characters are not allowed in key names |
| [Byte sequences](byte-sequences.md) | to embed binary values |

The [Cheat sheet](cheat-sheet.md) summarizes the complete syntax on one page.

## The basic idea: the dollar operator

Most of the JSONP features are built around one single syntax element - the **dollar operator** `${...}`.
It refers to a parameter that is defined somewhere in the JSONP file (or in an imported file).

```json
{
   "name"     : "World",
   "greeting" : "Hello ${name}!",      // right-hand side: read a value
   ${name}    : "JSONP"                // left-hand side: overwrite a value
}
```

| Position | Meaning | Example |
|---|---|---|
| Right-hand side of the colon, without quotes | value with original data type | `"b" : ${a}` |
| Right-hand side of the colon, inside quotes | value converted to string | `"b" : "prefix_${a}"` |
| Left-hand side of the colon (never in quotes) | overwrite or create a value | `${a} : 1` |

## How to read the examples

- Every example can be tried out with a few lines of Python (the JsonPreprocessor is installed together with
  the TestsuitesManagement):

    ```python
    from pprint import pprint
    from JsonPreprocessor import CJsonPreprocessor

    pprint(CJsonPreprocessor().jsonLoad("./example.jsonp"))
    ```

- Some examples show only a part of a JSONP file (without the outer curly brackets).
  In a TestsuitesManagement configuration such parts are usually placed inside `params` → `global`.
- The **outcome** is shown in the format of Python's `pprint` for dictionaries (keys sorted alphabetically).
  The real return value is a `DotDict`, see [Standard JSON format](standard-json.md).

!!! info "JsonPreprocessor and TestsuitesManagement"
    Because Robot Framework has its own syntax rules, the JSONP format deviates in some cases between the pure
    Python world (JsonPreprocessor) and the Robot Framework world (TestsuitesManagement). Where this is the case,
    you find a corresponding hint. The most important deviation: key names inside `params` → `global` have to follow
    the [naming convention](../user-guide/naming-convention.md) of Robot Framework variables.
