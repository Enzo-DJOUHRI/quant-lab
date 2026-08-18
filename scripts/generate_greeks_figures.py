from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.derivatives import black_scholes, greeks
from src.derivatives.greeks_plots import (
    plot_delta_vs_spot,
    plot_gamma_vs_spot,
    plot_rho_vs_rate,
    plot_theta_vs_maturity,
    plot_vega_vs_volatility,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "reports" / "pricing" / "figures" / "greeks"


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
    parameters = {
        "S": 100,
        "K": 100,
        "T": 1,
        "sigma": 0.20,
        "r": 0.05,
        "q": 0.02,
    }
    spot_values = np.linspace(50, 150, 201)

    call_prices = [
        black_scholes.bsm_call(
            S=spot,
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for spot in spot_values
    ]
    put_prices = [
        black_scholes.bsm_put(
            S=spot,
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for spot in spot_values
    ]
    call_deltas = [
        greeks.bsm_call_delta(
            S=spot,
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for spot in spot_values
    ]
    put_deltas = [
        greeks.bsm_put_delta(
            S=spot,
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for spot in spot_values
    ]
    gamma_values = [
        greeks.bsm_gamma(
            S=spot,
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for spot in spot_values
    ]

    delta_figure = plot_delta_vs_spot(
        spot_values,
        call_prices,
        put_prices,
        call_deltas,
        put_deltas,
        parameters,
    )
    delta_path = _save_figure(delta_figure, "delta_vs_spot.png")

    gamma_figure = plot_gamma_vs_spot(
        spot_values,
        call_deltas,
        put_deltas,
        gamma_values,
        parameters,
    )
    gamma_path = _save_figure(gamma_figure, "gamma_vs_spot.png")

    volatility_values = np.linspace(0.05, 0.80, 151)
    call_prices_by_volatility = [
        black_scholes.bsm_call(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=volatility,
            r=parameters["r"],
            q=parameters["q"],
        )
        for volatility in volatility_values
    ]
    put_prices_by_volatility = [
        black_scholes.bsm_put(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=volatility,
            r=parameters["r"],
            q=parameters["q"],
        )
        for volatility in volatility_values
    ]
    vega_values = [
        greeks.bsm_vega(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=volatility,
            r=parameters["r"],
            q=parameters["q"],
        )
        for volatility in volatility_values
    ]

    vega_figure = plot_vega_vs_volatility(
        volatility_values,
        call_prices_by_volatility,
        put_prices_by_volatility,
        vega_values,
        parameters,
    )
    vega_path = _save_figure(vega_figure, "vega_vs_volatility.png")

    maturity_values = np.linspace(0.02, 2.00, 200)
    call_prices_by_maturity = [
        black_scholes.bsm_call(
            S=parameters["S"],
            K=parameters["K"],
            T=maturity,
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for maturity in maturity_values
    ]
    put_prices_by_maturity = [
        black_scholes.bsm_put(
            S=parameters["S"],
            K=parameters["K"],
            T=maturity,
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for maturity in maturity_values
    ]
    call_thetas = [
        greeks.bsm_call_theta(
            S=parameters["S"],
            K=parameters["K"],
            T=maturity,
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for maturity in maturity_values
    ]
    put_thetas = [
        greeks.bsm_put_theta(
            S=parameters["S"],
            K=parameters["K"],
            T=maturity,
            sigma=parameters["sigma"],
            r=parameters["r"],
            q=parameters["q"],
        )
        for maturity in maturity_values
    ]

    theta_figure = plot_theta_vs_maturity(
        maturity_values,
        call_prices_by_maturity,
        put_prices_by_maturity,
        call_thetas,
        put_thetas,
        parameters,
    )
    theta_path = _save_figure(theta_figure, "theta_vs_maturity.png")

    rate_values = np.linspace(-0.05, 0.15, 201)
    call_prices_by_rate = [
        black_scholes.bsm_call(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=rate,
            q=parameters["q"],
        )
        for rate in rate_values
    ]
    put_prices_by_rate = [
        black_scholes.bsm_put(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=rate,
            q=parameters["q"],
        )
        for rate in rate_values
    ]
    call_rhos = [
        greeks.bsm_call_rho(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=rate,
            q=parameters["q"],
        )
        for rate in rate_values
    ]
    put_rhos = [
        greeks.bsm_put_rho(
            S=parameters["S"],
            K=parameters["K"],
            T=parameters["T"],
            sigma=parameters["sigma"],
            r=rate,
            q=parameters["q"],
        )
        for rate in rate_values
    ]

    rho_figure = plot_rho_vs_rate(
        rate_values,
        call_prices_by_rate,
        put_prices_by_rate,
        call_rhos,
        put_rhos,
        parameters,
    )
    rho_path = _save_figure(rho_figure, "rho_vs_rate.png")

    print(f"Delta figure saved to: {delta_path}")
    print(f"Gamma figure saved to: {gamma_path}")
    print(f"Vega figure saved to: {vega_path}")
    print(f"Theta figure saved to: {theta_path}")
    print(f"Rho figure saved to: {rho_path}")


if __name__ == "__main__":
    main()
