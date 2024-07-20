from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,reqparse,marshal_with,fields,abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db = SQLAlchemy(app)
api = Api(app)



user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be empty")
user_args.add_argument('email', type=str, required=True, help="Email cannot be empty")


userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}
class GetUsers(Resource):
    @marshal_with(userFields)
    def get(self):
        users=UserModel.query.all()
        return users


class CreateUser(Resource):
    # @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'],email=args['email'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

class GetUserById(Resource):
    @marshal_with(userFields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user
class EditUser(Resource):
    #@marshal_with(userFields)
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        user.name = args['name']    
        user.email = args['email'] 
        db.session.commit()   
        return {"message": "User Updated successfully"}, 200
    
class DeleteUser(Resource):
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)     
        db.session.commit()   
        return {"message": "User deleted successfully"}, 200
    
api.add_resource(EditUser,'/api/user/edit/<int:id>')    
api.add_resource(GetUserById,'/api/user/<int:id>')
api.add_resource(DeleteUser,'/api/user/delete/<int:id>')
api.add_resource(CreateUser, '/api/users/add/')
api.add_resource(GetUsers, '/api/users/') 

class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
        
    def __repr__(self):
        return f"User(name={self.name},email={self.email})"
        

@app.route('/')
def home():
    return '<h1> FLASK REASTFUL API</h1>'
if __name__ == '__main__':
    app.run(debug='TRUEpip')


