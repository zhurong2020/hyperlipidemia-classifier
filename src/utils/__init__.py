def validate_lipid_levels(ldl, tc, hdl):
    if not (0 <= ldl <= 10) or not (0 <= tc <= 10) or not (0 <= hdl <= 10):
        raise ValueError("Lipid levels must be between 0 and 10 mmol/L")

def convert_to_mmol_per_liter(value, unit):
    if unit == 'mg/dL':
        return value / 38.67
    elif unit == 'mmol/L':
        return value
    else:
        raise ValueError("Unsupported unit. Use 'mg/dL' or 'mmol/L'")