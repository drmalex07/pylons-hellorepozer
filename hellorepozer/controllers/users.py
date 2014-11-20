import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from hellorepozer.lib.base import BaseController, render

from hellorepozer.lib.auth.helpers import authenticated

log = logging.getLogger(__name__)

class UsersController(BaseController):

    def __before__(self):
        count_visits = session.get('count_visits', 0);
        session['count_visits'] = count_visits +1;
        pass

    def __after__(self):
        session.save()

    #
    # login-related actions
    #

    def login_form(self):
        #raise Exception ('break')
        c.action = url(controller='users', action='login',
            came_from = request.params.get('came_from', '/'));
        return render('login_redirecting_form.html');

    def login(self):
        # Not reached, intercepted by repoze.who to perform 'authenticate' and 'remember' duties
        return 'Logged in!'

    def logged_in(self):
        identity = request.environ.get("repoze.who.identity")
        came_from = request.params.get('came_from', '/')
        redirect_url = None
        if identity:
            # Success
            redirect_url = came_from
        else:
            # Failed
            redirect_url = url(controller='users', action='login_form', came_from=came_from)

        redirect(redirect_url)
        return

    def logout(self):
        # Not reached, intercepted by repoze.who to perform 'forget' duties
        return 'Logged out!'

    def logged_out(self):
        came_from = request.params.get('came_from')
        if came_from:
            redirect(came_from)
        return render('logged_out.html');


    #
    # account-related actions
    #

    @authenticated
    def me(self):
        c.who_identity = request.environ.get('repoze.who.identity')
        c.count_visits = session['count_visits']
        c.logout_url = url(controller='users', action='logout')
        return render('users/me.html')

