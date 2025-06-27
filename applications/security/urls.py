from django.urls import path

from applications.security.views.auth import signin, signout , signup
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.usuarios import UserCreateView, UserDeleteView, UserListView, UserUpdateView
from applications.security.views.grupo import GroupListView, GroupUpdateView, GroupCreateView, GroupDeleteView
from applications.security.views.grupo_modulo_permisos import GroupModulePermissionListView, GroupModulePermissionCreateView, GroupModulePermissionUpdateView, GroupModulePermissionDeleteView, GroupModulePermissionAjaxView

app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [

  # rutas de modulos
  path('module_list/',ModuleListView.as_view() ,name="module_list"),
  path('module_create/', ModuleCreateView.as_view(),name="module_create"),
  path('module_update/<int:pk>/', ModuleUpdateView.as_view(),name='module_update'),
  path('module_delete/<int:pk>/', ModuleDeleteView.as_view(),name='module_delete'),

# rutas de menus
  path('menu_list/',MenuListView.as_view() ,name="menu_list"),
  path('menu_create/', MenuCreateView.as_view(),name="menu_create"),
  path('menu_update/<int:pk>/', MenuUpdateView.as_view(),name='menu_update'),
  path('menu_delete/<int:pk>/', MenuDeleteView.as_view(),name='menu_delete'),

  # rutas de autenticacion
  path('signin/', signin, name='signin'),
  path('signup/', signup, name='signup'),
  path('logout/', signout, name='signout'),


# rutas de usuarios
path('user_list/', UserListView.as_view(), name="user_list"),
path('user_create/', UserCreateView.as_view(), name="user_create"),
path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

# rutas de grupos
path('group_list/', GroupListView.as_view(), name="group_list"),
path('group_create/', GroupCreateView.as_view(), name="group_create"),
path('group_update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
path('group_delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),

# rutas de grupos_modulos_permisos
path('group_module_permission_list/', GroupModulePermissionListView.as_view(), name="group_module_permission_list"),
path('group_module_permission_create/', GroupModulePermissionCreateView.as_view(), name="group_module_permission_create"),
path('group_module_permission_update/<int:pk>/', GroupModulePermissionUpdateView.as_view(), name='group_module_permission_update'),
path('group_module_permission_delete/<int:pk>/', GroupModulePermissionDeleteView.as_view(), name='group_module_permission_delete'),
path('group_module_permission_ajax/', GroupModulePermissionAjaxView.as_view(), name='group_module_permission_ajax'),
path('group_module_permission_ajax/<int:pk>/', GroupModulePermissionAjaxView.as_view(), name='group_module_permission_ajax_delete'),

]