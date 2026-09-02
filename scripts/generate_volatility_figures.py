from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.derivatives import vol_smile, vol_surface
from src.derivatives.volatility_plots import (
    plot_smile_slices,
    plot_synthetic_smile,
    plot_synthetic_surface,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = (
    PROJECT_ROOT
    / "reports"
    / "pricing"
    / "figures"
    / "volatility"
    / "synthetic"
)


def _save_figure(fig, file_name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / file_name

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    return output_path


def main():
    S = 100
    r = 0.03
    q = 0.03
    atm_volatility = 0.20
    reference_maturity = 1.0
    maturities = [0.25, 0.50, 0.75, 1.00, 1.50, 2.00]

    log_moneyness_values = np.linspace(-0.30, 0.30, 31)
    strikes = S * np.exp(log_moneyness_values)

    symmetric_smile_rows = vol_smile.build_synthetic_smile(
        S, strikes, reference_maturity, r, atm_volatility,
        option_type="call", q=q, slope=0.0, curvature=0.45,
    )

    symmetric_smile_figure = plot_synthetic_smile(
        symmetric_smile_rows,
        "Synthetic Symmetric Smile: True vs Recovered IV",
    )

    symmetric_smile_path = _save_figure(
        symmetric_smile_figure,
        "symmetric_smile.png",
    )
    skew_slope = -0.10
    skew_curvature = 0.20

    equity_skew_rows = vol_smile.build_synthetic_smile(
        S, strikes, reference_maturity, r, atm_volatility,
        option_type="call", q=q, slope=skew_slope, curvature=skew_curvature,
    )

    equity_skew_figure = plot_synthetic_smile(
        equity_skew_rows,
        "Synthetic Equity Skew: True vs Recovered IV",
    )

    equity_skew_path = _save_figure(
        equity_skew_figure,
        "equity_skew.png",
    )
    equity_skew_surface_rows = vol_surface.build_synthetic_surface(
        S, strikes, maturities, r, atm_volatility, reference_maturity,
        option_type="call", q=q, slope=skew_slope, curvature=skew_curvature,
        maturity_slope=0.025,
    )

    equity_skew_slices_figure = plot_smile_slices(
        equity_skew_surface_rows,
        "Synthetic Equity Skew by Maturity",
    )
    equity_skew_surface_figure = plot_synthetic_surface(
        equity_skew_surface_rows,
        "Synthetic Equity Skew Surface",
    )

    equity_skew_slices_path = _save_figure(
        equity_skew_slices_figure,
        "equity_skew_slices.png",
    )

    equity_skew_surface_path = _save_figure(
        equity_skew_surface_figure,
        "equity_skew_surface.png",
    )
    print(f"Symmetric smile figure saved to: {symmetric_smile_path}")
    print(f"Equity skew figure saved to: {equity_skew_path}")
    print(f"Equity skew slices figure saved to: {equity_skew_slices_path}")
    print(f"Equity skew surface figure saved to: {equity_skew_surface_path}")


if __name__ == "__main__":
    main()
