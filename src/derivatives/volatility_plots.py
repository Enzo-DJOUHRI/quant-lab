import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def plot_synthetic_smile(smile_rows, title="Synthetic Smile: True vs Recovered Implied Volatility"):
    if not smile_rows:
        raise ValueError("smile_rows must not be empty")

    sorted_rows = sorted(
        smile_rows,
        key=lambda row: row["log_moneyness"],
    )

    log_moneyness_values = [row["log_moneyness"] for row in sorted_rows]
    true_volatilities = [row["true_volatility"] for row in sorted_rows]
    implied_volatilities = [row["implied_volatility"] for row in sorted_rows]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        log_moneyness_values,
        true_volatilities,
        color="#1d6a73",
        linewidth=2.5,
        label="True volatility",
    )

    ax.scatter(
        log_moneyness_values,
        implied_volatilities,
        color="#e07a2d",
        edgecolor="white",
        linewidth=0.8,
        s=45,
        zorder=3,
        label="Recovered implied volatility",
    )

    ax.axvline(
        0.0,
        color="#6c757d",
        linestyle="--",
        linewidth=1.5,
        label="ATM forward",
    )

    ax.set_xlabel("Log-forward moneyness k = log(K / F0)")
    ax.set_ylabel("Volatility")
    ax.set_title(title)

    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.grid(alpha=0.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend()

    fig.tight_layout()

    return fig


def plot_smile_slices(surface_rows, title="Synthetic Implied Volatility Smiles by Maturity"):
    if not surface_rows:
        raise ValueError("surface_rows must not be empty")

    rows_by_maturity = {}

    for row in surface_rows:
        maturity = row["maturity"]

        if maturity not in rows_by_maturity:
            rows_by_maturity[maturity] = []

        rows_by_maturity[maturity].append(row)

    fig, ax = plt.subplots(figsize=(10, 6))

    for maturity in sorted(rows_by_maturity):
        maturity_rows = rows_by_maturity[maturity]

        sorted_maturity_rows = sorted(
            maturity_rows,
            key=lambda row: row["log_moneyness"],
        )

        log_moneyness_values = [
            row["log_moneyness"]
            for row in sorted_maturity_rows
        ]
        implied_volatilities = [
            row["implied_volatility"]
            for row in sorted_maturity_rows
        ]

        ax.plot(
            log_moneyness_values,
            implied_volatilities,
            marker="o",
            linewidth=2,
            markersize=5,
            label=f"T = {maturity:g} years",
        )

    ax.axvline(
        0.0,
        color="#6c757d",
        linestyle="--",
        linewidth=1.5,
        label="ATM forward",
    )

    ax.set_xlabel("Log-forward moneyness k = log(K / F0)")
    ax.set_ylabel("Implied volatility")
    ax.set_title(title)

    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.grid(alpha=0.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend()

    fig.tight_layout()

    return fig


def plot_synthetic_surface(surface_rows, title="Synthetic Implied Volatility Surface"):
    if not surface_rows:
        raise ValueError("surface_rows must not be empty")

    log_moneyness_values = [row["log_moneyness"] for row in surface_rows]
    maturity_values = [row["maturity"] for row in surface_rows]
    implied_volatilities = [row["implied_volatility"] for row in surface_rows]

    fig = plt.figure(figsize=(15, 6))

    surface_ax = fig.add_subplot(
        1,
        2,
        1,
        projection="3d",
    )

    heatmap_ax = fig.add_subplot(
        1,
        2,
        2,
    )

    volatility_min = min(implied_volatilities)
    volatility_max = max(implied_volatilities)

    surface_ax.plot_trisurf(
        log_moneyness_values,
        maturity_values,
        implied_volatilities,
        cmap="cividis",
        vmin=volatility_min,
        vmax=volatility_max,
        linewidth=0.25,
        antialiased=True,
    )

    heatmap = heatmap_ax.tricontourf(
        log_moneyness_values,
        maturity_values,
        implied_volatilities,
        levels=20,
        cmap="cividis",
        vmin=volatility_min,
        vmax=volatility_max,
    )

    surface_ax.set_xlabel("Log-forward moneyness")
    surface_ax.set_ylabel("Maturity T (years)")
    surface_ax.set_zlabel("Implied volatility")
    surface_ax.set_title("3D Volatility Surface")
    surface_ax.zaxis.set_major_formatter(PercentFormatter(1.0))
    surface_ax.view_init(elev=25, azim=-130)

    heatmap_ax.axvline(
        0.0,
        color="white",
        linestyle="--",
        linewidth=1.5,
        alpha=0.85,
    )

    heatmap_ax.scatter(
        log_moneyness_values,
        maturity_values,
        c=implied_volatilities,
        cmap="cividis",
        vmin=volatility_min,
        vmax=volatility_max,
        s=20,
        edgecolor="white",
        linewidth=0.4,
        zorder=3,
    )

    heatmap_ax.set_xlabel("Log-forward moneyness")
    heatmap_ax.set_ylabel("Maturity T (years)")
    heatmap_ax.set_title("Implied Volatility Heatmap")

    fig.suptitle(
        title,
        fontsize=16,
        fontweight="bold",
    )

    fig.subplots_adjust(
        left=0.05,
        right=0.88,
        bottom=0.12,
        top=0.84,
        wspace=0.28,
    )

    colorbar_ax = fig.add_axes([
        0.91,
        0.20,
        0.015,
        0.56,
    ])

    colorbar = fig.colorbar(
        heatmap,
        cax=colorbar_ax,
    )

    colorbar.set_label(
        "Implied volatility",
        labelpad=12,
    )
    colorbar.ax.yaxis.set_major_formatter(PercentFormatter(1.0))

    return fig
