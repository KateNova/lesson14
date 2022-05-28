from flask import Blueprint, jsonify
from utils import search_by_title, search_by_year_range, search_by_rating, search_by_genre

main_blueprint = Blueprint("main_blueprint", __name__)


@main_blueprint.route("/")
def index():
    return "Начните работу с поиском фильма"


@main_blueprint.route("/movie/<title>")
def get_movie(title):
    return jsonify(search_by_title(title))


@main_blueprint.route("/movie/<int:start_year>/to/<int:end_year>")
def get_movies_by_range(start_year, end_year):
    return jsonify(search_by_year_range(start_year, end_year))


@main_blueprint.route("/rating/children")
def get_movie_by_child_rating():
    return jsonify(search_by_rating(['G']))


@main_blueprint.route("/rating/family")
def get_movie_by_fam_rating():
    return jsonify(search_by_rating(['G', 'PG', 'PG-13']))


@main_blueprint.route("/rating/adult")
def get_movie_by_adult_rating():
    return jsonify(search_by_rating(['R', 'NC-17']))


@main_blueprint.route("/genre/<genre>")
def get_list_by_genre(genre):
    return jsonify(search_by_genre(genre))
