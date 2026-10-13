XPS Carbon Correction Tool
![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23306324.svg)
Version: 1.0.1  
Author: Sreerag Ponnarassery Suresh Babu  
Repository: https://github.com/sreeragpsuresh1997/XPS-Carbon_Correction  
DOI: https://doi.org/10.5281/zenodo.23306324
XPS Carbon Correction Tool is a Python application for applying a uniform binding-energy shift to X-ray photoelectron spectroscopy (XPS) spectra using a user-selected C 1s reference energy. It offers a graphical interface and a command-line batch workflow for supported Excel datasets.
> **Scientific scope:** This is a binding-energy *referencing* utility, not an instrument calibration or chemical-state identification tool. The software identifies the maximum-intensity position in the supplied C 1s spectrum; it does not fit individual C 1s components. Users must confirm that the selected peak is an appropriate reference for their sample.
Features
Graphical interface for selecting the C 1s reference spectrum and spectra to correct.
Editable reference binding energy (default 284.8 eV).
Automatic energy-shift calculation from the maximum-intensity position in the reference spectrum.
Batch processing of supported `.xlsx` spectra.
Corrected Excel workbooks containing data, correction metadata, and a spectrum chart.
Preservation of additional input columns in corrected workbooks.
Command-line interface for reproducible batch processing.
Download and install
Get the release files from GitHub Releases.
Windows
Download the Windows setup executable attached to the v1.0.1 release (for example, `XPS_Carbon_Correction_Setup_v1.0.1.exe`; use the actual filename shown under Assets).
Run the installer and follow its instructions.
Open XPS Carbon Correction Tool from the Start menu.
A correctly packaged standalone Windows installer does not require users to install Python separately. Windows-version compatibility depends on the tested build; Windows XP support is not verified.
Linux (Debian/Ubuntu)
If a validated Debian package is attached to the release, download the `.deb` file and install it from its download directory:
```bash
sudo apt install ./XPS_Carbon_Correction.deb
```
Replace the filename if the attached asset differs. Launch the installed application using the package's application entry or documented command. Check the package's actual version and architecture before installation; an older `.deb` build should not be described as v1.0.1 unless rebuilt and tested. Support for other Linux distributions is not established.
Run from Python source
Install Python and the project dependencies, then run:
```bash
python -m pip install -r requirements.txt
python xps_gui.py
```
The source workflow uses Tkinter; on Linux, your Python installation may also need the system Tk package (for example, `python3-tk`).
Input file format
The current engine expects Excel `.xlsx` files with a worksheet named `Spectrum_1` and these exact column headers:
Required column	Meaning
`Binding Energy (eV)`	Original binding-energy axis
`Corrected Intensity`	Intensity used to identify the C 1s maximum and generate charts
Additional columns are retained in the output. The required sheet and header names are case-sensitive. Example files, when included, can be found in `test_files/`.
Graphical workflow
Launch the application.
Select the C 1s reference workbook.
Enter the reference energy (default 284.8 eV).
Calculate the energy shift and review the measured maximum position.
Select the additional XPS workbooks to correct.
Choose an output directory and run the correction.
Inspect the corrected binding-energy values and metadata in each exported workbook.
If you change the C 1s file or reference energy, recalculate the shift before processing.
How the correction works
The software obtains the binding energy at the highest valid intensity in the selected C 1s spectrum and calculates:
[
\Delta E = E_{\mathrm{reference}} - E_{\mathrm{measured}}
]
It then shifts the binding-energy axis uniformly:
[
E_{\mathrm{corrected}} = E_{\mathrm{original}} + \Delta E
]
Example: If the selected maximum occurs at 285.38 eV and the reference is 284.80 eV, the applied shift is −0.58 eV.
This method does not perform Gaussian/Voigt fitting, background subtraction, differential-charging correction, or absolute instrument calibration.
Output files
Each successfully processed spectrum is exported as a workbook named `Corrected_<original filename>.xlsx`, containing:
`Corrected_Data`: shifted binding-energy values and the remaining data columns.
`Correction_Metadata`: source file, C 1s reference file, chosen reference energy, measured maximum, applied shift, method, and UTC processing time.
An Excel scatter chart of the corrected spectrum.
Keep the original raw XPS exports unchanged for traceability.
Command-line batch correction
Run from the repository root:
```bash
python xps_correction.py \
  --carbon "test_files/C1s Scan.xlsx" \
  --input "test_files/Pb4f Scan.xlsx" "test_files/S2p Scan.xlsx" \
  --output "corrected_files" \
  --reference 284.8
```
The C 1s reference file is included among the corrected outputs. The command prints the applied shift and reports file-processing errors.
Tests and source build
Run the automated engine tests:
```bash
python -m unittest discover -s tests -v
```
To rebuild the Windows executable from the supplied PyInstaller specification (requires PyInstaller):
```powershell
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm "XPS Carbon Correction Tool.spec"
```
Then compile `installer_script.iss` with Inno Setup. Test the resulting executable and installer before distributing them; source-code tests alone do not validate packaged installers.
Scientific limitations and good practice
The highest-intensity C 1s point is not necessarily the adventitious-carbon C–C/C–H component.
A reference energy of 284.8 eV is a convention and is not universally suitable for all samples or experimental conditions.
Noise, overlapping chemical components, surface chemistry, and differential charging can make a uniform correction misleading.
Validate the reference assignment independently and retain original uncorrected spectra.
Correction metadata documents the numerical transformation; it does not establish its scientific validity.
Citation
If this software contributes to published research, cite the version used:
Sreerag Ponnarassery Suresh Babu. XPS Carbon Correction Tool, v1.0.1.  
https://doi.org/10.5281/zenodo.23306324
GitHub can also generate a citation from the repository's `CITATION.cff` file. Use the citation information shown in the Zenodo record if it differs from this short example.
License and feedback
See the repository's `LICENSE` file for the applicable license terms. Report problems or request improvements through GitHub Issues.
