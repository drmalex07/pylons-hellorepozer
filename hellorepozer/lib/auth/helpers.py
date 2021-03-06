from decorator import decorator
from pylons import  request
from pylons.controllers.util import abort

def user_is_authenticated():
    """ Returns True if a user is authenticated, False otherwise """
    identity = request.environ.get('repoze.who.identity')
    return identity is not None

@decorator
def authenticated(func, *args, **kwargs):
    """ Decorator that will use Pylons' abort method to trigger the repoze.who
        middleware that this request needs to be authenticated. """
    if not user_is_authenticated():
        abort(401)
    return func(*args, **kwargs)

