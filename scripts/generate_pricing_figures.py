from math import log

from src.derivatives import binomial, black_scholes
from src.derivatives.binomial_plots import (
    plot_american_put_tree,
    plot_crr_convergence,
)


def main():
    tree = binomial.build_crr_american_put_tree(
        S=100,
        K=120,
        T=2,
        sigma=log(1.25),
        r=log(1.05),
        n_steps=2,
    )

    tree_path = plot_american_put_tree(
        tree,
        "reports/pricing/figures/american_put_tree.png",
    )

    n_steps_values = list(range(1, 201))

    crr_prices = [
        binomial.crr_european_call(
            S=42,
            K=40,
            T=0.5,
            sigma=0.20,
            r=0.10,
            n_steps=n_steps,
        )
        for n_steps in n_steps_values
    ]

    bsm_price = black_scholes.bsm_call(
        S=42,
        K=40,
        T=0.5,
        sigma=0.20,
        r=0.10,
    )

    convergence_path = plot_crr_convergence(
        n_steps_values,
        crr_prices,
        bsm_price,
        "reports/pricing/figures/crr_bsm_convergence.png",
    )

    print(f"American put price: {tree['price']:.6f}")
    print(f"BSM call price: {bsm_price:.6f}")
    print(f"CRR call price (N={n_steps_values[-1]}): {crr_prices[-1]:.6f}")
    print(f"CRR absolute error: {abs(crr_prices[-1] - bsm_price):.6f}")
    print(f"Tree figure saved to: {tree_path}")
    print(f"Convergence figure saved to: {convergence_path}")


if __name__ == "__main__":
    main()