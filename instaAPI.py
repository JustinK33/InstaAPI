from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

db.create_all()

post_put = reqparse.RequestParser() #this is the RequestParser object= makes sure the request fits the following guidelines
post_put.add_argument("name", type=str, help="name of post")
post_put.add_argument("date", type=str, help="date of post")
post_put.add_argument("likes", type=int, help="likes of post")

post_patch = reqparse.RequestParser()
post_patch.add_argument("name", type=str, help="name of post")
post_patch.add_argument("date", type=str, help="date of post")
post_patch.add_argument("likes", type=int, help="likes of post")

resource_field = { #this defines whats allowed to get through and formats the data according to the field type
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.String,
    'likes': fields.Integer
}

class Post(Resource):
    @marshal_with(resource_field) #this is what catches the request and passes it through a filter sort of thing with the defined resource_field
    def get(self, post_id):
        result = PostModel.query.filter_by(id=post_id).first()
        return result

    @marshal_with(resource_field)
    def put(self, post_id):
        args = post_put.parse_args()
        result = PostModel.query.filter_by(id=post_id).first()
        if not result:
            abort(409, message="already exist")
        post = PostModel(id=post_id, name=args['name'], date=args['date'], likes=args['likes'])
        db.session.add(post)
        db.session.commit()
        return post, 201
    
    @marshal_with(resource_field)
    def patch(self, post_id):
        args = post_patch.parse_args()
        result = PostModel.query.filter_by(id=post_id).first()
        if "name" in args and args['name'] is not None:
            result.name = args['name']
        if "date" in args and args['date'] is not None:
            result.name = args['date']
        if "likes" in args and args['likes'] is not None:
            result.name = args['likes']
        db.session.commit()
        return result


    def delete(self, post_id):
        result = PostModel.query.filter_by(id=post_id).first()
        if not result:
            abort(404, message="cant delete it doesnt exist")
        db.session.delete(result)
        db.session.commit()
        return '', 204

api.add_resource(Post, "/post/<int=id>")

if __name__ == "__main__":
    app.run(debug=True)