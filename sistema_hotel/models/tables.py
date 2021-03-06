"""Modulo destinado a criação das tabelas do banco"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import (
    create_engine,
    Column,
    Boolean,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    UniqueConstraint,
    DateTime)
from sqlalchemy.orm import scoped_session, sessionmaker

db_url = 'postgresql://pi_fatec:pi_fatec123@localhost:5432/pi_fatec_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    """Tabela de usuarios."""

    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True, unique=True)
    username = Column(String(255), nullable=False)
    pwd = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    permission = Column(String(255), nullable=False)
    activity = Column(Boolean, default=True, primary_key=True)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'User(id_user={}, username={}, \
                pwd={}, name={}, \expenses_value, \
                permission={}, activity={})'.format(
                     self.id_user,
                     self.username,
                     self.pwd,
                     self.name,
                     self.permission,
                     self.activity
                    )


class Resident(db.Model):
    """Tabela de Hospedes."""

    __tablename__ = 'resident'
    __table_args__ = (UniqueConstraint('id_user'),)

    id_resident = Column(Integer, primary_key=True, unique=True)
    id_user = Column(Integer, ForeignKey('user.id_user'))
    name = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False)
    phone = Column(String(11), nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Resident(id_resident={}, id_user={}, \
                name={}, cpf={}, phone={}'.format(
                     self.id_resident,
                     self.id_user,
                     self.name,
                     self.cpf,
                     self.phone
                    )


class Category(db.Model):
    """Tabela de categorias."""

    __tablename__ = 'category'

    id_category = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Category(nome={}, descricao={})'.format(self.nome,
                                                        self.descricao)


class ResidentAccount(db.Model):
    """Tabela de contas dos hospedes."""

    __tablename__ = 'resident_account'

    id_account = Column(Integer, primary_key=True, unique=True)
    id_resident = Column(Integer, ForeignKey('resident.id_resident'))
    openned = Column(DateTime, default='0000-00-00', nullable=False)
    closed = Column(DateTime, default='0000-00-00', nullable=False)
    status = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Category(id_account={}, id_resident={}, \
                openned={}, closed={}, status={}, value={})'.format(
                    self.id_account,
                    self.id_resident,
                    self.openned,
                    self.closed,
                    self.status,
                    self.value
                )


class Employee(db.Model):
    """Tabela de funcionarios."""

    __tablename__ = "employee"

    id_employee = Column(Integer, primary_key=True, unique=True)
    id_user = Column(Integer, ForeignKey('user.id_user'))
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False)
    cargo = Column(String(255), nullable=False)
    setor = Column(String(255), nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Employee(id_employee={}, id_user={}, \
                nome={}, cpf={}, cargo={}, setor={})'.format(
                    self.id_employee,
                    self.id_user,
                    self.nome,
                    self.cpf,
                    self.cargo,
                    self.setor
                )


class Room(db.Model):
    """Tabela de quartos."""

    __tablename__ = 'room'

    id_room = Column(Integer, primary_key=True, unique=True)
    number = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    daily_value = Column(Float, nullable=False)
    status = Column(String(15), default='Livre', nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Room(id_room={}, number={}, \
                floor={}, description={}, daily_value={}, status={})'.format(
                    self.id_room,
                    self.number,
                    self.floor,
                    self.description,
                    self.daily_value,
                    self.status
                )


class Service(db.Model):
    """Tabela de serviços."""

    __tablename__ = 'service'

    id_service = Column(Integer, primary_key=True, unique=True)
    id_category = Column(Integer, ForeignKey('category.id_category'))
    id_employee = Column(Integer, ForeignKey('employee.id_employee'))
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Service(id_service={}, id_category={}, \
                id_employee={}, name={}, description={}, value={})'.format(
                    self.id_service,
                    self.id_category,
                    self.id_employee,
                    self.name,
                    self.description,
                    self.value
                )


class Accommodation(db.Model):
    """Tabela de Hospedagem."""

    __tablename__ = "accommodation"

    id_accommodation = Column(Integer, primary_key=True, unique=True)
    id_room = Column(Integer, ForeignKey('room.id_room'))
    id_resident = Column(Integer, ForeignKey('resident.id_resident'))
    date_entrance = Column(DateTime, default='0000-00-00', nullable=False)
    date_leave = Column(DateTime, default='0000-00-00', nullable=False)
    observation = Column(String(255), nullable=False)
    expenses_value = Column(Float, nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Accommodation(id_accommodation={}, id_room={}, \
                id_resident={}, date_entrance={}, date_leave={}, \
                observation={}, expenses_value={})'.format(
                    self.id_accommodation,
                    self.id_room,
                    self.id_resident,
                    self.date_entrance,
                    self.date_leave,
                    self.observation,
                    self.expenses_value
                )


class Order(db.Model):
    """Tabela de Pedidos."""

    __tablename__ = "order"

    id_order = Column(Integer, primary_key=True, unique=True)
    id_resident = Column(Integer, ForeignKey('resident.id_resident'))
    id_room = Column(Integer, ForeignKey('room.id_room'))
    date = Column(DateTime, default='0000-00-00', nullable=False)
    status = Column(String(255), nullable=False)
    total_value = Column(String(255), nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'Order(id_order={}, id_resident={}, \
                id_room={}, date={}, status={}, \
                total_value={})'.format(
                    self.id_order,
                    self.id_resident,
                    self.id_room,
                    self.date,
                    self.status,
                    self.total_value
                )

class ItemOrder(db.Model):
    """Tabela de Items e pedidos."""

    __tablename__ = "item_order"

    id_item_order = Column(Integer, primary_key=True, unique=True)
    id_order = Column(Integer, ForeignKey('order.id_order'))
    id_service = Column(Integer, ForeignKey('service.id_service'))
    id_employee = Column(Integer, ForeignKey('employee.id_employee'))
    amount = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    status = Column(String(255), nullable=False)

    def __repr__(self):
        """Alteração do __repr__ para representar os elementos da tabela."""
        return 'ItemOrder(id_order={}, id_service={}, \
                id_employee={}, amount={}, value={}, \
                status={})'.format(
                    self.id_order,
                    self.id_service,
                    self.id_employee,
                    self.amount,
                    self.value,
                    self.status
                )

engine = create_engine(db_url)
session = scoped_session(sessionmaker(bind=engine))
