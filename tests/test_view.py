import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from src.controllers.view import criar_conta, listar_contas, desativar_conta, transferir_saldo, movimentar_dinheiro, total_contas
from src.models.models import Conta, Historico, Bancos, Status, Tipos, engine

# Criar um banco de dados em memória para testes
test_engine = create_engine("sqlite:///:memory:", echo=True)

def setup_db():
    """Cria o banco de dados de teste."""
    SQLModel.metadata.create_all(test_engine)

@pytest.fixture
def session():
    """Configura uma sessão de teste com banco em memória."""
    setup_db()
    with Session(test_engine) as session:
        yield session

@pytest.fixture
def conta_teste(session):
    """Cria uma conta de teste."""
    conta = Conta(banco=Bancos.NUBANK, status=Status.ATIVO, valor=1000)
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

# Teste para criar conta
def test_criar_conta(session):
    conta = Conta(banco=Bancos.ITAU, status=Status.ATIVO, valor=500)
    nova_conta = criar_conta(session, conta)
    assert nova_conta is not None
    assert nova_conta.banco == Bancos.ITAU
    assert nova_conta.valor == 500

# Teste para listar contas
def test_listar_contas(session, conta_teste):
    contas = session.exec(select(Conta)).all()
    assert len(contas) >= 1  # Verifica que pelo menos uma conta foi criada
    assert any(conta.banco == Bancos.NUBANK for conta in contas)  # Verifica se a conta esperada está presente

# Teste para desativar conta
def test_desativar_conta(session, conta_teste):
    conta_teste.valor = 0  # Para poder desativar
    session.commit()
    desativar_conta(session, conta_teste.id)
    session.refresh(conta_teste)
    assert conta_teste.status == Status.INATIVO

# Teste para transferir saldo
def test_transferir_saldo(session, conta_teste):
    conta_destino = Conta(banco=Bancos.INTER, status=Status.ATIVO, valor=500)
    session.add(conta_destino)
    session.commit()
    session.refresh(conta_destino)

    transferir_saldo(session, conta_teste.id, conta_destino.id, 200)
    session.refresh(conta_teste)
    session.refresh(conta_destino)

    assert conta_teste.valor == 800
    assert conta_destino.valor == 700

# Teste para movimentação de dinheiro
def test_movimentar_dinheiro(session, conta_teste):
    data_atual = datetime.today().date()  # Garante que seja um objeto date válido
    historico = Historico(conta_id=conta_teste.id, tipo=Tipos.ENTRADA, valor=300, data=data_atual)
    
    movimentar_dinheiro(session, historico)
    
    session.refresh(conta_teste)
    assert conta_teste.valor == 1300

# Teste para total de contas
def test_total_contas(session, conta_teste):
    # Criar uma nova conta no banco de testes
    conta_extra = Conta(banco=Bancos.SANTANDER, status=Status.ATIVO, valor=500)
    session.add(conta_extra)
    session.commit()

    # Recalcular o total
    total = total_contas(session)
    
    # O total esperado é a soma das contas criadas no teste
    expected_total = conta_teste.valor + conta_extra.valor  

    assert total == expected_total
