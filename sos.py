class AuthView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        try:
            user = UsersService(db.session).get_item_by_email(email=req_json.get("email"))
            tokens = login_user(request.json, user)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")

    def put(self):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        try:
            tokens = refresh_user_token(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")
user = UsersService(db.session).get_item_by_email(email=req_json.get("email"))
            tokens = login_user(request.json, user)
            return tokens, 200
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")

#########

req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        if not req_json.get('id'):
            req_json['id'] = user_id
        try:
            return UsersService(db.session).update(req_json)
        except ItemNotFound:
            abort(404, message="User not found")
