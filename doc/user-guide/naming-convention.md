# Naming convention

Keys defined within `params` → `global` become **Robot Framework variables**. Therefore the key names must conform to
the naming conventions of Robot Framework.

## The rule

Key names may only contain letters, digits and underscores, and must start with a letter.

Internally this is realized by the regular expression `^\p{L}[\p{L}\p{Nd}_]*$` (letters include non-ASCII letters).

| Valid | Invalid |
|---|---|
| `"abcParam"` | `"+param01"` |
| `"abcParam01"` | `"param$01"` |
| `"abc_Param_01"` | `"abc#Param"` |
| | `"01abc_Param"` |

An invalid name aborts the execution:

```text
Variable name '01abc_Param' is invalid. Expected format: '^\p{L}[\p{L}\p{Nd}_]*$' (letters, digits, underscores)
Please check variable '01abc_Param' in params['global'] in the configuration file '...'
```

!!! note
    The rule applies only to the keys **directly** below `params` → `global`. Keys of nested dictionaries are not
    Robot Framework variables and follow the [JSONP rules](../jsonp-format/special-characters.md).

## Reserved names

The following names are reserved by Robot Framework and must not be used as parameter names:

`Settings`, `Variables`, `Keywords`, `Comments`, `Documentation`, `Metadata`

## Underscores and case

!!! warning "Caution"
    Robot Framework ignores underscores (and the case) in variable names. Underscores are allowed, but you must be
    aware of the consequences.

**Example**

```json
"params" : {
             "global": {
                         "ABC"     : "A",
                         "ABC__"   : "B",
                         "A__B__C" : "C"
                       }
           }
```

With

```robotframework
Log    ABC: ${ABC}
Log    ABC__: ${ABC__}
Log    A__B__C: ${A__B__C}
```

the result is

```text
INFO - ABC: C
INFO - ABC__: C
INFO - A__B__C: C
```

!!! danger "Impact"
    Three Robot Framework variables with different names are created, but all have the same value - the last
    definition wins. **Underscores and upper/lower case must not be used to distinguish between variables!**
