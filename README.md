## alignschema

Generate and run `ogr2ogr` commands using a CSV to rename fields, thus aligning the schemas of many input files.

The csv should be set up with column names that contain the desired field names. The values of the field should be the field name in source. Blank fields are ignored.
Column names that match `ogr2ogr` options will be used to create those options and flags. For example:

```
src_datasource_name,id,name,year,skipfailures,dst_datasource_name
espanol.shp,gid,nombre,,,PG:dbname=example
francais.shp,ID,nom,1,,PG:dbname=example
```

This will generate two `ogr2ogr` commands. In the second command, the `skipfailures` flag will be added. In the first command, the field `year` won't be populated because that column is blank. Additional flags can be added to `alignschema`:

```
alignschema input.csv -t_srs EPSG:4326
```

### Usage

```
usage: alignschema [-h] [--dry-run]
                   [--dst-datasource-name DST_DATASOURCE_NAME] [--layer LAYER]
                   csvfile

Construct an ogr2ogr command that maps field names based on a CSV.

positional arguments:
  csvfile               Contains columns that match ogr2ogr import options.
                        Any unrecognized columns will be used in sql
                        statement, e.g. SELECT value AS column

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             echo command, do not execute
  --dst-datasource-name DST_DATASOURCE_NAME
  --layer LAYER

Additional arguments are passed to ogr2ogr.
```
