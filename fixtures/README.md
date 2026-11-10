# Fixtures

## `timetable/`

XML timetable files for the legacy import task. Characterization seeding runs:

```text
./symfony doctrine:insert-sql --env=prod
./symfony candle:import --env=prod --ignore-warnings --no-generate-slugs \
  /fixtures/timetable/rozvrh.xml
```

`compose.test.yaml` mounts this directory into the legacy container at `/fixtures`.
The import task asks for confirmation; tests answer `y` on stdin.

`--no-generate-slugs` avoids a `setlocale` failure in the legacy image during seed.
