# Release Process

Notes on the current development/release lifecyle.

## Start a new release
+   Get the latest develop branch `git checkout develop`

## Develop changes
+   Develop new feature/patch
+   Update CHANGELOG.md with changes made
+   Repeat until version completed

## Increment the version
+   Bump to the next version `./bumpnersion.sh [patch|minor|major]`
+   Add version line in CHANGELOG.md with the list of changes

## Release the current version
+   Checkout the release branch.                    `git checkout release`
+   Merge the release branch with develop.          `git merge develop`
+   Create release tag from the release branch with the same version number in the CHANGELOG.md using github web page
