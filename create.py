#!/usr/bin/env python3

from sqlalchemy.orm import configure_mappers

from getpost.models import Base
from getpost.orm import engine

configure_mappers()  # sqlalchemy-searchable
Base.metadata.create_all(engine)
