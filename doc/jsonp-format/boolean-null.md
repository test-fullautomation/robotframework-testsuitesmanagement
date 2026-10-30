# Boolean and null values

JSON supports the boolean values `true` and `false`, and also the null value `null`.
In Python, the corresponding values differ: `True`, `False` and `None`.

Because the JsonPreprocessor is a Python application and therefore the returned content is required to be Python compatible,
the JsonPreprocessor does the conversion automatically.

Accepted in JSONP files are **both** styles:

```json
{
   "param_06" : true,
   "param_07" : false,
   "param_08" : null,
   "param_09" : True,
   "param_10" : False,
   "param_11" : None
}
```

The output contains all keywords in Python style only:

```python
{'param_06': True,
 'param_07': False,
 'param_08': None,
 'param_09': True,
 'param_10': False,
 'param_11': None}
```

| JSON keyword | Python keyword (also allowed in JSONP) | Result in Python |
|---|---|---|
| `true` | `True` | `True` |
| `false` | `False` | `False` |
| `null` | `None` | `None` |

!!! note
    The TestsuitesManagement loads all configuration files with the JsonPreprocessor syntax setting `python`.
    Therefore both styles are always accepted.

In Robot Framework the values are available as `${True}`, `${False}` and `${None}`:

```robotframework
Should Be True    ${param_06}
Should Be Equal    ${param_08}    ${None}
```
