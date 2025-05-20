import pandas as pd
from io import BytesIO

def generate_excel(data):
    rows = []
    for blog in data:
        rows.append({
            "Website": blog["website"],
            "Title": blog["title"],
            "Content": blog["content"],
            "Link": blog["link"],
            "Published": blog["metadata"].get("published", "N/A"),
            "VADER Pos": blog["analysis"]["vader"]["pos"],
            "VADER Neu": blog["analysis"]["vader"]["neu"],
            "VADER Neg": blog["analysis"]["vader"]["neg"],
            "Empath Positive": blog["analysis"]["empath"].get("positive_emotion", 0),
            "Empath Negative": blog["analysis"]["empath"].get("negative_emotion", 0),
            "LLM Summary": blog["analysis"]["llm"]
        })
    df = pd.DataFrame(rows)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Blog Analysis")
    output.seek(0)
    return output

def split_and_generate_excels(data, prefix, chunk_size=10, analyzed=False):
    files = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        rows = []
        for blog in chunk:
            base = {
                "Website": blog["website"],
                "Title": blog["title"],
                "Content": blog["content"],
                "Link": blog["link"],
                "Published": blog["metadata"].get("published", "N/A"),
            }
            if analyzed:
                base.update({
                    "VADER Pos": blog["analysis"]["vader"]["pos"],
                    "VADER Neu": blog["analysis"]["vader"]["neu"],
                    "VADER Neg": blog["analysis"]["vader"]["neg"],
                    "Empath Positive": blog["analysis"]["empath"].get("positive_emotion", 0),
                    "Empath Negative": blog["analysis"]["empath"].get("negative_emotion", 0),
                    "LLM Summary": blog["analysis"]["llm"]
                })
            rows.append(base)

        df = pd.DataFrame(rows)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Blogs")
        output.seek(0)
        filename = f"{prefix}_part_{(i // chunk_size) + 1}.xlsx"
        files.append((filename, output))
    return files
