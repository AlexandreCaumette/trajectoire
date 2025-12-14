import polars as pl

SCHEMA_CONTRIBUTIONS = {
    "Label": pl.String,
    "Catégorie": pl.String,
    "Score": pl.Float32,
    "Date": pl.Date,
}

SCHEMA_REFERENTIEL = {
    "Label": pl.String,
    "Catégorie": pl.String,
    "Score": pl.Float32,
    "Echéance": pl.Date,
    "Fréquence": pl.String,
}
