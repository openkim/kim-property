# External

External contains `openkim-properties` used in `kim-python-utils`.

## Contents

It should contain the following folder:

````sh
external
`-- openkim-properties  https://github.com/openkim/openkim-properties.git
````

## openkim-properties submodule

* Cloning `kim-python-utils` repository with this `openkim-properties` submodule

```sh
git clone --recursive git@github.com:openkim/kim-python-utils.git
```

or clone using the HTTPS URL (recommended)

```sh
git clone --recursive https://github.com/openkim/kim-python-utils.git
```

* Loading the `openkim-properties` submodule if you already have cloned the
`kim-python-utils` repository


```sh
git submodule update --init
```

* To fetch/pull all changes in `kim-python-utils` repository including
changes in the `openkim-properties` submodule

```sh
git pull --recurse-submodules
```

* To fetch/pull all changes for `openkim-properties` submodule

```sh
git submodule update --remote
```
