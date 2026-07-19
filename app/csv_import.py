TEXT_COLUMN_ALIASES = ("Tweet Text", "text", "tweet", "full_text")


def _normalized_header(value: object) -> str:
    return " ".join(str(value).strip().lower().replace("_", " ").split())


def extract_posts(dataframe) -> list[str]:
    normalized_columns = {
        _normalized_header(column): column for column in dataframe.columns
    }
    text_column = next(
        (
            normalized_columns[_normalized_header(alias)]
            for alias in TEXT_COLUMN_ALIASES
            if _normalized_header(alias) in normalized_columns
        ),
        None,
    )
    if text_column is None:
        raise ValueError(
            "CSV must include a Tweet Text, text, tweet, or full_text column."
        )

    return [
        text
        for value in dataframe[text_column].dropna().tolist()
        if (text := str(value).strip())
    ]
