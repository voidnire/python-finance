from sqlmodel import Session, select
from models import Conta, Historico, Status, Tipos

def criar_conta(session: Session, conta: Conta):
    statement = select(Conta).where(Conta.banco == conta.banco.value)
    results = session.exec(statement).all()
    if results:
        print("Já existe uma conta nesse banco!")
        return None
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

def listar_contas(session: Session):
    contas = session.exec(select(Conta)).all()
    if not contas:
        print("Nenhuma conta encontrada no banco de dados.")
    else:
        for conta in contas:
            print(f"ID: {conta.id}, Banco: {conta.banco}, Valor: {conta.valor}")

def desativar_conta(session: Session, id: int):
    statement = select(Conta).where(Conta.id == id)
    conta = session.exec(statement).first()
    if not conta:
        raise ValueError("Conta não encontrada.")
    if conta.valor > 0:
        raise ValueError("Essa conta ainda possui saldo, não é possível desativar.")
    conta.status = Status.INATIVO
    session.commit()

def transferir_saldo(session: Session, id_conta_saida: int, id_conta_entrada: int, valor: float):
    conta_saida = session.exec(select(Conta).where(Conta.id == id_conta_saida)).first()
    conta_entrada = session.exec(select(Conta).where(Conta.id == id_conta_entrada)).first()

    if not conta_saida or not conta_entrada:
        raise ValueError("Uma das contas não foi encontrada.")

    if conta_saida.valor < valor:
        raise ValueError("Saldo insuficiente")

    conta_saida.valor -= valor
    conta_entrada.valor += valor
    session.commit()

def movimentar_dinheiro(session: Session, historico: Historico):
    conta = session.exec(select(Conta).where(Conta.id == historico.conta_id)).first()
    if not conta:
        raise ValueError("Conta não encontrada.")

    if historico.tipo == Tipos.ENTRADA:
        conta.valor += historico.valor
    else:
        if conta.valor < historico.valor:
            raise ValueError("Saldo insuficiente")
        conta.valor -= historico.valor

    session.add(historico)
    session.commit()
    return historico

def total_contas(session: Session):
    contas = session.exec(select(Conta)).all()
    return sum(conta.valor for conta in contas) if contas else 0.0
