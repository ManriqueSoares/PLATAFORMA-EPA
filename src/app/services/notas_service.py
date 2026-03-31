import csv
from pathlib import Path


NOTAS_CSV_PATH = Path(__file__).resolve().parents[2] / "storage" / "data" / "notas.csv"
NOTAS_CSV_COLUMNS = ["CP", "RESP", "NOTA"]


def _normalizar_cp(valor):
    return str(valor).replace("Notas CP:", "", 1).strip()


def adicionar_nota_csv(titulo, usuario, conteudo):
    nova_linha = {"CP": _normalizar_cp(titulo), "RESP": usuario, "NOTA": conteudo}

    NOTAS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    arquivo_tem_conteudo = NOTAS_CSV_PATH.exists() and NOTAS_CSV_PATH.stat().st_size > 0

    with NOTAS_CSV_PATH.open("a", encoding="utf-8", newline="") as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=NOTAS_CSV_COLUMNS, delimiter=";")
        if not arquivo_tem_conteudo:
            writer.writeheader()
        writer.writerow(nova_linha)

        