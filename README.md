# csv-norm

To run `csv-norm`, you'll need Python `3.7.x` along with
[pipenv](https://pipenv.readthedocs.io/en/latest/).

`csv-norm` reads CSV data from `stdin` and emits the normalized rendition
of that data to `stdout`.

A CSV whose column headings can't be read will raise an exception, and no
normalization will be attempted. If the CSV is parseable but data is encountered
that cannot be normalized, `WARNING`s will be written to `stderr`, and the row in
question will be dropped from the output.

Example usage:

```bash
cat ~/sample.csv | bin/csv-norm > ~/sample-normalized.csv
```