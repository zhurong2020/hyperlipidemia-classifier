def classify_hyperlipidemia(ldl_c, tc, hdl_c, tg):
    """
    Classify hyperlipidemia levels based on ASCVD risk guidelines.
    
    Parameters:
    ldl_c (float): LDL cholesterol level in mmol/L
    tc (float): Total cholesterol level in mmol/L
    hdl_c (float): HDL cholesterol level in mmol/L
    tg (float): Triglycerides level in mmol/L
    
    Returns:
    str: Classification of hyperlipidemia level
    """
    if ldl_c >= 4.1:
        return "High Risk: LDL-C is elevated."
    elif 3.4 <= ldl_c < 4.1:
        return "Moderate Risk: LDL-C is borderline high."
    elif tc >= 6.2:
        return "High Risk: Total cholesterol is elevated."
    elif 5.2 <= tc < 6.2:
        return "Moderate Risk: Total cholesterol is borderline high."
    elif hdl_c < 1.0:
        return "High Risk: Low HDL-C level."
    elif tg >= 2.3:
        return "High Risk: Elevated triglycerides."
    else:
        return "Normal: Lipid levels are within the acceptable range."

def main():
    print("Welcome to the Hyperlipidemia Classifier")
    ldl_c = float(input("Enter LDL cholesterol level (mmol/L): "))
    tc = float(input("Enter Total cholesterol level (mmol/L): "))
    hdl_c = float(input("Enter HDL cholesterol level (mmol/L): "))
    tg = float(input("Enter Triglycerides level (mmol/L): "))

    classification = classify_hyperlipidemia(ldl_c, tc, hdl_c, tg)
    print(f"Classification: {classification}")

if __name__ == "__main__":
    main()