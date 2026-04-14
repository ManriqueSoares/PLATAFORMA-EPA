import flet as ft
import pandas as pd
import datetime
from pathlib import Path

from app.config.config import configuracoes
from app.data.data import data_base
from app.layout.components.widgets import (
    DATATABLE_GERAL,
    ENTRADA_CLIENTE_FILTRO_GERAL,
    ENTRADA_RESPONSAVEL_FILTRO_GERAL,
    RESPONSAVEL_FILTRO_OPCOES,
)

from app.layout.raiz import raiz


RESPONSAVEL_COLUMNS = ["RESP_CALCULO", "RESP_EBPA", "RESP_EBPM", "RESP_APROVACAO"]
NOTAS_CSV_PATH = Path(__file__).resolve().parents[2] / "storage" / "data" / "notas.csv"


def _normalize_cp_to_int(value):
    if pd.isna(value):
        return None

    value_text = str(value).strip()
    if not value_text:
        return None

    try:
        return int(float(value_text))
    except (TypeError, ValueError):
        return None


def _buscar_linhas_notas_por_cp(cp):
    cp_normalizado = _normalize_cp_to_int(cp)

    if cp_normalizado is None or not NOTAS_CSV_PATH.exists():
        return pd.DataFrame()

    try:
        notas_df = pd.read_csv(NOTAS_CSV_PATH, sep=";", dtype=str)
    except pd.errors.ParserError:
        notas_df = pd.read_csv(
            NOTAS_CSV_PATH,
            sep=";",
            dtype=str,
            engine="python",
            on_bad_lines="skip",
        )

    if "CP" not in notas_df.columns:
        return pd.DataFrame()

    notas_df["CP"] = (
        notas_df["CP"]
        .astype("string")
        .str.strip()
        .apply(_normalize_cp_to_int)
        .astype("Int64")
    )

    print(f"CP BUSCADA: {cp_normalizado}")
    print(f"Colunas CP no CSV: {notas_df['CP'].dropna().astype(int).tolist()}")

    df_filtrado = notas_df.loc[notas_df["CP"] == cp_normalizado].copy()
    df_filtrado["LINHA_ARQUIVO"] = df_filtrado.index + 2

    print(f"Linhas encontradas no CSV: {df_filtrado['LINHA_ARQUIVO'].tolist()}")
    return df_filtrado

def func_open_janela_notas(e, cp):
    from app.layout.pages.home_page import JANELA_NOTAS
    from app.layout.components.widgets import TITULO_JANELA_NOTAS, TAB_NOTAS

    cp_normalizado = _normalize_cp_to_int(cp)
    df_cp_encontradas = _buscar_linhas_notas_por_cp(cp)
    linhas_arquivo = df_cp_encontradas["LINHA_ARQUIVO"].astype(int).tolist() if not df_cp_encontradas.empty else []
    linhas_formatadas = ",".join(str(linha) for linha in linhas_arquivo)
    TITULO_JANELA_NOTAS.value = f"Notas CP: {cp}"
    TAB_NOTAS.tabs.clear()
    num_tab = 0
    for i in range(df_cp_encontradas.shape[0]):
        TAB_NOTAS.selected_index = 0
        TAB_NOTAS.tabs.append(
            ft.Tab(
                text=f"Nota {i+1}",
                content=ft.Container(
                    expand=True,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900)),
                    content=ft.TextField(
                        value=df_cp_encontradas.iloc[i]["NOTA"],
                        expand=True,
                        multiline=True,
                        read_only=True,
                        border_color="transparent",
                        content_padding=ft.padding.all(10),
                    )
                )
            )
        )
        num_tab += 1

    

    raiz.controls.append(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        JANELA_NOTAS()
                    ]
                )
            ]
        )
    )
    raiz.update()
    return df_cp_encontradas


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
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_300, on_click=lambda e, cp=row["CP"]: func_open_janela_notas(e, cp))
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
    if data_base.planilha_geral is None:
        return

    clientes_df = _apply_filters_to_dataframe(
        data_base.planilha_geral,
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
    if data_base.planilha_geral is None:
        return

    filtered_df = _apply_filters_to_dataframe(
        data_base.planilha_geral,
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
    from app.services.database.loading_data import run_primeiro_envio
    run_primeiro_envio()
    if data_base.planilha_geral is not None:
        _set_datatable_rows(data_base.planilha_geral)
        print("Primeiro envio carregado com sucesso.")
        print(data_base.planilha_geral.head())
        update_filter_options()
    else:
        print("Primeiro envio ainda não carregado.")


def funcs_datatable_atividades_em_aberto(e, cp, func):
    match func:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass

def run_datatable_atividades_em_aberto():

    from app.layout.components.widgets import DATATABLE_ATIVIDADES_EM_ABERTO
    from app.services.database.loading_data import run_atividades_em_aberto
    df_pendentes, df_em_andamento, df_finalizado = run_atividades_em_aberto()
    data_base.em_aberto_user = df_pendentes
    data_base.em_andamento_user = df_em_andamento
    data_base.concluido_user = df_finalizado

    ## Carrega datatable de atividades em aberto
    for i in data_base.em_aberto_user.index:
        DATATABLE_ATIVIDADES_EM_ABERTO.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[14]]))),
                    ft.DataCell(ft.Text(str(data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[16]]))),
                    ft.DataCell(ft.Text(str(data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[4]]))),
                    ft.DataCell(ft.Text(str(data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[2]]))),    
                    ft.DataCell(ft.Text(str(data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[10]]))),
                    ft.DataCell(
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(text="Em Andamento", icon=ft.Icons.PLAY_ARROW, on_click=lambda e, cp=data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[14]], func=1: funcs_datatable_atividades_em_aberto(e, cp, func)),
                                ft.PopupMenuItem(text="Direcionar Estudo", icon=ft.Icons.FORWARD, on_click=lambda e, cp=data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[14]], func=2: funcs_datatable_atividades_em_aberto(e, cp, func)),
                                ft.PopupMenuItem(text="Sinalizar Problema", icon=ft.Icons.WARNING, on_click=lambda e, cp=data_base.em_aberto_user.loc[i, data_base.em_aberto_user.columns[14]], func=3: funcs_datatable_atividades_em_aberto(e, cp, func))
                            ]
                        )
                    )
                ]
            )
        )
    raiz.update()