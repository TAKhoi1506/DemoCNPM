from datetime import datetime
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from saleapp import app, db , dao
from models import RoomType, Room, UserEnum
from flask_login import current_user, logout_user
from flask import redirect, request
from flask_admin import BaseView
from functools import wraps
from flask import abort

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN

    # #mới thêm
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect('/admin/login')

class MyRoomTypeView(ModelView):        #Chuyển từ ModelView sang MyModelView
    column_list = ["name", "rooms"]


class MyRoomView(ModelView):           #Chuyển từ ModelView sang MyModelView
    column_list = ["name", "roomType_id", "image"]
    column_searchable_list = ["id", "name"]
    column_filters = ["id", "name"]
    can_export = True

class MyBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(MyBaseView):
    @expose('/')
    def index(self):
        # revenue_product = dao.stats_revenue_by_product(kw=request.args.get('kw'))
        # revenue_period = dao.stats_revenue_by_period(year=request.args.get('year', datetime.now().year),
        #                                              period=request.args.get('period', 'month'))
        return self.render('admin/stats.html')
                           # , revenue_product=revenue_product, revenue_period=revenue_period)
class RulesView(MyBaseView):
    def index(self):
        return self.render('admin/rules.html')

class LogoutView(MyBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


#Kiểm tra quyền truy cập
class MyAdminIndexView(AdminIndexView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.role == UserEnum.ADMIN
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect('/admin/login')
    @expose('/')
    def index(self):
        # stats = dao.count_product_by_cate()
        return self.render('admin/index.html')
                           # , stats=stats)

# Kiểm tra quyền admin


# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != UserEnum.ADMIN:
#             return redirect('/admin/login')
#         return f(*args, **kwargs)
#     return decorated_function




admin = Admin(app=app, name="Hotel Booking", template_mode="bootstrap4")
              #, index_view= MyAdminIndexView) #Thêm index_view
admin.add_views(MyRoomTypeView(RoomType, db.session,name="Loại Phòng"))
admin.add_views(MyRoomView(Room, db.session,name ="Phòng"))
admin.add_views(StatsView(name="Thống kê"))
#admin.add_views(RulesView(name="Quy định"))
admin.add_views(LogoutView(name="Đăng xuất"))