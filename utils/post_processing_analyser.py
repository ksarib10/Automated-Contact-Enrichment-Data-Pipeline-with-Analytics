import pandas as pd
import re

def clean_and_analyze_final_excel(input_file, output_file="Output\\final_cleaned.xlsx"):

    df = pd.read_excel(input_file)
    
    # Counting Needs Payment rows
    needs_payment_count = (df['status'].str.strip().str.lower() == 'needs payment').sum()
    
    # Counting Success rows
    success_count = (df['status'].str.strip().str.lower() == 'success').sum()
    
    # Remove "Needs Payment" rows
    df_cleaned = df[df['status'].str.strip().str.lower() != 'needs payment']

    # Phone: remove first digit if length == 11
    df_cleaned['phone'] = df_cleaned['phone'].astype(str).str.strip()
    df_cleaned['phone'] = [p[1:] if len(p) == 11 and p.isdigit() else p for p in df_cleaned['phone']]

    # CNIC: remove last 2 chars if contains ".0"
    df_cleaned['cnic'] = df_cleaned['cnic'].astype(str).str.strip()
    df_cleaned['cnic'] = [c[:-2] if ".0" in c else c for c in df_cleaned['cnic']]
    df_cleaned['cnic'] = [c if len(re.sub(r'\D', '', c)) == 13 else "Not Available" for c in df_cleaned['cnic']]

    # Name: keep only alphabets & spaces
    df_cleaned['name'] = df_cleaned['name'].astype(str)
    df_cleaned['name'] = [re.sub(r'[^A-Za-z\s]', '', n).strip() for n in df_cleaned['name']]

    # Address: replace junk values with "Not Available"
    junk_addresses = ['no record', 'record not found', 'nan', 'none', '?']
    df_cleaned['address'] = ["Not Available" if str(a).strip().lower() in junk_addresses else a for a in df_cleaned['address']]

    # Sort by name
    df_cleaned = df_cleaned.sort_values(by='name')

    print("The data is cleaned and sorted, stored as 'final_cleaned.xlsx' in Output folder.")
    
    # Calculating ratio and insights
    total_rows = len(df)
    ratio = f"{success_count}:{needs_payment_count}" if needs_payment_count > 0 else "All Success"
    success_rate = (success_count / total_rows) * 100
    fail_rate = (needs_payment_count / total_rows) * 100
    
    insights = {
        "Total contacts processed": total_rows,
        "Successful contacts": success_count,
        "Needs Payment contacts": needs_payment_count,
        "Success to Needs Payment ratio": ratio,
        "Success rate (%)": round(success_rate, 2),
        "Failure rate (%)": round(fail_rate, 2)
    }
    
    # Print insights (or return them)
    print("\n--- Data Insights ---")
    for k, v in insights.items():
        print(f"{k}: {v}")
        
    # Saved cleaned file
    df_cleaned.to_excel(output_file, index=False)
    
