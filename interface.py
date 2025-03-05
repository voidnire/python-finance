from src.controllers.view import *
from src.services.graphic import criar_grafico_por_conta
from src.models.models import Conta, Historico, Bancos, Tipos, engine
from datetime import datetime,date

class UI:
    def start(self):
        while True:
            print('''
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
            [0] -> Sair
            ''')

            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self._criar_conta()
            elif choice == 2:
                self._desativar_conta()
            elif choice == 3:
                self._transferir_saldo()
            elif choice == 4:
                self._movimentar_dinheiro()
            elif choice == 5:
                self._total_contas()
            elif choice == 6:
                self._filtrar_movimentacoes()
            elif choice == 7:
                self._criar_grafico()
            else:
                break

    def _criar_conta(self):
        print('Digite o nome de algum dos bancos abaixo:')
        for banco in Bancos:
            print(f'---{banco.value}---')

        banco = input().title()
        valor = float(input('Digite o valor atual disponível na conta: '))

        conta = Conta(banco=Bancos(banco), valor=valor)

        with Session(engine) as session:
            criar_conta(session, conta)

    def _desativar_conta(self):
        with Session(engine) as session:
            print('Escolha a conta que deseja desativar.')
            contas = listar_contas(session)

            for i in contas:
                if i.valor == 0:
                    print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

            id_conta = int(input())

            try:
                desativar_conta(session, id_conta)
                print('Conta desativada com sucesso.')
            except ValueError:
                print('Essa conta ainda possui saldo, faça uma transferência.')

    def _transferir_saldo(self):
        with Session(engine) as session:
            contas = listar_contas(session)

            if not contas:  # Verifica se há contas antes de iterar
                print("⚠️ Nenhuma conta disponível para transferência.")
                return

            print("Escolha a conta para retirar o dinheiro:")
            for i in contas:
                print(f"ID: {i.id}, Banco: {i.banco.value}, Valor: R$ {i.valor:,.2f}")

            conta_retirar_id = int(input("\nDigite o ID da conta de origem: "))

            print("Escolha a conta para enviar dinheiro:")
            for i in contas:
                if i.id != conta_retirar_id:
                    print(f"ID: {i.id}, Banco: {i.banco.value}, Valor: R$ {i.valor:,.2f}")

            conta_enviar_id = int(input("\nDigite o ID da conta de destino: "))

            valor = float(input("\nDigite o valor para transferir: R$ "))

            try:
                transferir_saldo(session, conta_retirar_id, conta_enviar_id, valor)
                print("\n✅ Transferência realizada com sucesso!")
            except ValueError as e:
                print(f"\n❌ Erro: {e}")



    def _movimentar_dinheiro(self):
        with Session(engine) as session:
            print('Escolha a conta.')
            contas = listar_contas(session)

            for i in contas:
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

            conta_id = int(input())
            valor = float(input('Digite o valor movimentado: '))

            print('Selecione o tipo da movimentação')
            for tipo in Tipos:
                print(f'---{tipo.value}---')

            tipo = input().title()
            historico = Historico(conta_id=conta_id, tipo=Tipos(tipo), valor=valor, data=date.today())

            movimentar_dinheiro(session, historico)

    def _total_contas(self):
        with Session(engine) as session:
            print("\n" + "="*30)
            print(f" 💰 SALDO TOTAL DAS CONTAS 💰")
            print("="*30)
            print(f" ✅ Saldo disponível: R$ {total_contas(session):,.2f}\n")

        
    def _filtrar_movimentacoes(self):
        with Session(engine) as session:
            data_inicio = input('Digite a data de início (dd/mm/yyyy): ')
            data_fim = input('Digite a data final (dd/mm/yyyy): ')

            data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
            data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()

            historicos = buscar_historicos_entre_datas(session, data_inicio, data_fim)

            for i in historicos:
                print(f'{i.valor} - {i.tipo.value} - {i.data}')

    def _criar_grafico(self):
        with Session(engine) as session:
            criar_grafico_por_conta(session)

UI().start()
