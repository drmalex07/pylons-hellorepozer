"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    m = Mapper(directory=config['pylons.paths']['controllers'],always_scan=config['debug'])
    m.minimization = False
    m.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    m.connect('/error/{action}', controller='error')
    m.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    m.redirect('/', '/users/me')

    m.connect('/login_form', controller='users', action='login_form')
    m.connect('/login', controller='users', action='login')
    m.connect('/logout', controller='users', action='logout')
    m.connect('/logged-in', controller='users', action='logged_in')
    m.connect('/logged-out', controller='users', action='logged_out')

    m.connect('/{controller}/{action}')
    m.connect('/{controller}/{action}/{id}')

    return m
