# datasources

Repository with the BridgeDb data source. The reason to abstract this out is that other tools no longer depend
on updates of the BridgeDb Java library to use the information.

The following URLs can be used in downstream tools:

* [https://bridgedb.github.io/datasources/datasources.tsv](https://bridgedb.github.io/datasources/datasources.tsv)
* [https://bridgedb.github.io/datasources/datasources_headers.tsv](https://bridgedb.github.io/datasources/datasources_headers.tsv)
* [https://bridgedb.github.io/datasources/organisms.tsv](https://bridgedb.github.io/datasources/organisms.tsv)

## Testing

There are tests for data integrity that can be run with the following commands
in the shell:

```bash
$ pip install tox
$ tox
```
