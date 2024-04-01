import pandas as pd

# Load the CSV file
df = pd.read_csv('rawdata.csv')

# Filter the DataFrame to keep only first occurrence of each unique docket ID
unique_df = df.drop_duplicates(subset='assigned_to_id')

# Total Cases Over Time by Year
unique_df['entry_date_filed'] = pd.to_datetime(unique_df['entry_date_filed'], errors='coerce', utc=True)
unique_df['year'] = unique_df['entry_date_filed'].dt.year
df_filtered = unique_df[(unique_df['year'] >= 2015) & (unique_df['year'] <= 2024)]
cases_per_year = df_filtered['year'].value_counts().sort_index()

# Court Location of Cases for 2023
court_location_counts_2023 = unique_df[unique_df['year'] == 2023]['court'].value_counts()

# Total Court Location Counts (Since Tracking Began)
court_location_counts_total = unique_df['court'].value_counts()

# Nature of Suit of Cases for 2023
nature_of_suit_2023 = unique_df[unique_df['year'] == 2023]['suitNature'].value_counts()

# Nature of Suit (Total Since Tracking Began)
nature_of_suit_total = unique_df['suitNature'].value_counts()

# Ongoing vs Finished Cases
unique_df['case_status'] = unique_df['dateTerminated'].apply(lambda x: 'Finished' if pd.notnull(x) else 'Ongoing')
case_status_counts = unique_df['case_status'].value_counts()

# Save summary results to an Excel file
with pd.ExcelWriter('ai_court_cases_summary.xlsx') as writer:
    cases_per_year.to_frame('Total Cases').to_excel(writer, sheet_name='Cases Over Time')
    court_location_counts_2023.to_frame('Count').to_excel(writer, sheet_name='Court Locations 2023')
    court_location_counts_total.to_frame('Total Count').to_excel(writer, sheet_name='Court Locations Total')
    nature_of_suit_2023.to_frame('Count').to_excel(writer, sheet_name='Nature of Suit 2023')
    nature_of_suit_total.to_frame('Total Count').to_excel(writer, sheet_name='Nature of Suit Total')
    case_status_counts.to_frame('Case Status Counts').to_excel(writer, sheet_name='Ongoing vs Finished')
