from sqlmodel import Session
from src.models.models import Conta, engine,Bancos, Status

def inserir_conta(banco: Bancos, status: Status, valor: float):
    with Session(engine) as session:
        nova_conta = Conta(banco=banco, status=status, valor=valor)
        session.add(nova_conta)
        session.commit()
        session.refresh(nova_conta)
        print(f"Conta inserida com ID {nova_conta.id}")

if __name__ == "__main__":
    inserir_conta(Bancos.ITAU, Status.ATIVO, 1500.75)
    inserir_conta(Bancos.NUBANK, Status.ATIVO, 200.00)
    inserir_conta(Bancos.INTER, Status.ATIVO, 123.54)
    inserir_conta(Bancos.ITAU, Status.ATIVO, 11.25)
