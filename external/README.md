# External

External contains `openkim-properties` used in `kim-property`.

## Contents

It should contain the following folder:

````sh
external
|-- README.md
`-- openkim-properties  https://github.com/openkim/openkim-properties.git
````

## openkim-properties submodule

Cloning `kim-property` repository with this `openkim-properties` submodule

```sh
git clone --recursive git@github.com:openkim/kim-property.git
```

or clone using the HTTPS URL (recommended)

```sh
git clone --recursive https://github.com/openkim/kim-property.git
```

Loading the `openkim-properties` submodule if you already have cloned the
`kim-property` repository

```sh
git submodule update --init
```

To fetch/pull all changes in `kim-property` repository including
changes in the `openkim-properties` submodule

```sh
git pull --recurse-submodules
```

To fetch/pull all changes for `openkim-properties` submodule

```sh
git submodule update --remote
```
