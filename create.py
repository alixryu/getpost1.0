#!/usr/bin/env python3

from getpost.models import Base
from getpost.orm import engine

Base.metadata.create_all(engine)
