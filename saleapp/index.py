import math
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, request, redirect, session, jsonify
import dao
from saleapp import app, admin, login
import cloudinary.uploader
from models import UserEnum

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("roomType_id")
    page = request.args.get("page")
    rooms = dao.load_rooms(q=q, cate_id=cate_id, page=page)
    pages = dao.count_room()
    return render_template('index.html', rooms=rooms, pages=math.ceil(pages/app.config["PAGE_SIZE"]))


@app.route('/rooms/<int:id>')
def details(id):
    room = dao.load_room_by_id(id)
    return render_template('room-details.html', room = room)


@app.route('/register', methods=["get", "post"])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            ava_path = None
            name = request.form.get('name')
            username = request.form.get('username')
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                ava_path = res['secure_url']
            dao.add_user(name=name, username=username, password=password, avatar=ava_path)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"
    return render_template('register.html', err_msg=err_msg)



@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)



@app.route('/login-admin', methods=['post'])
def process_login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return redirect('/admin')
                   # ,err_msg = err_msg)



@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')




@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)



# # Kiểm tra quyền admin
# @app.route('/admin/login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = dao.auth_user(username=username, password=password)
#         if user and user.role == UserEnum.ADMIN:
#             login_user(user)
#             return redirect('/admin')
#         return redirect('/admin/login')
#     return render_template('admin/login.html')


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)