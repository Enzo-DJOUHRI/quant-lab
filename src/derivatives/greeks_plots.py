import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


CALL_COLOR = "#2176ae"
PUT_COLOR = "#c14924"
REFERENCE_COLOR = "#6c757d"
GREEK_COLOR = "#2a9d8f"


def _validate_series_lengths(x_values, **series):
    if len(x_values) == 0:
        raise ValueError("x_values must not be empty")

    for name, values in series.items():
        if len(values) != len(x_values):
            raise ValueError(f"{name} must have the same length as x_values")


def _style_axis(ax):
    ax.grid(alpha=0.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _create_two_panel_figure():
    return plt.subplots(
        2,
        1,
        figsize=(11, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [1.15, 1]},
    )


def _plot_option_prices(ax, x_values, call_prices, put_prices, reference_value, reference_label):
    ax.plot(
        x_values,
        call_prices,
        color=CALL_COLOR,
        linewidth=2,
        label="Call price",
    )
    ax.plot(
        x_values,
        put_prices,
        color=PUT_COLOR,
        linewidth=2,
        label="Put price",
    )
    ax.axvline(
        reference_value,
        color=REFERENCE_COLOR,
        linestyle="--",
        linewidth=1.5,
        label=reference_label,
    )
    ax.set_ylabel("Option price")
    ax.legend()


def _add_reference_line(ax, reference_value):
    ax.axvline(
        reference_value,
        color=REFERENCE_COLOR,
        linestyle="--",
        linewidth=1.5,
    )


def plot_delta_vs_spot(spot_values, call_prices, put_prices, call_deltas, put_deltas, parameters):
    _validate_series_lengths(
        spot_values,
        call_prices=call_prices,
        put_prices=put_prices,
        call_deltas=call_deltas,
        put_deltas=put_deltas,
    )

    strike = parameters["K"]

    fig, (price_ax, delta_ax) = _create_two_panel_figure()

    _plot_option_prices(
        price_ax,
        spot_values,
        call_prices,
        put_prices,
        strike,
        f"Strike K={strike:g}",
    )

    delta_ax.plot(
        spot_values,
        call_deltas,
        color=CALL_COLOR,
        linewidth=2,
        label="Call Delta",
    )
    delta_ax.plot(
        spot_values,
        put_deltas,
        color=PUT_COLOR,
        linewidth=2,
        label="Put Delta",
    )
    _add_reference_line(delta_ax, strike)
    delta_ax.axhline(0, color=REFERENCE_COLOR, linewidth=1, alpha=0.6)
    delta_ax.set_xlabel("Spot price S")
    delta_ax.set_ylabel("Delta")
    delta_ax.set_ylim(-1.05, 1.05)
    delta_ax.legend()

    for ax in (price_ax, delta_ax):
        _style_axis(ax)

    fig.suptitle(
        "Black-Scholes-Merton: Price and Delta Across Spot",
        fontsize=16,
        fontweight="bold",
    )
    price_ax.set_title(
        (
            f"K={parameters['K']:g} | T={parameters['T']:g} years | "
            f"sigma={parameters['sigma']:.0%} | r={parameters['r']:.1%} | "
            f"q={parameters['q']:.1%}"
        ),
        fontsize=10,
        color="#495057",
        pad=12,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))

    return fig


def plot_gamma_vs_spot(spot_values, call_deltas, put_deltas, gamma_values, parameters):
    _validate_series_lengths(
        spot_values,
        call_deltas=call_deltas,
        put_deltas=put_deltas,
        gamma_values=gamma_values,
    )

    strike = parameters["K"]

    fig, (delta_ax, gamma_ax) = _create_two_panel_figure()

    delta_ax.plot(
        spot_values,
        call_deltas,
        color=CALL_COLOR,
        linewidth=2,
        label="Call Delta",
    )
    delta_ax.plot(
        spot_values,
        put_deltas,
        color=PUT_COLOR,
        linewidth=2,
        label="Put Delta",
    )
    delta_ax.axvline(
        strike,
        color=REFERENCE_COLOR,
        linestyle="--",
        linewidth=1.5,
        label=f"Strike K={strike:g}",
    )
    delta_ax.axhline(0, color=REFERENCE_COLOR, linewidth=1, alpha=0.6)
    delta_ax.set_ylabel("Delta")
    delta_ax.set_ylim(-1.05, 1.05)
    delta_ax.legend()

    gamma_ax.plot(
        spot_values,
        gamma_values,
        color=GREEK_COLOR,
        linewidth=2,
        label="Call and put Gamma",
    )
    _add_reference_line(gamma_ax, strike)
    gamma_ax.set_xlabel("Spot price S")
    gamma_ax.set_ylabel("Gamma")
    gamma_ax.set_ylim(bottom=0)
    gamma_ax.legend()

    for ax in (delta_ax, gamma_ax):
        _style_axis(ax)

    fig.suptitle(
        "Black-Scholes-Merton: Delta and Gamma Across Spot",
        fontsize=16,
        fontweight="bold",
    )
    delta_ax.set_title(
        (
            f"K={parameters['K']:g} | T={parameters['T']:g} years | "
            f"sigma={parameters['sigma']:.0%} | r={parameters['r']:.1%} | "
            f"q={parameters['q']:.1%}"
        ),
        fontsize=10,
        color="#495057",
        pad=12,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))

    return fig


def plot_vega_vs_volatility(volatility_values, call_prices, put_prices, vega_values, parameters):
    _validate_series_lengths(
        volatility_values,
        call_prices=call_prices,
        put_prices=put_prices,
        vega_values=vega_values,
    )

    reference_volatility = parameters["sigma"]

    fig, (price_ax, vega_ax) = _create_two_panel_figure()

    _plot_option_prices(
        price_ax,
        volatility_values,
        call_prices,
        put_prices,
        reference_volatility,
        f"Reference sigma={reference_volatility:.0%}",
    )

    vega_ax.plot(
        volatility_values,
        vega_values,
        color=GREEK_COLOR,
        linewidth=2,
        label="Call and put Vega",
    )
    _add_reference_line(vega_ax, reference_volatility)
    vega_ax.set_xlabel("Volatility sigma")
    vega_ax.set_ylabel("Vega per 1.00 volatility")
    vega_ax.set_ylim(bottom=0)
    vega_ax.legend()

    for ax in (price_ax, vega_ax):
        ax.xaxis.set_major_formatter(PercentFormatter(1.0))
        _style_axis(ax)

    fig.suptitle(
        "Black-Scholes-Merton: Price and Vega Across Volatility",
        fontsize=16,
        fontweight="bold",
    )
    price_ax.set_title(
        (
            f"S={parameters['S']:g} | K={parameters['K']:g} | "
            f"T={parameters['T']:g} years | r={parameters['r']:.1%} | "
            f"q={parameters['q']:.1%}"
        ),
        fontsize=10,
        color="#495057",
        pad=12,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))

    return fig


def plot_theta_vs_maturity(maturity_values, call_prices, put_prices, call_thetas, put_thetas, parameters):
    _validate_series_lengths(
        maturity_values,
        call_prices=call_prices,
        put_prices=put_prices,
        call_thetas=call_thetas,
        put_thetas=put_thetas,
    )

    reference_maturity = parameters["T"]

    fig, (price_ax, theta_ax) = _create_two_panel_figure()

    _plot_option_prices(
        price_ax,
        maturity_values,
        call_prices,
        put_prices,
        reference_maturity,
        f"Reference T={reference_maturity:g} year",
    )

    theta_ax.plot(
        maturity_values,
        call_thetas,
        color=CALL_COLOR,
        linewidth=2,
        label="Call Theta",
    )
    theta_ax.plot(
        maturity_values,
        put_thetas,
        color=PUT_COLOR,
        linewidth=2,
        label="Put Theta",
    )
    _add_reference_line(theta_ax, reference_maturity)
    theta_ax.axhline(0, color=REFERENCE_COLOR, linewidth=1, alpha=0.6)
    theta_ax.set_xlabel("Remaining maturity T (years)")
    theta_ax.set_ylabel("Annual Theta")
    theta_ax.legend()

    for ax in (price_ax, theta_ax):
        _style_axis(ax)

    fig.suptitle(
        "Black-Scholes-Merton: Price and Theta Across Maturity",
        fontsize=16,
        fontweight="bold",
    )
    price_ax.set_title(
        (
            f"S={parameters['S']:g} | K={parameters['K']:g} | "
            f"sigma={parameters['sigma']:.0%} | r={parameters['r']:.1%} | "
            f"q={parameters['q']:.1%}"
        ),
        fontsize=10,
        color="#495057",
        pad=12,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))

    return fig


def plot_rho_vs_rate(rate_values, call_prices, put_prices, call_rhos, put_rhos, parameters):
    _validate_series_lengths(
        rate_values,
        call_prices=call_prices,
        put_prices=put_prices,
        call_rhos=call_rhos,
        put_rhos=put_rhos,
    )

    reference_rate = parameters["r"]

    fig, (price_ax, rho_ax) = _create_two_panel_figure()

    _plot_option_prices(
        price_ax,
        rate_values,
        call_prices,
        put_prices,
        reference_rate,
        f"Reference r={reference_rate:.1%}",
    )

    rho_ax.plot(
        rate_values,
        call_rhos,
        color=CALL_COLOR,
        linewidth=2,
        label="Call Rho",
    )
    rho_ax.plot(
        rate_values,
        put_rhos,
        color=PUT_COLOR,
        linewidth=2,
        label="Put Rho",
    )
    _add_reference_line(rho_ax, reference_rate)
    rho_ax.axhline(0, color=REFERENCE_COLOR, linewidth=1, alpha=0.6)
    rho_ax.set_xlabel("Continuously compounded rate r")
    rho_ax.set_ylabel("Rho per 1.00 rate")
    rho_ax.legend()

    for ax in (price_ax, rho_ax):
        ax.xaxis.set_major_formatter(PercentFormatter(1.0))
        _style_axis(ax)

    fig.suptitle(
        "Black-Scholes-Merton: Price and Rho Across Rates",
        fontsize=16,
        fontweight="bold",
    )
    price_ax.set_title(
        (
            f"S={parameters['S']:g} | K={parameters['K']:g} | "
            f"T={parameters['T']:g} years | sigma={parameters['sigma']:.0%} | "
            f"q={parameters['q']:.1%}"
        ),
        fontsize=10,
        color="#495057",
        pad=12,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))

    return fig
