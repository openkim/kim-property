# External

External contains `openkim-properties` used in `kim-property`.

## Contents

It should contain the following folder:

```sh
external
|-- README.md
`-- openkim-properties  https://github.com/openkim/openkim-properties.git
```

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

## Updating the properties from the latest changes in openkim-properties

Once you cloned the repository with external submodule and fetch all the latest
changes from `openkim-properties`. In the package main directory,

```sh
├── LICENSE.CDDL
├── MANIFEST.in
├── README.md
├── external
├── kim_property
├── setup.cfg
├── setup.py
├── tests
└── versioneer.py
```

please run python and do as,

```sh
python
>>> import kim_property
>>> kim_property.pickle.pickle_kim_properties()
```

Now, you have the latest update from `openkim-properties`.
Please install the `kim-property` package using pip in the package main
directory,

```sh
pip install .
```
