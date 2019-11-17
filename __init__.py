"""
		Policy Reader Toolkit (v1.0)
This toolkit contains a list of components helping with parse context and extract useful entities in a Policy or regulatory document.


from .parser import Parser
from .planning import Planning
from .db import Database
from .nlp import NLP
from .time import Time

"""
import logging

__LogFormat__ = "%(asctime)s %(levelname)s %(message)s"


logging.basicConfig(format=__LogFormat__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



