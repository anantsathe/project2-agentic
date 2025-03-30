import pandas as pd
from datetime import datetime
from fastapi import UploadFile
from io import BytesIO

def solve_ga_5_q1(file: UploadFile) -> dict:
    try:
        print(f"🔹 Processing file: {file.filename}")  # Debugging log
        
        # Load Excel file
        content = file.file.read()
        print(f"🔹 File size: {len(content)} bytes")  # Debugging log
        
        df = pd.read_excel(BytesIO(content))
        print("🔹 Excel loaded successfully. Columns:", df.columns.tolist())  # Debugging log
        
        # Trim spaces from Customer Name and Country
        df["Customer Name"] = df["Customer Name"].str.strip()
        df["Country"] = df["Country"].str.strip()

        # Standardize country names
        country_map = {"USA": "US", "U.S.A": "US", "U.K": "UK", "Fra": "FR", "Bra": "BR", "Ind": "IN"}
        df["Country"] = df["Country"].replace(country_map)

        # Standardize date format
        def parse_date(date):
            for fmt in ("%m-%d-%Y", "%Y/%m/%d", "%d-%m-%Y"):
                try:
                    return datetime.strptime(str(date), fmt).date()
                except ValueError:
                    continue
            return None

        df["Date"] = df["Date"].apply(parse_date)
        df = df.dropna(subset=["Date"])

        # Extract product name before "/"
        df["Product/Code"] = df["Product/Code"].astype(str).str.split("/").str[0].str.strip().str.upper()

        # Clean Sales and Cost columns
        df["Sales"] = df["Sales"].astype(str).str.replace("USD", "").str.strip().astype(float)
        df["Cost"] = df["Cost"].astype(str).str.replace("USD", "").str.strip()
        df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
        df.loc[df["Cost"].isna(), "Cost"] = df["Sales"] * 0.5

        # Apply Filters
        filter_date = datetime(2022, 2, 11).date()
        filtered_df = df[(df["Date"] <= filter_date) & (df["Product/Code"] == "GAMMA") & (df["Country"] == "IN")]

        print(f"🔹 Filtered rows count: {len(filtered_df)}")  # Debugging log

        # Calculate Total Margin
        total_sales = filtered_df["Sales"].sum()
        total_cost = filtered_df["Cost"].sum()
        total_margin = (total_sales - total_cost) / total_sales if total_sales > 0 else 0

        print(f"🔹 Total Sales: {total_sales:.2f}, Total Cost: {total_cost:.2f}, Total Margin: {total_margin:.4f}")  # Debugging log

        return {"answer": f"{total_margin:.4f}"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Debugging log
        return {"answer": f"Error: {str(e)}"}
