import tempfile
import unittest
from pathlib import Path
import pandas as pd
from xps_correction import calculate_shift, correct_file

class EngineTests(unittest.TestCase):
    def test_shift_and_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / 'carbon.xlsx'
            with pd.ExcelWriter(source) as w:
                pd.DataFrame({'Binding Energy (eV)': [284.0, 285.0, 286.0], 'Corrected Intensity': [1, 10, 2], 'Extra': ['a','b','c']}).to_excel(w, sheet_name='Spectrum_1', index=False)
            shift, measured = calculate_shift(source, 284.8)
            self.assertAlmostEqual(shift, -0.2)
            dest = root / 'corrected.xlsx'
            correct_file(source, dest, shift, measured, 284.8, source)
            data = pd.read_excel(dest, sheet_name='Corrected_Data')
            self.assertAlmostEqual(data.loc[1, 'Binding Energy (eV)'], 284.8)
            self.assertIn('Extra', data.columns)
            meta = pd.read_excel(dest, sheet_name='Correction_Metadata')
            self.assertAlmostEqual(meta.loc[0, 'applied_shift_eV'], -0.2)

if __name__ == '__main__': unittest.main()
