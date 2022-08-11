from dataclasses import dataclass, fields
from datetime import datetime
from functools import lru_cache
from itertools import chain
import psycopg2

from .app import app

class DoesNotExist(Exception): pass
class UniqueViolation(Exception): pass

class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)

class Model:
    @classmethod
    def create(self, **kwargs):
        table = self.Meta.tablename
        rowid = self.Meta.rowid
        columns = ', '.join(kwargs.keys())
        placeholders = ", ".join('%s' for _ in range(len(kwargs)))

        with app.db.cursor() as c:
            try:
                c.execute(
                    f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING {rowid}",
                    list(kwargs.values())
                )

                pk_val, = c.fetchone()
                return self.objects.get(**{rowid: pk_val})
            except psycopg2.errors.UniqueViolation:
                raise UniqueViolation()

    @classproperty
    def objects(self):
        return Manager(self)

class Manager:
    def __init__(self, model):
        self.model = model

    def get(self, **pk):
        table = self.model.Meta.tablename
        with app.db.cursor() as c:
            constraint = " AND ".join(f"{col} = %s" for col in pk.keys())
            field_names = [f.name for f in fields(self.model)]
            columns = ", ".join(f'T.{f}' for f in field_names)
            c.execute(
                f"SELECT {columns} FROM {table} T WHERE {constraint}",
                list(pk.values())
            )

            if c.rowcount == 0:
                raise DoesNotExist()

            return self.model(**dict(zip(field_names, c.fetchone())))

    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(ResultSet(self.model), name)

class ForeignKey:
    def __init__(self, model, field):
        self.model = model
        self.field = field

class ResultSet:
    def __init__(self, model):
        self.model = model
        self.constraints = dict()
        self._values = None
        self._slice = None
        self._ordering = None
        self._joins = dict()

    def filter(self, **constraints):
        self.constraints.update(constraints)
        return self

    def values(self, *columns):
        if self._values is None:
            self._values = list(columns)
        else:
            self._values.extend(columns)

        return self

    def ordering(self, *columns):
        if self._ordering is None:
            self._ordering = list(columns)
        else:
            self._ordering.extend(columns)

        return self

    def all(self):
        return list(self)

    @lru_cache
    def _get_fkeys(self):
        return {
            f.name: f
            for f in fields(self.model)
            if isinstance(f.type, ForeignKey)
        }

    def _get_field(self, f):
        if '__' not in f:
            return f, 0
        
        fkeys = self._get_fkeys()
        prop, foreign_field = f.split('__', 2)
        if prop not in self._joins: 
            if prop not in fkeys:
                raise Exception(f"{prop}: No such foreign key field")
            Tn = list(fkeys.keys()).index(prop) + 1
            self._joins[prop] = (fkeys[prop].type, Tn)

        _, Tn = self._joins[prop]
        return foreign_field, Tn

    def _get_joins(self):
        return ([k, *v] for k, v in self._joins.items())

    def _get_where(self):
        constraints = []
        for field in self.constraints.keys():
            field_name, Tn = self._get_field(field)
            constraints.append(f"T{Tn}.{field_name} = %s")

        return " AND ".join(constraints)

    def _get_select(self):
        if self.values is None:
            return [f'T0.{f.name}' for f in fields(self.model)]

        fields = []
        for f in self._values:
            field_name, Tn = self._get_field(f)
            fields.append(f"T{Tn}.{field_name}")

        return fields

    def __getitem__(self, slice):
        self._slice = slice
        return self

    @property
    def query(self):
        table = self.model.Meta.tablename
        constraint = self._get_where()
        columns = ', '.join(self._get_select())

        ordering = ''
        if self._ordering is not None:
            ordering = " ORDER BY " + ', '.join(
                f"{col[1:]} DESC" if col.startswith('-') else col
                for col in self._ordering
            )

        joins = ''
        for local_field, foreign, Tn in self._get_joins():
            foreign_table = foreign.model.Meta.tablename
            joins += ' JOIN %s T%s ON (T0.%s = T%s.%s)' % (
                foreign_table, Tn, local_field, Tn, foreign.field
            )

        limit = ''
        if self._slice is not None:
            if isinstance(self._slice, slice):
                start, end = self._slice.start or 0, self._slice.stop
                limit = f" LIMIT {end - start} OFFSET {start}"
            else:
                limit = f" LIMIT {self._slice}"

        return (
            f"SELECT {columns} FROM {table} T0{joins} WHERE {constraint}{ordering}{limit}",
            list(self.constraints.values())
        )

    def __iter__(self):
        # XXX: Dedupe this from _get_select()
        field_names = [f.name for f in fields(self.model)]
        with app.db.cursor() as c:
            print(self.query)
            c.execute(*self.query)
            for row in c:
                if self.values:
                    yield dict(zip(self._values, row))
                else:
                    # XXX: This won't work-- need to f
                    return self.model(**dict(zip(field_names, row)))

@dataclass
class User(Model):
    class Meta:
        tablename = 'chat.user'
        rowid = 'id'

    username:   str
    id:         int = None

@dataclass
class ChatRoom(Model):
    class Meta:
        tablename = 'chat.room'
        rowid = 'id'

    name:       str
    creator:    ForeignKey(User, 'id')
    id:         int = None

@dataclass
class ChatMessage(Model):
    class Meta:
        tablename = 'chat.message'
        rowid = 'id'

    poster:     ForeignKey(User, 'id')
    posted_at:  datetime
    room:       ForeignKey(ChatRoom, 'id')
    content:    str
    id:         int = None