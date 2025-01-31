def classify_hyperlipidemia(ldl_c, tc, hdl_c, tg):
    """
    Classify hyperlipidemia levels based on ASCVD risk guidelines.
    
    Parameters:
    ldl_c (float): Low-density lipoprotein cholesterol level in mmol/L.
    tc (float): Total cholesterol level in mmol/L.
    hdl_c (float): High-density lipoprotein cholesterol level in mmol/L.
    tg (float): Triglycerides level in mmol/L.

    Returns:
    str: Classification of hyperlipidemia level.
    """
    if ldl_c >= 4.0:
        return "High LDL-C: Consider lifestyle changes and medication."
    elif ldl_c >= 3.0:
        return "Borderline high LDL-C: Monitor and consider lifestyle changes."
    
    if tc >= 6.2:
        return "High Total Cholesterol: Consider lifestyle changes and medication."
    elif tc >= 5.2:
        return "Borderline high Total Cholesterol: Monitor and consider lifestyle changes."
    
    if hdl_c < 1.0:
        return "Low HDL-C: Consider lifestyle changes."
    
    if tg >= 2.3:
        return "High Triglycerides: Consider lifestyle changes and medication."
    elif tg >= 1.7:
        return "Borderline high Triglycerides: Monitor and consider lifestyle changes."
    
    return "Normal lipid levels: Maintain a healthy lifestyle."