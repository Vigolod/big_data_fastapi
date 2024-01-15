def get_kds(columns, values):
    kds = [f"{val:.2f}" for (col, val) in zip(columns, values) if col in ["KDL", "KDH", "KDE", "KD"]]
    return kds

