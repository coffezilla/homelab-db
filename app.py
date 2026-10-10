from flask import Flask, jsonify
import psycopg

from db import init_db, save_posts, save_user


app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/save-users")
def save_users_endpoint():
    try:
        return jsonify({"user": save_user()}), 201
    except psycopg.Error as error:
        return jsonify({"error": str(error)}), 500


@app.post("/api/save-posts")
def save_posts_endpoint():
    try:
        return jsonify({"posts": save_posts()}), 201
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 409
    except psycopg.Error as error:
        return jsonify({"error": str(error)}), 500


init_db()
