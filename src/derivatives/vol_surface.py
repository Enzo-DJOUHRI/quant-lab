from src.derivatives import vol_smile


def build_synthetic_surface(
    S, strikes, maturities, r,
    atm_volatility, reference_maturity,
    option_type="call", q=0,
    slope=0.0, curvature=0.0,
    maturity_slope=0.0,
):
    surface_rows = []

    for T in maturities:
        atm_volatility_at_maturity = (
            atm_volatility + maturity_slope * (T - reference_maturity)
        )
        smile_rows = vol_smile.build_synthetic_smile(
            S,
            strikes,
            T,
            r,
            atm_volatility_at_maturity,
            option_type=option_type,
            q=q,
            slope=slope,
            curvature=curvature,
        )

        for row in smile_rows:
            row["maturity"] = T
            surface_rows.append(row)

    return surface_rows
