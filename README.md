# csv-norm

`csv-norm` reads CSV data from `stdin` and emits a normalized rendition of that
data to `stdout`.

A CSV whose column headings can't be read will raise an exception, and no
normalization will be attempted. If the CSV is parseable but a row's data
cannot be normalized, `WARNING`s will be written to `stderr`, and the row in
question will be dropped from the output.

#### Setup

To run `csv-norm`, you'll need Python `3.7.x` along with
[pipenv](https://pipenv.readthedocs.io/en/latest/). Once you have those, install
the dependencies:

```bash
pipenv install
```

#### Usage

```bash
cd $PATH_TO_REPO
cat ~/sample.csv | bin/csv-norm > ~/sample-normalized.csv
```

#### Tests

You can run the tests from the top of the repo:

```bash
pipenv install --dev
pipenv run pytest
```
