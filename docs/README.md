## Documentation

Documentation is now being build for the `gh-pages` branch.

To build a new version of the documentation you need to do the following:

```
# checkout latest build
$ git checkout develop

# make the docs
$ make docs

# checkout gh-pages
$ git checkout gh-pages

# copy over the new build files from the html dir
