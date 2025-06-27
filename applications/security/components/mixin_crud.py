from django.db.models import Q

# Django imports for messages, authentication, and decorators
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

# Import custom components for permissions, sessions, and menu modules
from applications.security.components.group_permission import GroupPermission
from applications.security.components.group_session import UserGroupSession
from applications.security.components.menu_module import MenuModule

# =========================
# Mixin para ListView
# =========================
class ListViewMixin(object):
    query = None
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        # Inicializa el filtro de consulta vacío
        self.query = Q()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Agrega títulos y permisos al contexto
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.model._meta.verbose_name_plural}'
        context['title1'] = f'Consulta de {self.model._meta.verbose_name_plural}'
        # Llena el menú y los permisos del grupo activo
        MenuModule(self.request).fill(context)
        userGroupSession = UserGroupSession(self.request)
        group = userGroupSession.get_group_session()
        context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group)
        return context

# =========================
# Mixin para CreateView
# =========================
class CreateViewMixin(object):
    def get_context_data(self, **kwargs):
        # Agrega títulos y permisos al contexto para crear objetos
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.model._meta.verbose_name}'
        context['title1'] = f'Ingresar {self.model._meta.verbose_name_plural}'
        MenuModule(self.request).fill(context)
        userGroupSession = UserGroupSession(self.request)
        group = userGroupSession.get_group_session()
        context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group)
        return context

# =========================
# Mixin para UpdateView
# =========================
class UpdateViewMixin(object):
    def get_context_data(self, **kwargs):
        # Agrega títulos y permisos al contexto para actualizar objetos
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.model._meta.verbose_name_plural}'
        context['title1'] = f'Ingresar {self.model._meta.verbose_name_plural}'
        MenuModule(self.request).fill(context)
        userGroupSession = UserGroupSession(self.request)
        group = userGroupSession.get_group_session()
        context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group)
        return context

# =========================
# Mixin para DeleteView
# =========================
class DeleteViewMixin(object):
    def get_context_data(self, **kwargs):
        # Agrega títulos y permisos al contexto para eliminar objetos
        context = super().get_context_data(**kwargs)
        print("entro al deleteMixin")
        context['title'] = f'{self.model._meta.verbose_name_plural}'
        MenuModule(self.request).fill(context)
        userGroupSession = UserGroupSession(self.request)
        group = userGroupSession.get_group_session()
        context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group)
        return context

# =========================
# Mixin para control de permisos en vistas
# =========================
class PermissionMixin(object):
    permission_required = ''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user_session = UserGroupSession(request)
            user_session.set_group_session()

            # Si no hay grupo activo en sesión, redirige a home
            if 'group_id' not in request.session:
                return redirect('home')

            # Permite acceso total a superusuarios
            if user.is_superuser:
                return super().get(request, *args, **kwargs)

            # Obtiene permisos del grupo y valida acceso
            group = user_session.get_group_session()
            permissions = self._get_permissions_to_validate()
            print("permissions", permissions)
            if not permissions.__len__():
                print("entro permisos vacios")
                return super().get(request, *args, **kwargs)

            if not group.module_permissions.filter(
                    permissions__codename__in=permissions
            ).exists():
                print("no tengo permiso")
                messages.error(request, 'No tiene permiso para ingresar a este módulo')
                return redirect('home')

            return super().get(request, *args, **kwargs)

        except Exception as ex:
            messages.error(
                request,
                'A ocurrido un error al ingresar al modulo, error para el admin es : {}'.format(ex))

        # Si el usuario está autenticado pero ocurre error, redirige a home
        if request.user.is_authenticated:
            return redirect('home')

        # Si no está autenticado, redirige a login
        return redirect('security:auth_login')

    def _get_permissions_to_validate(self):
        # Devuelve los permisos requeridos para la vista
        if self.permission_required == '':
            return ()

        if isinstance(self.permission_required, str):
            return self.permission_required,

        return tuple(self.permission_required)