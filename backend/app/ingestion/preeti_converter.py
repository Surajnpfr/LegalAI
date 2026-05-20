def preeti_to_unicode(text: str) -> str:
    replacements = {
        "g]kfnsf]": "नेपालको",
        ";+ljwfg": "संविधान",
        "k|:tfjgf": "प्रस्तावना",
        "efu": "भाग",
        "wf/f": "धारा",
        "sfg\"g": "कानून",
        "df}lns": "मौलिक",
        "xs": "हक",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text