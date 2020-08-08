from flask import Blueprint, session, render_template, request, redirect, url_for
from .helper import verify_auth
from ..representations.user import CreateUserRequest


# This code is written by using SampleProject as reference
def construct_auth_blueprint(user_client):
    auth_crud = Blueprint('auth', __name__)

    @auth_crud.route('/login', defaults={'page': 'index'})
    @auth_crud.route('/login/<page>', methods=['GET'])
    def login(page):
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is not None and error_message is None:
            user = user_client.get_by_email_id(claims['email'])
            if user is None:
                create_user_request = CreateUserRequest(name=claims['name'],
                                                        email=claims['email'],
                                                        image_id='hardcode',
                                                        role='admin')
                user = user_client.create(create_user_request)

        if page == 'index':
            return render_template(
                'index.html',
                user_data=claims, error_message=error_message)
        else:
            redir = redirect(url_for('user.view_subscriptions', id=str(user.id)))
            if request.cookies.get('funtech_token'):
                redir.set_cookie('funtech_token', request.cookies.get('funtech_token'))
            return redir

    @auth_crud.route('/logout')
    def logout():
        return redirect(url_for('.login'))

    return auth_crud
