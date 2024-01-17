def get_kds_and_wr(columns, values):
    col_val_dict = dict(zip(columns, values))
    kd_dict = {}
    for k, v in col_val_dict.items():
        if k.startswith("KD"):
            suffix = "" if k == "KD" else k[-1]
            deaths = col_val_dict["TD" + suffix]
            kills = col_val_dict['TK' + suffix]
            if deaths == 0:
                kd_dict[k] = f">={kills}"
            elif kills == 0:
                kd_dict[k] = f"<={(1 / deaths):.2f}"
            else:
                kd_dict[k] = f"{v:.2f}"
    kds = [kd_dict[col] for col in ["KDL", "KDH", "KDE", "KD"]]
    if col_val_dict["WINS"] == 0 and col_val_dict["LOSSES"] == 0:
        wr = "UNK"
    else:
        wr = f"{col_val_dict['WIN_RATE']:.2f}"
    return kds, wr

