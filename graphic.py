import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from sqlmodel import Session, select
from models import Conta, engine

def criar_grafico_por_conta(session: Session):
    """Gera um gráfico de barras mostrando o saldo de cada conta e salva como imagem."""

    contas = session.exec(select(Conta)).all()

    if not contas:
        print("\n⚠️ Nenhuma conta encontrada para gerar o gráfico.")
        return

    nomes = [conta.banco.value for conta in contas]
    valores = [conta.valor for conta in contas]

    plt.figure(figsize=(8, 5))
    plt.bar(nomes, valores, color="blue")
    plt.xlabel("Banco")
    plt.ylabel("Saldo (R$)")
    plt.title("Saldo por Conta")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como imagem
    plt.savefig("grafico_saldo.png")  
    print("\n📊 Gráfico salvo como 'grafico_saldo.png'. Abra o arquivo para visualizar.")
