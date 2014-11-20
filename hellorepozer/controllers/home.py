import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from hellorepozer.lib.base import BaseController, render

from hellorepozer.lib.auth.helpers import authenticated

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        return 'Hello (repoze.who) World'


