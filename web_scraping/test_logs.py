import pandas as pd

# Test single team
url = 'https://www.sports-reference.com/cbb/schools/southern-california/men/2025-gamelogs.html'

try:
    tables = pd.read_html(url)
    print(f"✓ Found {len(tables)} tables")
    print(f"✓ First table has {len(tables[0])} rows")
    print("\nColumns:", tables[0].columns.tolist())
    print("\nFirst row:", tables[0].iloc[0])
except Exception as e:
    print(f"✗ Error: {e}")