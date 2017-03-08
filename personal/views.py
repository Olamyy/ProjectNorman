# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('personal', __name__, url_prefix='/personal', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def login():
    return render_template('landingpage/privacy.html')
