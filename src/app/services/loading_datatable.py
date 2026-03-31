import flet as ft
import pandas as pd
import datetime

from app.config.config import configuracoes
from app.services.database.loading_data import run_primeiro_envio
from app.layout.components.widgets import (
    DATATABLE_GERAL,
    ENTRADA_CLIENTE_FILTRO_GERAL,
    ENTRADA_RESPONSAVEL_FILTRO_GERAL,
    RESPONSAVEL_FILTRO_OPCOES,
)


RESPONSAVEL_COLUMNS = ["RESP_CALCULO", "RESP_EBPA", "RESP_EBPM", "RESP_APROVACAO"]


def _parse_filter_date(value):
    if not value:
        return None
    return datetime.datetime.strptime(value, "%d/%m/%Y")


def _normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _format_data_final(value):
    if pd.isna(value) or value in {"", None}:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value)


def _build_rows(df):
    rows = []
    for _, row in df.iterrows():
        if row["CALCULO"] == "Pendente":
            color = ft.Colors.RED_300
        else:
            color = ft.Colors.GREEN_300

        if row["EBPA"] == "Pendente":
            ebpa_color = ft.Colors.RED_300
        else:
            ebpa_color = ft.Colors.GREEN_300
        if row["EBPM"] == "Pendente":
            ebpm_color = ft.Colors.RED_300
        else:
            ebpm_color = ft.Colors.GREEN_300
        if row["APROVACAO"] == "Pendente":
            aprovacao_color = ft.Colors.RED_300
        else:
            aprovacao_color = ft.Colors.GREEN_300
        
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(_normalize_text(row["CP"]))),
                    ft.DataCell(ft.Text(_normalize_text(row["CLIENTE"]))),
                    ft.DataCell(ft.Text(_normalize_text(row["CALCULO"]), color=color)),
                    ft.DataCell(ft.Text(_normalize_text(row["RESP_CALCULO"]))),
                    ft.DataCell(ft.Text(_normalize_text(row["EBPA"]), color=ebpa_color)),
                    ft.DataCell(ft.Text(_normalize_text(row["RESP_EBPA"]))),
                    ft.DataCell(ft.Text(_normalize_text(row["EBPM"]), color=ebpm_color)),
                    ft.DataCell(ft.Text(_normalize_text(row["RESP_EBPM"]))),
                    ft.DataCell(ft.Text(_normalize_text(row["APROVACAO"]), color=aprovacao_color)),
                    ft.DataCell(ft.Text(_normalize_text(row["RESP_APROVACAO"]))),
                    ft.DataCell(ft.Text(_format_data_final(row["DATA_PS"]))),
                    ft.DataCell(
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(text="Add Nota", icon=ft.Icons.NOTIFICATION_ADD),
                                ft.PopupMenuItem(text="Visualizar Notas", icon=ft.Icons.REMOVE_RED_EYE),
                            ]
                        )
                    ),
                ]
            )
        )
    return rows


def _set_datatable_rows(df):
    DATATABLE_GERAL.rows.clear()
    DATATABLE_GERAL.rows.extend(_build_rows(df))
    if DATATABLE_GERAL.page is not None:
        DATATABLE_GERAL.update()


def _apply_filters_to_dataframe(
    df,
    cp_value="",
    cliente_value="",
    responsavel_value="",
    data_inicio_value="",
    data_fim_value="",
):
    filtered_df = df.copy()

    cp_filter = (cp_value or "").strip()
    if cp_filter:
        filtered_df = filtered_df[
            filtered_df["CP"].astype("string").str.contains(cp_filter, case=False, na=False)
        ]

    cliente_filter = (cliente_value or "").strip()
    if cliente_filter:
        filtered_df = filtered_df[
            filtered_df["CLIENTE"].astype("string").str.strip() == cliente_filter
        ]

    responsavel_filter = (responsavel_value or "").strip()
    if responsavel_filter:
        responsavel_mask = pd.Series(False, index=filtered_df.index)
        for column in RESPONSAVEL_COLUMNS:
            responsavel_mask = responsavel_mask | (
                filtered_df[column].astype("string").str.strip() == responsavel_filter
            )
        filtered_df = filtered_df[responsavel_mask]

    data_final = pd.to_datetime(filtered_df["DATA_PS"], format="%d/%m/%Y", errors="coerce")

    data_inicio = _parse_filter_date(data_inicio_value) if data_inicio_value else None
    if data_inicio is not None:
        filtered_df = filtered_df[data_final >= data_inicio]
        data_final = pd.to_datetime(filtered_df["DATA_PS"], format="%d/%m/%Y", errors="coerce")

    data_fim = _parse_filter_date(data_fim_value) if data_fim_value else None
    if data_fim is not None:
        filtered_df = filtered_df[data_final <= data_fim]

    return filtered_df.reset_index(drop=True)


def _build_dropdown_options(values):
    return [ft.dropdown.Option(value) for value in values if value]


def update_filter_options(cp_value="", cliente_value="", responsavel_value="", data_inicio_value="", data_fim_value=""):
    if configuracoes.planilha_geral is None:
        return

    clientes_df = _apply_filters_to_dataframe(
        configuracoes.planilha_geral,
        cp_value=cp_value,
        responsavel_value=responsavel_value,
        data_inicio_value=data_inicio_value,
        data_fim_value=data_fim_value,
    )
    clientes = sorted({_normalize_text(value) for value in clientes_df["CLIENTE"].tolist() if _normalize_text(value)})
    ENTRADA_CLIENTE_FILTRO_GERAL.options = _build_dropdown_options(clientes)

    ENTRADA_RESPONSAVEL_FILTRO_GERAL.options = _build_dropdown_options(RESPONSAVEL_FILTRO_OPCOES)

    if ENTRADA_CLIENTE_FILTRO_GERAL.page is not None:
        ENTRADA_CLIENTE_FILTRO_GERAL.update()
    if ENTRADA_RESPONSAVEL_FILTRO_GERAL.page is not None:
        ENTRADA_RESPONSAVEL_FILTRO_GERAL.update()


def apply_filters_primeiro_envio(cp_value="", cliente_value="", responsavel_value="", data_inicio_value="", data_fim_value=""):
    if configuracoes.planilha_geral is None:
        return

    filtered_df = _apply_filters_to_dataframe(
        configuracoes.planilha_geral,
        cp_value=cp_value,
        cliente_value=cliente_value,
        responsavel_value=responsavel_value,
        data_inicio_value=data_inicio_value,
        data_fim_value=data_fim_value,
    )
    _set_datatable_rows(filtered_df)
    update_filter_options(
        cp_value=cp_value,
        cliente_value=cliente_value,
        responsavel_value=responsavel_value,
        data_inicio_value=data_inicio_value,
        data_fim_value=data_fim_value,
    )

def run_datatable_primeiro_envio():
    run_primeiro_envio()
    if configuracoes.planilha_geral is not None:
        _set_datatable_rows(configuracoes.planilha_geral)
        print("Primeiro envio carregado com sucesso.")
        print(configuracoes.planilha_geral.head())
        update_filter_options()
    else:
        print("Primeiro envio ainda não carregado.")
