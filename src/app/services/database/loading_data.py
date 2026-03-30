import re
import unicodedata

import pandas as pd
import xlwings as xw
import os

from app.config.config import configuracoes
import datetime


RESP_COLUMNS_BY_POSITION = {
    0: "RESP_CALCULO",
    1: "RESP_EBPA",
    2: "RESP_SCC",
    3: "RESP_EBPM",
    4: "RESP_APROVACAO",
}
REQUIRED_COLUMNS = [
    "CP",
    "CLIENTE",
    "CALCULO",
    "RESP_CALCULO",
    "EBPA",
    "RESP_EBPA",
    "EBPM",
    "RESP_EBPM",
    "APROVACAO",
    "RESP_APROVACAO",
    "DATA_FINAL",
]


def run_relatorio_ps_weg():
    pasta_relatorio = configuracoes.caminho_banco_relatorio_ps_weg
    today_weekday = datetime.datetime.now().strftime("%A").upper()
    file_path = os.path.join(pasta_relatorio, f"{today_weekday}.xlsx")

    df = pd.read_excel(file_path, sheet_name="1500")
    df = df[df.iloc[:, 6].str.contains("PS ENG Estudo Parte Ati", na=False)]
    return df


def _normalize_header(value):
    text = unicodedata.normalize("NFKD", str(value).strip().upper())
    text = text.encode("ASCII", "ignore").decode("ASCII")
    text = re.sub(r"[^A-Z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def _rename_primeiro_envio_columns(columns):
    renamed_columns = []
    resp_index = 0

    for column in columns:
        normalized = _normalize_header(column)
        normalized_base = re.sub(r"_\d+$", "", normalized)

        if normalized_base in {"RESP", "RESPONSAVEL"}:
            if resp_index in RESP_COLUMNS_BY_POSITION:
                renamed_columns.append(RESP_COLUMNS_BY_POSITION[resp_index])
            else:
                renamed_columns.append(f"RESP_{resp_index + 1}")
            resp_index += 1
        elif normalized_base in {"CLIENTE", "CLEINTE"}:
            renamed_columns.append("CLIENTE")
        elif normalized_base == "CALCULO":
            renamed_columns.append("CALCULO")
        elif normalized_base in {"APROV", "APROVACAO"}:
            renamed_columns.append("APROVACAO")
        elif normalized_base in {"DATA_FINAL", "DATA_FINAL_ENVIO"}:
            renamed_columns.append("DATA_FINAL")
        elif normalized_base in {"DATA_INICIAL", "DATA_INICIAL_ENVIO"}:
            renamed_columns.append("DATA_INICIAL")
        else:
            renamed_columns.append(normalized_base)

    return renamed_columns


def _ensure_required_columns(df):
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df


def _format_primeiro_envio_columns(df):
    df["CP"] = pd.to_numeric(df["CP"], errors="coerce").astype("Int64")

    data_final = pd.to_datetime(df["DATA_FINAL"], errors="coerce")
    df["DATA_FINAL"] = data_final
    df = df.sort_values(by="DATA_FINAL", na_position="last").reset_index(drop=True)
    #df["DATA_FINAL"] = df["DATA_FINAL"].dt.strftime("%d/%m/%Y").fillna("")

    return df

def run_primeiro_envio():

    df = pd.read_excel(
    configuracoes.caminho_banco_dados_programacao,
    sheet_name="PRIMEIRO ENVIO",
    header=7,
    usecols="B:R",
    )
    df.columns = _rename_primeiro_envio_columns(df.columns)
    df = _ensure_required_columns(df)
    df = _format_primeiro_envio_columns(df)
    df_relatorio_weg = run_relatorio_ps_weg()
    df['DATA_PS'] = df['CP'].apply(
        lambda x: df_relatorio_weg[df_relatorio_weg.iloc[:, 14] == x].iloc[0, 10] 
        if any(df_relatorio_weg.iloc[:, 14] == x) else "-"
    )
    configuracoes.planilha_geral = df
    