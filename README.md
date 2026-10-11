# XPS Carbon Correction Tool

Tkinter application to shift binding energies in Excel XPS spectra using a user-selected C 1s reference.

## Run
`pip install -r requirements.txt` then `python xps_gui.py`.

Input: worksheet `Spectrum_1` with `Binding Energy (eV)` and `Corrected Intensity` columns.

## Scientific limitations
The maximum-intensity position is not necessarily the adventitious-carbon C–C/C–H component. The software applies a numerical shift, not instrument calibration or peak fitting. Verify the reference and check for differential charging.

## Release preparation
The installer declares 1.0.1. Source and installers require validation before public release. License and citation metadata are pending author approval.


## Batch command-line use

```powershell
python xps_correction.py --carbon "test_files/C1s Scan.xlsx" --input "test_files/Pb4f Scan.xlsx" "test_files/S2p Scan.xlsx" --output corrected_files --reference 284.8
```

The command-line program writes a `Corrected_Data` sheet, a `Correction_Metadata` sheet, and a spectrum chart per file. The C 1s maximum is only a numerical proxy; verify the actual chemical reference before interpreting binding energies. The Tkinter GUI remains a separate workflow and has not yet been updated to use this new CLI implementation.

## GUI/CLI consistency

Both interfaces now use `xps_correction.py` for peak-maximum energy referencing and Excel exports. See `INTEGRATION_TEST.md` for verification and scientific limitations.
