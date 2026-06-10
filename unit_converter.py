"""
╔══════════════════════════════════════════════════════╗
║          Universal Unit Converter Tool               ║
║   Algorithm: Convert to Base Unit → Target Unit      ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


# ─────────────────────────────────────────────────────────────
#  CONVERSION DATA  (value = multiplier to reach BASE UNIT)
#  Special-case entries for non-linear conversions (temperature)
# ─────────────────────────────────────────────────────────────
CATEGORIES = {
    "Length": {
        "base": "Meter",
        "units": {
            "Meter":        1,
            "Kilometer":    1_000,
            "Centimeter":   0.01,
            "Millimeter":   0.001,
            "Micrometer":   1e-6,
            "Nanometer":    1e-9,
            "Mile":         1_609.344,
            "Yard":         0.9144,
            "Foot":         0.3048,
            "Inch":         0.0254,
            "Nautical Mile":1_852,
            "Light Year":   9.461e+15,
        }
    },
    "Weight / Mass": {
        "base": "Kilogram",
        "units": {
            "Kilogram":     1,
            "Gram":         0.001,
            "Milligram":    1e-6,
            "Microgram":    1e-9,
            "Tonne":        1_000,
            "Pound":        0.453592,
            "Ounce":        0.0283495,
            "Stone":        6.35029,
            "Carat":        0.0002,
            "Short Ton":    907.185,
            "Long Ton":     1016.05,
        }
    },
    "Temperature": {
        "base": "Celsius",   # handled specially
        "units": {
            "Celsius":      "C",
            "Fahrenheit":   "F",
            "Kelvin":       "K",
            "Rankine":      "R",
        }
    },
    "Volume": {
        "base": "Liter",
        "units": {
            "Liter":            1,
            "Milliliter":       0.001,
            "Cubic Meter":      1_000,
            "Cubic Centimeter": 0.001,
            "Cubic Inch":       0.0163871,
            "Cubic Foot":       28.3168,
            "Gallon (US)":      3.78541,
            "Gallon (UK)":      4.54609,
            "Quart":            0.946353,
            "Pint":             0.473176,
            "Cup":              0.236588,
            "Fluid Ounce":      0.0295735,
            "Tablespoon":       0.0147868,
            "Teaspoon":         0.00492892,
        }
    },
    "Area": {
        "base": "Square Meter",
        "units": {
            "Square Meter":     1,
            "Square Kilometer": 1_000_000,
            "Square Centimeter":0.0001,
            "Square Millimeter":1e-6,
            "Square Mile":      2_589_988.11,
            "Square Yard":      0.836127,
            "Square Foot":      0.092903,
            "Square Inch":      0.00064516,
            "Acre":             4_046.86,
            "Hectare":          10_000,
        }
    },
    "Speed": {
        "base": "Meter/Second",
        "units": {
            "Meter/Second":     1,
            "Kilometer/Hour":   0.277778,
            "Mile/Hour":        0.44704,
            "Knot":             0.514444,
            "Foot/Second":      0.3048,
            "Mach":             343,
        }
    },
    "Time": {
        "base": "Second",
        "units": {
            "Second":       1,
            "Millisecond":  0.001,
            "Microsecond":  1e-6,
            "Nanosecond":   1e-9,
            "Minute":       60,
            "Hour":         3_600,
            "Day":          86_400,
            "Week":         604_800,
            "Month":        2_629_746,
            "Year":         31_556_952,
            "Decade":       315_569_520,
            "Century":      3_155_695_200,
        }
    },
    "Digital Storage": {
        "base": "Byte",
        "units": {
            "Bit":          0.125,
            "Byte":         1,
            "Kilobyte":     1_024,
            "Megabyte":     1_048_576,
            "Gigabyte":     1_073_741_824,
            "Terabyte":     1_099_511_627_776,
            "Petabyte":     1_125_899_906_842_624,
            "Kibibyte":     1_024,
            "Mebibyte":     1_048_576,
            "Gibibyte":     1_073_741_824,
        }
    },
    "Pressure": {
        "base": "Pascal",
        "units": {
            "Pascal":       1,
            "Kilopascal":   1_000,
            "Megapascal":   1_000_000,
            "Bar":          100_000,
            "Millibar":     100,
            "PSI":          6_894.76,
            "Atmosphere":   101_325,
            "Torr":         133.322,
            "mmHg":         133.322,
        }
    },
    "Energy": {
        "base": "Joule",
        "units": {
            "Joule":        1,
            "Kilojoule":    1_000,
            "Megajoule":    1_000_000,
            "Calorie":      4.184,
            "Kilocalorie":  4_184,
            "Watt-hour":    3_600,
            "Kilowatt-hour":3_600_000,
            "Electron Volt":1.602e-19,
            "BTU":          1_055.06,
            "Foot-pound":   1.35582,
        }
    },
    "Power": {
        "base": "Watt",
        "units": {
            "Watt":             1,
            "Kilowatt":         1_000,
            "Megawatt":         1_000_000,
            "Horsepower":       745.7,
            "BTU/Hour":         0.29307,
            "Foot-pound/Min":   0.0225970,
        }
    },
    "Angle": {
        "base": "Degree",
        "units": {
            "Degree":       1,
            "Radian":       180 / math.pi,
            "Gradian":      0.9,
            "Arcminute":    1 / 60,
            "Arcsecond":    1 / 3600,
            "Milliradian":  180 / (math.pi * 1000),
            "Turn":         360,
        }
    },
    "Frequency": {
        "base": "Hertz",
        "units": {
            "Hertz":        1,
            "Kilohertz":    1_000,
            "Megahertz":    1_000_000,
            "Gigahertz":    1_000_000_000,
            "RPM":          1 / 60,
        }
    },
    "Fuel Economy": {
        "base": "km/L",
        "units": {
            "km/L":             1,
            "L/100km":          "special",  # handled via formula
            "Miles per Gallon": 0.425144,
            "Miles per Liter":  1.60934,
        }
    },
}


# ─────────────────────────────────────────────────────────────
#  CORE CONVERSION ENGINE
# ─────────────────────────────────────────────────────────────
def to_celsius(value: float, unit: str) -> float:
    """Convert any temperature unit → Celsius (base)."""
    if unit == "Celsius":
        return value
    elif unit == "Fahrenheit":
        return (value - 32) * 5 / 9
    elif unit == "Kelvin":
        return value - 273.15
    elif unit == "Rankine":
        return (value - 491.67) * 5 / 9
    raise ValueError(f"Unknown temperature unit: {unit}")


def from_celsius(value: float, unit: str) -> float:
    """Convert Celsius (base) → any temperature unit."""
    if unit == "Celsius":
        return value
    elif unit == "Fahrenheit":
        return value * 9 / 5 + 32
    elif unit == "Kelvin":
        return value + 273.15
    elif unit == "Rankine":
        return (value + 273.15) * 9 / 5
    raise ValueError(f"Unknown temperature unit: {unit}")


def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """
    Master conversion function.
    Algorithm:
      1. Convert input → base unit
      2. Convert base unit → target unit
    """
    cat = CATEGORIES[category]

    # ── Temperature (non-linear) ─────────────────────────────
    if category == "Temperature":
        base_value = to_celsius(value, from_unit)
        return from_celsius(base_value, to_unit)

    # ── Fuel Economy special case ────────────────────────────
    if category == "Fuel Economy":
        units = cat["units"]
        if from_unit == "L/100km":
            # Convert L/100km → km/L first
            km_l = 100 / value if value != 0 else float("inf")
        else:
            km_l = value * units[from_unit]          # → base (km/L)

        if to_unit == "L/100km":
            return 100 / km_l if km_l != 0 else float("inf")
        else:
            return km_l / units[to_unit]

    # ── Standard linear conversion ───────────────────────────
    units = cat["units"]
    base_value = value * units[from_unit]            # step 1 → base
    return base_value / units[to_unit]               # step 2 → target


# ─────────────────────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────────────────────
BG          = "#0f1117"
SURFACE     = "#1a1d27"
CARD        = "#21253a"
ACCENT      = "#6c63ff"
ACCENT2     = "#a78bfa"
TEXT        = "#e2e8f0"
TEXT_MUTED  = "#94a3b8"
SUCCESS     = "#10b981"
ERROR       = "#ef4444"
BORDER      = "#2d3148"
HOVER       = "#2e3350"


# ─────────────────────────────────────────────────────────────
#  GUI APPLICATION
# ─────────────────────────────────────────────────────────────
class UnitConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Universal Unit Converter")
        self.geometry("900x680")
        self.resizable(True, True)
        self.configure(bg=BG)
        self.minsize(750, 580)

        self._history: list[str] = []
        self._selected_category = tk.StringVar(value=list(CATEGORIES.keys())[0])
        self._from_unit = tk.StringVar()
        self._to_unit   = tk.StringVar()
        self._input_val = tk.StringVar()
        self._result    = tk.StringVar(value="—")

        self._build_ui()
        self._on_category_change()

    # ── UI Builder ───────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        self._build_converter_panel(body)
        self._build_history_panel(body)

    def _build_header(self):
        hdr = tk.Frame(self, bg=ACCENT, height=4)
        hdr.pack(fill="x")

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(18, 10))

        tk.Label(top, text="⚡ Unit Converter", font=("Segoe UI", 22, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        tk.Label(top, text="Base-Unit Algorithm  •  13 Categories  •  100+ Units",
                 font=("Segoe UI", 9), bg=BG, fg=TEXT_MUTED).pack(side="left", padx=16, pady=6)

    def _build_converter_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE, bd=0, relief="flat")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=4)
        panel.columnconfigure(0, weight=1)

        # ── Category selector ─────────────────────────────
        tk.Label(panel, text="CATEGORY", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(20, 4))

        cat_frame = tk.Frame(panel, bg=SURFACE)
        cat_frame.pack(fill="x", padx=20)

        self._cat_buttons = {}
        cats = list(CATEGORIES.keys())
        for i, cat in enumerate(cats):
            btn = tk.Button(
                cat_frame, text=cat,
                font=("Segoe UI", 8), bd=0, relief="flat", cursor="hand2",
                padx=10, pady=5,
                command=lambda c=cat: self._select_category(c)
            )
            btn.grid(row=i // 4, column=i % 4, padx=3, pady=3, sticky="ew")
            cat_frame.columnconfigure(i % 4, weight=1)
            self._cat_buttons[cat] = btn

        self._refresh_cat_buttons()

        # ── Input row ─────────────────────────────────────
        sep = tk.Frame(panel, bg=BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=16)

        tk.Label(panel, text="FROM", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 4))

        from_row = tk.Frame(panel, bg=SURFACE)
        from_row.pack(fill="x", padx=20)
        from_row.columnconfigure(0, weight=2)
        from_row.columnconfigure(1, weight=1)

        self._input_entry = tk.Entry(
            from_row, textvariable=self._input_val,
            font=("Segoe UI", 18), bg=CARD, fg=TEXT,
            insertbackground=ACCENT2, relief="flat",
            bd=0, highlightthickness=2,
            highlightbackground=BORDER, highlightcolor=ACCENT
        )
        self._input_entry.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 8))
        self._input_entry.bind("<KeyRelease>", lambda e: self._do_convert())

        self._from_combo = ttk.Combobox(
            from_row, textvariable=self._from_unit,
            font=("Segoe UI", 11), state="readonly"
        )
        self._from_combo.grid(row=0, column=1, sticky="ew", ipady=6)
        self._from_combo.bind("<<ComboboxSelected>>", lambda e: self._do_convert())

        # ── Swap button ───────────────────────────────────
        swap_btn = tk.Button(
            panel, text="⇅  Swap Units", font=("Segoe UI", 10),
            bg=CARD, fg=ACCENT2, activebackground=HOVER, activeforeground=ACCENT2,
            relief="flat", cursor="hand2", bd=0, padx=14, pady=8,
            command=self._swap_units
        )
        swap_btn.pack(pady=12)

        # ── To row ────────────────────────────────────────
        tk.Label(panel, text="TO", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 4))

        to_row = tk.Frame(panel, bg=SURFACE)
        to_row.pack(fill="x", padx=20)
        to_row.columnconfigure(0, weight=2)
        to_row.columnconfigure(1, weight=1)

        self._result_label = tk.Label(
            to_row, textvariable=self._result,
            font=("Segoe UI", 18, "bold"), bg=CARD, fg=SUCCESS,
            anchor="w", relief="flat", bd=0, padx=12,
        )
        self._result_label.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 8))

        self._to_combo = ttk.Combobox(
            to_row, textvariable=self._to_unit,
            font=("Segoe UI", 11), state="readonly"
        )
        self._to_combo.grid(row=0, column=1, sticky="ew", ipady=6)
        self._to_combo.bind("<<ComboboxSelected>>", lambda e: self._do_convert())

        # ── Formula label ─────────────────────────────────
        self._formula_var = tk.StringVar(value="")
        tk.Label(panel, textvariable=self._formula_var,
                 font=("Segoe UI", 9, "italic"), bg=SURFACE, fg=TEXT_MUTED
                 ).pack(anchor="w", padx=20, pady=(10, 4))

        # ── Copy button ───────────────────────────────────
        copy_btn = tk.Button(
            panel, text="📋  Copy Result", font=("Segoe UI", 10),
            bg=ACCENT, fg="white", activebackground=ACCENT2, activeforeground="white",
            relief="flat", cursor="hand2", bd=0, padx=18, pady=9,
            command=self._copy_result
        )
        copy_btn.pack(pady=(8, 20))

        self._style_combos()

    def _build_history_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE)
        panel.grid(row=0, column=1, sticky="nsew", pady=4)

        tk.Label(panel, text="HISTORY", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", padx=16, pady=(20, 8))

        list_frame = tk.Frame(panel, bg=SURFACE)
        list_frame.pack(fill="both", expand=True, padx=16)

        scrollbar = tk.Scrollbar(list_frame, bg=SURFACE, troughcolor=SURFACE,
                                 activebackground=ACCENT, relief="flat")
        scrollbar.pack(side="right", fill="y")

        self._history_box = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            font=("Segoe UI", 9), bg=CARD, fg=TEXT,
            selectbackground=ACCENT, selectforeground="white",
            relief="flat", bd=0, activestyle="none",
            highlightthickness=0
        )
        self._history_box.pack(fill="both", expand=True)
        scrollbar.config(command=self._history_box.yview)

        clear_btn = tk.Button(
            panel, text="🗑  Clear History", font=("Segoe UI", 9),
            bg=CARD, fg=ERROR, activebackground=HOVER, activeforeground=ERROR,
            relief="flat", cursor="hand2", bd=0, padx=12, pady=6,
            command=self._clear_history
        )
        clear_btn.pack(pady=(8, 16))

    def _style_combos(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=CARD,
                        background=CARD,
                        foreground=TEXT,
                        arrowcolor=ACCENT2,
                        borderwidth=0,
                        relief="flat",
                        selectbackground=ACCENT,
                        selectforeground="white")
        style.map("TCombobox",
                  fieldbackground=[("readonly", CARD)],
                  selectbackground=[("readonly", ACCENT)],
                  selectforeground=[("readonly", "white")])

    # ── Category Selection ───────────────────────────────────
    def _select_category(self, cat: str):
        self._selected_category.set(cat)
        self._on_category_change()
        self._refresh_cat_buttons()

    def _refresh_cat_buttons(self):
        current = self._selected_category.get()
        for cat, btn in self._cat_buttons.items():
            if cat == current:
                btn.configure(bg=ACCENT, fg="white")
            else:
                btn.configure(bg=CARD, fg=TEXT_MUTED,
                              activebackground=HOVER, activeforeground=TEXT)

    def _on_category_change(self):
        cat = self._selected_category.get()
        units = list(CATEGORIES[cat]["units"].keys())
        self._from_combo["values"] = units
        self._to_combo["values"]   = units
        self._from_unit.set(units[0])
        self._to_unit.set(units[1] if len(units) > 1 else units[0])
        self._do_convert()

    # ── Conversion ───────────────────────────────────────────
    def _do_convert(self):
        raw = self._input_val.get().strip()
        if not raw:
            self._result.set("—")
            self._formula_var.set("")
            return
        try:
            value = float(raw)
        except ValueError:
            self._result.set("Invalid input")
            self._result_label.configure(fg=ERROR)
            return

        from_u = self._from_unit.get()
        to_u   = self._to_unit.get()
        cat    = self._selected_category.get()

        try:
            result = convert(value, from_u, to_u, cat)
        except Exception as e:
            self._result.set(f"Error: {e}")
            self._result_label.configure(fg=ERROR)
            return

        # Format output
        if abs(result) >= 1e9 or (abs(result) < 1e-4 and result != 0):
            formatted = f"{result:.6e}"
        elif result == int(result) and abs(result) < 1e9:
            formatted = f"{int(result):,}"
        else:
            formatted = f"{result:,.8f}".rstrip("0").rstrip(".")

        self._result.set(formatted)
        self._result_label.configure(fg=SUCCESS)

        formula = f"{value} {from_u}  =  {formatted} {to_u}"
        self._formula_var.set(formula)

        if from_u != to_u:
            entry = formula
            if not self._history or self._history[-1] != entry:
                self._history.append(entry)
                self._history_box.insert(0, f"  {entry}")
                if self._history_box.size() > 50:
                    self._history_box.delete("end")

    def _swap_units(self):
        f, t = self._from_unit.get(), self._to_unit.get()
        self._from_unit.set(t)
        self._to_unit.set(f)
        # also swap input/result if result is numeric
        res = self._result.get().replace(",", "")
        try:
            float(res)
            self._input_val.set(res)
        except ValueError:
            pass
        self._do_convert()

    def _copy_result(self):
        self.clipboard_clear()
        self.clipboard_append(self._result.get())
        self.update()
        messagebox.showinfo("Copied", f'Result "{self._result.get()}" copied to clipboard!',
                            parent=self)

    def _clear_history(self):
        self._history.clear()
        self._history_box.delete(0, "end")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = UnitConverterApp()
    app.mainloop()
