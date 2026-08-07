from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


DECISION_COLORS = {
    "exercise": "#c14924",
    "continue": "#2176ae",
    "maturity": "#6c757d",
}

def _prepare_output_path(output_path):
    output_path = Path(output_path)

    if not output_path.is_absolute():
        project_root = Path(__file__).resolve().parents[2]
        output_path = project_root / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    return output_path


def plot_american_put_tree(tree, output_path):
    levels = tree["levels"]

    output_path = _prepare_output_path(output_path)

    fig, ax = plt.subplots(figsize=(12, 7))

    strike = tree["parameters"]["K"]

    # 1. Draw branches between non-terminal nodes.
    for level in levels[:-1]:
        for node in level:
            i = node["i"]
            j = node["j"]

            x = i
            # Vertical position equals up moves minus down moves.
            y = 2 * j - i
            next_x = i + 1

            ax.plot(
                [x, next_x],
                [y, y - 1],
                color="#adb5bd",
                linewidth=1.2,
                zorder=1,
            )
            ax.plot(
                [x, next_x],
                [y, y + 1],
                color="#adb5bd",
                linewidth=1.2,
                zorder=1,
            )

    # 2. Draw every node, including maturity.
    for level in levels:
        for node in level:
            i = node["i"]
            j = node["j"]

            x = i
            y = 2 * j - i

            decision = node["decision"]
            color = DECISION_COLORS[decision]

            ax.scatter(
                x,
                y,
                s=2600,
                color=color,
                edgecolors="white",
                linewidth=2,
                zorder=2,
            )

            label = (
                f"S={node['spot']:.2f}\n"
                f"V={node['option_value']:.2f}\n"
                f"{decision}"
            )

            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                color="white",
                fontsize=8,
                fontweight="bold",
                zorder=3,
            )

    n_steps = len(levels) - 1

    ax.set_title(
        (
            "American Put CRR Tree\n"
            f"Strike: K={strike:.2f} | "
            f"Initial option value: {tree['price']:.4f}"
        ),
        fontsize=16,
        pad=20,
    )
    ax.set_xlabel("Time step")
    ax.set_xticks(range(len(levels)))
    ax.set_yticks([])

    ax.set_xlim(-0.8, n_steps + 0.8)
    ax.set_ylim(-n_steps - 0.8, n_steps + 0.8)

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    return output_path


def plot_crr_convergence(n_steps_values, crr_prices, bsm_price, output_path):
    if not n_steps_values:
        raise ValueError("n_steps_values must not be empty")

    if len(n_steps_values) != len(crr_prices):
        raise ValueError(
            "n_steps_values and crr_prices must have the same length"
        )

    output_path = _prepare_output_path(output_path)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        n_steps_values,
        crr_prices,
        color="#2176ae",
        linewidth=1.4,
        label="CRR call price",
    )

    ax.axhline(
        y=bsm_price,
        color="#c14924",
        linestyle="--",
        linewidth=2,
        label=f"BSM benchmark: {bsm_price:.4f}",
    )

    ax.set_title(
        "European Call: CRR Convergence to BSM",
        fontsize=16,
        pad=20,
    )
    ax.set_xlabel("Number of time steps")
    ax.set_ylabel("Option price")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    return output_path
