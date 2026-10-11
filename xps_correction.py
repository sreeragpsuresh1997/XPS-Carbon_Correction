"""Batch C 1s energy referencing for XPS Excel exports (not instrument calibration)."""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ENERGY = 'Binding Energy (eV)'
INTENSITY = 'Corrected Intensity'
SHEET = 'Spectrum_1'

def load_spectrum(path):
    df = pd.read_excel(path, sheet_name=SHEET)
    for col in (ENERGY, INTENSITY):
        if col not in df.columns:
            raise ValueError(f'{path}: missing required column {col!r}')
    return df

def calculate_shift(carbon_file, reference):
    if not math.isfinite(reference):
        raise ValueError('Reference must be finite')
    df = load_spectrum(carbon_file)
    intensity = pd.to_numeric(df[INTENSITY], errors='coerce')
    energy = pd.to_numeric(df[ENERGY], errors='coerce')
    valid = intensity.notna() & energy.notna() & energy.map(math.isfinite) & intensity.map(lambda v: math.isfinite(v) if pd.notna(v) else False)
    if not valid.any():
        raise ValueError('No valid energy/intensity pairs in C 1s spectrum')
    measured = float(energy.loc[intensity[valid].idxmax()])
    return reference - measured, measured

def correct_file(source, destination, shift, measured, reference, carbon_file):
    df = load_spectrum(source).copy()
    energy = pd.to_numeric(df[ENERGY], errors='coerce')
    if energy.isna().any() or not energy.map(math.isfinite).all():
        raise ValueError(f'{source}: invalid binding-energy values')
    df[ENERGY] = energy + shift
    provenance = pd.DataFrame([{
        'source_file': str(source), 'carbon_reference_file': str(carbon_file),
        'reference_eV': reference, 'measured_maximum_eV': measured,
        'applied_shift_eV': shift, 'method': 'C1s maximum intensity (not peak fitting)',
        'processed_utc': datetime.now(timezone.utc).isoformat()
    }])
    with pd.ExcelWriter(destination, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Corrected_Data', index=False)
        provenance.to_excel(writer, sheet_name='Correction_Metadata', index=False)
        ws = writer.sheets['Corrected_Data']
        chart = writer.book.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        cols = list(df.columns)
        chart.add_series({'name': source.stem, 'categories': ['Corrected_Data', 1, cols.index(ENERGY), len(df), cols.index(ENERGY)], 'values': ['Corrected_Data', 1, cols.index(INTENSITY), len(df), cols.index(INTENSITY)]})
        chart.set_x_axis({'name': ENERGY, 'reverse': True})
        chart.set_y_axis({'name': INTENSITY})
        ws.insert_chart(1, len(cols)+2, chart)

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--carbon', required=True, type=Path, help='C 1s .xlsx file')
    p.add_argument('--input', nargs='*', type=Path, default=[], help='Additional XPS .xlsx files')
    p.add_argument('--output', required=True, type=Path, help='Output directory')
    p.add_argument('--reference', type=float, default=284.8, help='Chosen C 1s reference in eV (default 284.8)')
    a = p.parse_args(argv)
    try:
        shift, measured = calculate_shift(a.carbon, a.reference)
    except Exception as exc:
        p.exit(2, f'Cannot calculate correction: {exc}\n')
    a.output.mkdir(parents=True, exist_ok=True)
    failures = []
    for source in dict.fromkeys([a.carbon, *a.input]):
        target = a.output / ('Corrected_' + source.name)
        if source.resolve() == target.resolve():
            failures.append(f'{source}: would overwrite source')
            continue
        try:
            correct_file(source, target, shift, measured, a.reference, a.carbon)
            print(f'OK: {target}')
        except Exception as exc:
            failures.append(f'{source}: {exc}')
    print(f'Shift: {shift:+.4f} eV; {len(failures)} failure(s)')
    for failure in failures:
        print('ERROR:', failure)
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
