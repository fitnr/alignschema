#!/usr/bin/env python3
from os import path
import subprocess
import argparse
import csv

OGR2OGR_OPTIONS = {
    'options': (
        'where', 'dialect', 'fid', 'limit', 'spat', 'spat_srs', 'geomfield',
        'a_srs', 't_srs', 's_srs', 'f', 'overwrite', 'dsco', 'lco', 'nln',
        'nlt', 'dim', 'gt', 'oo', 'doo', 'clipsrc', 'clipsrcsql', 'clipsrclayer',
        'clipsrcwhere', 'clipdst', 'clipdstsql', 'clipdstlayer', 'clipdstwhere',
        'datelineoffset', 'simplify', 'segmentize', 'addfields', 'unsetFid', 'relaxedFieldNameMatch',
        'fieldTypeToString', 'unsetFieldWidth', 'mapFieldType', 'fieldmap', 'maxsubfields',
        'zfield', 'gcp', 'order', 'mo',
    ),
    'flags': (
        'skipfailures', 'preserve_fid', 'append', 'update', 'progress',
        'splitlistfields', 'explodecollections', 'ds_transaction', 'nomd',
        'noNativeData', 'wrapdateline', 'tps', 'forceNullable', 'unsetDefault',
    ),
    'positional': ('dst_datasource_name', 'src_datasource_name', 'layer')

}


def generate(entry, **kwargs):
    output, fields = [], []
    entry.update(kwargs)

    # First, append positional arguments
    for k in OGR2OGR_OPTIONS['positional']:
        if k in entry:
            output.append('"{}"'.format(entry[k]))

    # Next, append options and flags
    for k, v in entry.items():
        if k in OGR2OGR_OPTIONS['options']:
            output.extend(['-{}'.format(k), v])

        elif k in OGR2OGR_OPTIONS['flags'] and v:
            output.append('-{}'.format(k))

        elif k in OGR2OGR_OPTIONS['positional']:
            pass

        else:
            if v:
                fields.append('"{}" AS "{}"'.format(v, k))

    # Finally, generate the -sql flag
    layer = entry.get('layer', path.splitext(path.basename(entry.get('src_datasource_name')))[0])
    sql = ['-sql', """'SELECT {} FROM "{}"'""".format(', '.join(fields), layer)]
    output.extend(sql)

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Construct an ogr2ogr command that maps field names based on a CSV",
        epilog="Additional arguments are passed to ogr2ogr."
    )
    parser.add_argument('csvfile', help=(
        'Contains columns that match ogr2ogr import options. '
        'Any unrecognized columns will be used in sql statement, e.g. SELECT value AS column'
    ))
    parser.add_argument('-n', '--dry-run', action='store_true', help='echo command, do not execute')
    parser.add_argument('-d', '--dst-datasource-name', type=str)
    parser.add_argument('-l', '--layer', type=str)

    args, extra = parser.parse_known_args()

    kwargs = {}
    if args.dst_datasource_name:
        kwargs['dst_datasource_name'] = args.dst_datasource_name
    if args.layer:
        kwargs['layer'] = args.layer

    with open(args.csvfile, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = generate(row, **kwargs)
            command = ['ogr2ogr'] + result + extra

            if args.dry_run:
                print(' '.join(command))
            else:
                subprocess.check_call(command)


if __name__ == '__main__':
    main()
