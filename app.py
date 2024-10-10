# microservice for register users and authenticate users of a bookstore project


from users_app import app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5011)