# Comments

## Line comments

Comments can be added to JSONP files with `//`:

```json
{
   // JSON keywords
   "param_06" : true,
   "param_07" : false,
   "param_08" : null,
   // Python keywords
   "param_09" : True,
   "param_10" : False,
   "param_11" : None
}
```

All lines starting with `//` are ignored by the JsonPreprocessor. The output of this example is the same as in
section [Boolean and null values](boolean-null.md).

## Block comments and inline comments

Block comments and inline comments are realized by a pair of `/* */`:

```json
{
   /*
   "param1" : 1,
   "param2" : "A",
   */

   "testlist" : ["A1", /*"B2", "C3",*/ "D4"]
}
```

**Outcome:**

```python
{'testlist': ['A1', 'D4']}
```

!!! tip "Good practice"
    Use comments to explain the *meaning* of a parameter, its unit or the range of valid values - especially in
    files that are maintained by several people.

    ```json
    {
       // timeout for the connection to the device, in seconds (valid: 1..120)
       "connect_timeout" : 30
    }
    ```
