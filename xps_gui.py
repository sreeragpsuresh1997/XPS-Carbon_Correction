import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
from xps_correction import calculate_shift as engine_calculate_shift, correct_file as engine_correct_file


class XPSCorrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XPS Carbon Correction Tool")
        self.root.geometry("650x700")
        self.root.resizable(False, False)

        # ==========================================================
        # WATERMARK INFORMATION
        # ==========================================================
        self.watermark_name = "Sreerag Ponnarassery Suresh Babu"
        self.watermark_affiliation = "UANL, FIME [2024-2028]"

        # Variables to store our file paths and shift
        self.carbon_file = ""
        self.other_files = []
        self.output_folder = ""
        self.shift_value = None

        self.setup_ui()

    def setup_ui(self):
        # ==========================================================
        # TITLE
        # ==========================================================
        title_label = tk.Label(
            self.root,
            text="XPS Carbon Correction",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            self.root,
            text="X-ray Photoelectron Spectroscopy",
            font=("Arial", 9),
            fg="gray"
        )
        subtitle_label.pack(pady=(0, 5))

        # ==========================================================
        # STANDARD CARBON REFERENCE
        # ==========================================================
        ref_frame = tk.Frame(self.root)
        ref_frame.pack(pady=5)

        lbl_ref = tk.Label(
            ref_frame,
            text="Standard Carbon Reference (eV):",
            font=("Arial", 10)
        )
        lbl_ref.pack(side=tk.LEFT, padx=5)

        self.entry_ref = tk.Entry(
            ref_frame,
            width=10,
            font=("Arial", 10)
        )
        self.entry_ref.insert(0, "284.8")
        self.entry_ref.pack(side=tk.LEFT, padx=5)

        # ==========================================================
        # 1. SELECT CARBON FILE
        # ==========================================================
        btn_carbon = tk.Button(
            self.root,
            text="1. Select Carbon (C1s) File",
            width=30,
            command=self.select_carbon
        )
        btn_carbon.pack(pady=5)

        self.lbl_carbon = tk.Label(
            self.root,
            text="No C1s file selected",
            fg="gray"
        )
        self.lbl_carbon.pack()

        # ==========================================================
        # 2. SELECT OTHER ELEMENT FILES
        # ==========================================================
        btn_other = tk.Button(
            self.root,
            text="2. Select Other Element/Survey Files",
            width=30,
            command=self.select_others
        )
        btn_other.pack(pady=5)

        self.lbl_other = tk.Label(
            self.root,
            text="0 files selected",
            fg="gray"
        )
        self.lbl_other.pack()

        # ==========================================================
        # 3. SELECT OUTPUT FOLDER
        # ==========================================================
        btn_folder = tk.Button(
            self.root,
            text="3. Select Output Folder",
            width=30,
            command=self.select_folder
        )
        btn_folder.pack(pady=5)

        self.lbl_folder = tk.Label(
            self.root,
            text="No output folder selected",
            fg="gray"
        )
        self.lbl_folder.pack()

        # ==========================================================
        # DIVIDER
        # ==========================================================
        ttk.Separator(
            self.root,
            orient='horizontal'
        ).pack(fill='x', pady=10, padx=20)

        # ==========================================================
        # 4. CALCULATE SHIFT
        # ==========================================================
        btn_calc = tk.Button(
            self.root,
            text="4. Calculate Carbon Shift",
            width=30,
            font=("Arial", 10, "bold"),
            command=self.calculate_shift
        )
        btn_calc.pack(pady=5)

        self.lbl_shift = tk.Label(
            self.root,
            text="Calculated Shift: Pending...",
            font=("Arial", 12),
            fg="blue"
        )
        self.lbl_shift.pack()

        # ==========================================================
        # 5. EXECUTE CORRECTION
        # ==========================================================
        btn_exec = tk.Button(
            self.root,
            text="5. Execute Corrections & Save",
            width=30,
            font=("Arial", 10, "bold"),
            bg="lightgreen",
            command=self.execute_corrections
        )
        btn_exec.pack(pady=10)

        # ==========================================================
        # 6. PROGRESS BAR
        # ==========================================================
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress.pack(pady=5)

        # ==========================================================
        # LOG OUTPUT
        # ==========================================================
        self.log_text = tk.Text(
            self.root,
            height=8,
            width=70,
            state='disabled'
        )
        self.log_text.pack(pady=5)

        # ==========================================================
        # 7. EXIT BUTTON
        # ==========================================================
        btn_exit = tk.Button(
            self.root,
            text="Exit Program",
            width=20,
            command=self.root.quit
        )
        btn_exit.pack(pady=8)

        # ==========================================================
        # WATERMARK
        # ==========================================================
        watermark_frame = tk.Frame(self.root)
        watermark_frame.pack(
            side=tk.BOTTOM,
            pady=(2, 8)
        )

        watermark_name_label = tk.Label(
            watermark_frame,
            text=self.watermark_name,
            font=("Arial", 8),
            fg="gray"
        )
        watermark_name_label.pack()

        watermark_affiliation_label = tk.Label(
            watermark_frame,
            text=self.watermark_affiliation,
            font=("Arial", 8),
            fg="gray"
        )
        watermark_affiliation_label.pack()

    # ==============================================================
    # HELPER FUNCTION: LOG MESSAGE
    # ==============================================================
    def log_message(self, message):
        """Prints messages to the text box in the GUI."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()

    # ==============================================================
    # SELECT CARBON FILE
    # ==============================================================
    def select_carbon(self):
        self.carbon_file = filedialog.askopenfilename(
            title="Select C1s Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if self.carbon_file:
            self.lbl_carbon.config(
                text=os.path.basename(self.carbon_file),
                fg="black"
            )

            self.log_message(
                f"Selected Carbon File: "
                f"{os.path.basename(self.carbon_file)}"
            )

    # ==============================================================
    # SELECT OTHER FILES
    # ==============================================================
    def select_others(self):
        self.other_files = filedialog.askopenfilenames(
            title="Select Other Excel Files",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if self.other_files:
            self.lbl_other.config(
                text=f"{len(self.other_files)} files selected",
                fg="black"
            )

            self.log_message(
                f"Selected {len(self.other_files)} additional files."
            )

    # ==============================================================
    # SELECT OUTPUT FOLDER
    # ==============================================================
    def select_folder(self):
        self.output_folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if self.output_folder:
            self.lbl_folder.config(
                text=self.output_folder,
                fg="black"
            )

            self.log_message(
                f"Output folder set to: {self.output_folder}"
            )

    # ==============================================================
    # CALCULATE CARBON SHIFT
    # ==============================================================
    def calculate_shift(self):

        if not self.carbon_file:
            messagebox.showwarning(
                "Warning",
                "Please select a Carbon file first!"
            )
            return

        self.shift_value = None
        try:
            # Get user-defined reference value
            reference_c1s = float(self.entry_ref.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid numeric value for "
                "the Standard Carbon Reference."
            )
            return

        try:
            self.shift_value, measured_c1s_peak = engine_calculate_shift(
                self.carbon_file, reference_c1s
            )
            self.calculated_measured = measured_c1s_peak
            self.calculated_reference = self.entry_ref.get().strip()
            self.calculated_carbon_file = self.carbon_file
            self.lbl_shift.config(
                text=(
                    f"Calculated Shift: "
                    f"{self.shift_value:.3f} eV "
                    f"(Ref: {reference_c1s})"
                )
            )

            self.log_message(
                f"Calculated Shift: {self.shift_value:.3f} eV "
                f"using Reference {reference_c1s} eV "
                f"(Measured C1s: {measured_c1s_peak:.3f} eV)"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to calculate shift: {e}"
            )

    # ==============================================================
    # EXECUTE CORRECTIONS
    # ==============================================================
    def execute_corrections(self):

        if self.shift_value is None:
            messagebox.showwarning(
                "Warning",
                "Please calculate the carbon shift first!"
            )
            return

        if not self.output_folder:
            messagebox.showwarning(
                "Warning",
                "Please select an output folder first!"
            )
            return

        if not self.carbon_file:
            messagebox.showwarning("Warning", "Select a C1s file first.")
            return

        # Prevent applying a stale shift after the reference changes
        if getattr(self, "calculated_reference", None) != self.entry_ref.get().strip() or getattr(self, "calculated_carbon_file", None) != self.carbon_file:
            messagebox.showwarning("Warning", "C1s file or reference changed. Recalculate the shift.")
            return

        # Avoid silently overwriting output when different source folders
        # contain the same basename.
        # Combine carbon file and other files
        all_files = (
            [self.carbon_file]
            + list(self.other_files)
        )

        names = [os.path.basename(f).casefold() for f in all_files]
        if len(names) != len(set(names)):
            messagebox.showerror("Duplicate filenames", "Selected files contain duplicate filenames. Rename files or process separately.")
            return

        self.progress['maximum'] = len(all_files)
        self.progress['value'] = 0

        self.log_message(
            "--- Starting Corrections ---"
        )

        succeeded = 0
        failed = 0
        for idx, file_path in enumerate(all_files):

            try:
                filename = os.path.basename(file_path)

                # Shared engine: same validation, export, and metadata as CLI.
                output_file = os.path.join(self.output_folder, f"Corrected_{filename}")
                if os.path.abspath(file_path) == os.path.abspath(output_file):
                    raise ValueError("Output would overwrite source")
                engine_correct_file(
                    __import__('pathlib').Path(file_path),
                    __import__('pathlib').Path(output_file),
                    self.shift_value,
                    self.calculated_measured,
                    float(self.calculated_reference),
                    __import__('pathlib').Path(self.carbon_file),
                )
                succeeded += 1
            except Exception as e:
                failed += 1
                self.log_message(f"Error processing {file_path}: {e}")

            # ------------------------------------------------------
            # UPDATE PROGRESS BAR
            # ------------------------------------------------------
            self.progress['value'] = idx + 1
            self.root.update_idletasks()

        # ==========================================================
        # COMPLETION MESSAGE
        # ==========================================================
        self.log_message(
            f"--- Completed: {succeeded} succeeded; {failed} failed ---"
        )

        if failed:
            messagebox.showwarning("Partial completion", f"{succeeded} files saved; {failed} failed. See log.")
        else:
            messagebox.showinfo("Complete", f"{succeeded} files corrected and saved.")


# ==============================================================
# RUN APPLICATION
# ==============================================================
if __name__ == "__main__":

    root = tk.Tk()

    app = XPSCorrectionApp(root)

    root.mainloop()