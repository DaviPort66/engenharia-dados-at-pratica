import os
import psycopg2
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "universidade"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options="-c search_path=universidade,public",
    )


def executar(sql, params=None, fetch=False):
    """Executa um comando. Retorna as linhas (fetch=True) ou o nº de linhas afetadas.
    Traduz os erros do Postgres em mensagens claras (ValueError)."""
    conn = conectar()
    try:
        with conn, conn.cursor() as cur:  # 'with conn' faz commit/rollback
            cur.execute(sql, params)
            return cur.fetchall() if fetch else cur.rowcount
    except errors.UniqueViolation:
        raise ValueError("Violação de chave/unicidade: já existe um registro com esse valor.")
    except errors.ForeignKeyViolation:
        raise ValueError("Violação de integridade referencial: o registro referenciado não existe "
                         "ou ainda é usado por outra tabela.")
    except errors.NotNullViolation:
        raise ValueError("Campo obrigatório (NOT NULL) não informado.")
    except errors.CheckViolation:
        raise ValueError("Valor viola uma restrição CHECK da tabela.")
    except (errors.InvalidTextRepresentation, errors.InvalidDatetimeFormat,
            errors.NumericValueOutOfRange, errors.StringDataRightTruncation):
        raise ValueError("Valor inválido para o domínio do campo (formato, tamanho ou opção do enum).")
    except psycopg2.Error as e:
        raise ValueError(f"Erro no banco: {e.pgerror or e}")
    finally:
        conn.close()
