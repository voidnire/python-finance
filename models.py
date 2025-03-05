from sqlmodel import Field, SQLModel, create_engine,Relationship,Session
from enum import Enum
from typing import Optional,List
from datetime import date

class Bancos(Enum):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'
    ITAU = 'Itaú'


class Status(Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Conta(SQLModel, table=True):
    id: Optional[int]  = Field(default=None,primary_key=True)
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)
    valor: float

    historicos: List["Historico"] = Relationship(back_populates="conta")


class Tipos(Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saida'

class Historico(SQLModel, table=True):
    id: Optional[int]  = Field(default=None,primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Optional[Conta] = Relationship(back_populates="historicos")
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date

sqlite_file_name = "database.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=True)  

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  

if __name__ == "__main__":  
    create_db_and_tables()  
