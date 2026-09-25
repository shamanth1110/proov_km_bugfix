analyze.py
# Key findings: km_since_service and avg_daily_km are the strongest breakdown predictors.
# Cars with high unserviced mileage and heavy daily usage break down far more often;
# odometer total and age are nearly identical across both groups and add no signal.
#
# fleet_history.csv has one row per car (120 of them) and a "broke_down" column (1 = it later
# broke down).

import pandas as pd  # type: ignore


def analyze_fleet_risk(csv_file_path: str = "fleet_history.csv") -> pd.DataFrame:  # type: ignore
    """
    Load fleet_history.csv, derive a 0-100 risk score from the columns that
    actually separate breakdowns from non-breakdowns, and print cars ranked
    by risk (highest first).

    Returns the ranked DataFrame so callers can do further work with it.
    """

    # 1. Load data
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"CSV file not found: '{csv_file_path}'. "
            "Make sure fleet_history.csv is in the same folder."
        )

    required_cols = {"car_id", "km_since_service", "avg_daily_km", "load_factor", "broke_down"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing expected columns: {missing}")

    # Coerce numeric columns; drop rows where any value is non-numeric
    numeric_cols = ["km_since_service", "avg_daily_km", "load_factor", "broke_down"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    bad_rows: pd.Series = df[numeric_cols].isna().any(axis=1)  # type: ignore
    if bad_rows.any():
        print(f"Warning: skipping {bad_rows.sum()} row(s) with non-numeric data: "
              f"{df.loc[bad_rows, 'car_id'].tolist()}")
        df = df[~bad_rows].reset_index(drop=True)

    # 2. Score using the three columns that actually separate breakdowns from non-breakdowns
    #
    #   Column            broke_down avg   ok avg   diff
    #   km_since_service   11 677.9         7 261.4  +4 416  <- strongest
    #   avg_daily_km          159.7           131.4    +28.3  <- second
    #   load_factor             0.601           0.506   +0.095 <- moderate
    #   odometer_km         53 448          53 302     +146   <- negligible
    #   age_years               5.89            5.89    -0.00  <- no signal

    def minmax(col: str) -> pd.Series:  # type: ignore
        s = df[col]
        lo, hi = s.min(), s.max()
        if hi == lo:
            return pd.Series([0.0] * len(s), index=s.index, dtype=float)  # type: ignore
        return pd.Series((s - lo) / (hi - lo), dtype=float)  # type: ignore

    w_kss  = 0.70   # km_since_service
    w_adkm = 0.15   # avg_daily_km
    w_lf   = 0.15   # load_factor

    df["risk_score"] = (
        w_kss  * minmax("km_since_service") +
        w_adkm * minmax("avg_daily_km")     +
        w_lf   * minmax("load_factor")
    ) * 100

    df["risk_score"] = df["risk_score"].round(1)

    # 3. Rank by risk, highest first
    cols = ["car_id", "km_since_service", "avg_daily_km", "load_factor", "risk_score", "broke_down"]
    subset: pd.DataFrame = df[cols].copy()  # type: ignore
    ranked = subset.sort_values("risk_score", ascending=False)

    # 4. Print report
    print("=" * 65)
    print("FLEET RISK REPORT  --  ranked highest risk first")
    print("=" * 65)
    print(f"{'Car':<12} {'km_since_svc':>12} {'avg_daily_km':>13} {'load':>6} {'risk':>6} {'broke?':>7}")
    print("-" * 65)

    for _, row in ranked.iterrows():
        flag = "  [BROKE]" if row["broke_down"] == 1 else ""
        print(
            f"{row['car_id']:<12}"
            f"{int(row['km_since_service']):>12,}"
            f"{int(row['avg_daily_km']):>13,}"
            f"{row['load_factor']:>6.2f}"
            f"{row['risk_score']:>6.1f}"
            f"{flag}"
        )

    print("=" * 65)
    total     = len(ranked)
    broke     = int(ranked["broke_down"].sum())
    top20     = ranked.head(20)
    top20_hit = int(top20["broke_down"].sum())
    print(f"\nFleet size : {total} cars   |   Historical breakdowns: {broke}")
    if broke > 0:
        print(f"Top-20 by risk captures {top20_hit}/{broke} known breakdowns "
              f"({top20_hit / broke * 100:.0f} %).")
    else:
        print("No historical breakdowns recorded in this dataset.")

    return ranked


if __name__ == "__main__":
    analyze_fleet_risk("fleet_history.csv")
