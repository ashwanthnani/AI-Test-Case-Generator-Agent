import pandas as pd
from io import StringIO

def to_csv(cases):
    out = StringIO()
    pd.DataFrame(cases).to_csv(out, index=False)
    return out.getvalue().encode("utf-8-sig")
