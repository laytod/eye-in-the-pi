from models import User
from forms import LoginForm
from cameraPi import app, login_manager

from flask import url_for, render_template, redirect, request
from flask.ext.login import current_user, login_user, logout_user


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(app.log_path)
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


@login_manager.user_loader
def load_user(userID):
    return User.get(int(userID))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', next=request.path))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(User.selectBy(username=form.user.data).getOne(), remember=form.rememberMe.data)
        logger.info('Logged in {user}'.format(user=current_user.username))
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logger.info("Logging out {user}".format(user=current_user.username))
    logout_user()
    return redirect(url_for('index'))
