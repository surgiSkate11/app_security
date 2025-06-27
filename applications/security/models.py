from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from django.db.models import UniqueConstraint
from applications.security.utils.audit_user import AccionChoices

# =========================
# MODELO: Menu
# =========================
"""
Modelo Menu: Representa las categorías principales de navegación del sistema.
Cada menú agrupa varios módulos relacionados funcionalmente.

Ejemplos:
1. Ventas (icon: bi bi-cart, order: 1) - Agrupa módulos de clientes, facturación, cotizaciones
2. Inventario (icon: bi bi-box, order: 2) - Agrupa módulos de productos, stock, transferencias
3. Finanzas (icon: bi bi-cash-coin, order: 3) - Agrupa módulos financieros
"""
class Menu(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, unique=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, default='bi bi-calendar-x-fill')
    order = models.PositiveSmallIntegerField(verbose_name='Orden', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['order', 'name']

# =========================
# MODELO: Module
# =========================
"""
Modelo Module: Representa funcionalidades específicas del sistema agrupadas por menú.
Cada módulo tiene una URL única y pertenece a un menú particular.

Ejemplos:
1. Clientes (url: clientes/, menu: Ventas) - Gestión de clientes
2. Facturación (url: facturacion/, menu: Ventas) - Emisión de facturas
3. Productos (url: productos/, menu: Inventario) - Catálogo de productos
"""
class Module(models.Model):
    url = models.CharField(verbose_name='Url', max_length=100, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    # La relación ForeignKey con el modelo Menu indica una relación de una a muchos en la que
    # un menú puede tener múltiples módulos, pero cada módulo pertenece a un solo menú.
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name='Menu', related_name='modules')
    description = models.CharField(verbose_name='Descripción', max_length=200, null=True, blank=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, default='bi bi-x-octagon')
    is_active = models.BooleanField(verbose_name='Es activo', default=True)
    order = models.PositiveSmallIntegerField(verbose_name='Orden', default=0)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f'{self.name} [{self.url}]'

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['menu', 'order', 'name']

# =========================
# MANAGER: GroupModulePermissionManager
# =========================
class GroupModulePermissionManager(models.Manager):
    """
    Obtiene los módulos con su respectivo menú del grupo requerido que estén activos
    """
    def get_group_module_permission_active_list(self, group_id):
        return self.select_related('module', 'module__menu').filter(
            group_id=group_id,
            module__is_active=True
        )
# modulos_activos_de_grupo = GroupModulePermission.objects.get_group_module_permission_active_list(group_id)
# El select_related permite optimizar las consultas a la base de datos, hace un join, y une estos tres:
# GrupoModulePermission | module | menu

# autor = Autor.objects.filter(nombre='Gabriel García Márquez')
# En mi caso voy a decir:
# modulos_activos_de_grupo = GroupModulePermission.objects.get_group_module_permission_active_list(group_id = "1", module__is_active=True)

# =========================
# MODELO: GroupModulePermission
# =========================
"""
Modelo GroupModulePermission: Asocia grupos con módulos y define qué permisos
tiene cada grupo sobre cada módulo específico.

Ejemplos:
1. Vendedores - Clientes: permisos [view_client, add_client, change_client]
2. Contadores - Facturas: permisos [view_invoice, add_invoice, change_invoice]
3. Bodegueros - Stock: permisos [view_stock, add_stock, change_stock]
"""
class GroupModulePermission(models.Model):
    # La relación del campo group indica que un grupo puede tener múltiples permisos sobre diferentes módulos.
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Grupo', related_name='module_permissions')
    module = models.ForeignKey('security.Module', on_delete=models.PROTECT, verbose_name='Módulo', related_name='group_permissions')
    permissions = models.ManyToManyField(Permission, verbose_name='Permisos')
    # Manager personalizado (conserva toda la funcionalidad del manager por defecto)
    objects = GroupModulePermissionManager()

    def __str__(self):
        return f"{self.module.name} - {self.group.name}"

    class Meta:
        verbose_name = 'Grupo módulo permiso'
        verbose_name_plural = 'Grupos módulos permisos'
        ordering = ['group', 'module']
        constraints = [
            UniqueConstraint(fields=['group', 'module'], name='unique_group_module')
        ]

# =========================
# MODELO: User
# =========================
"""
Modelo User: Extiende el usuario estándar de Django para añadir campos personalizados.
Utiliza email como identificador principal para login en lugar del username.

Ejemplos:
1. admin (email: admin@empresa.com) - Administrador del sistema
2. jperez (email: jperez@empresa.com) - Usuario con roles de Vendedor y Contador
3. mgarcia (email: mgarcia@empresa.com) - Usuario con roles de Contador y Auditor
"""
class User(AbstractUser, PermissionsMixin):
    dni = models.CharField(verbose_name='Cédula o RUC', max_length=13, blank=True, null=True)
    image = models.ImageField(
        verbose_name='Imagen de perfil',
        upload_to='security/users/',
        max_length=1024,
        blank=True,
        null=True
    )
    email = models.EmailField('Email', unique=True)
    direction = models.CharField('Dirección', max_length=200, blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        permissions = (
            ("change_userprofile", "Cambiar perfil de Usuario"),
            ("change_userpassword", "Cambiar contraseña de Usuario"),
        )

    # Métodos utilitarios
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_groups(self):
        return self.groups.all()

    def get_short_name(self):
        return self.username

    # def get_group_session(self):
    #     request = get_current_request()
    #     print("request==>", request)
    #     return Group.objects.get(pk=request.session['group_id'])

    # def set_group_session(self):
    #     request = get_current_request()
    #     if 'group' not in request.session:
    #         groups = request.user.groups.all().order_by('id')
    #         if groups.exists():
    #             request.session['group'] = groups.first()
    #             request.session['group_id'] = request.session['group'].id

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/usuario_anonimo.png'

    # Ejemplo de método save personalizado para manejo de contraseñas (comentado)
    # def save(self, *args, **kwargs):
    #     def password_needs_hashing(password):
    #         # Detecta si la contraseña ya está hasheada
    #         return not password.startswith('pbkdf2_') and not password.startswith('argon2') and not password.startswith('bcrypt')
    #     if self.pk is None:
    #         if password_needs_hashing(self.password):
    #             self.set_password(self.password)
    #     else:
    #         old = User.objects.get(pk=self.pk)
    #         if self.password != old.password and password_needs_hashing(self.password):
    #             self.set_password(self.password)
    #     super().save(*args, **kwargs)

class AuditUser(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuario',on_delete=models.PROTECT)
    tabla = models.CharField(max_length=100, verbose_name='Tabla')
    registroid = models.IntegerField(verbose_name='Registro Id')
    accion = models.CharField(choices=AccionChoices, max_length=15, verbose_name='Accion')
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    estacion = models.CharField(max_length=100, verbose_name='Estacion')

    def __str__(self):
        return "{} - {} [{}]".format(self.usuario.username, self.tabla, self.accion)

    class Meta:
        verbose_name = 'Auditoria Usuario '
        verbose_name_plural = 'Auditorias Usuarios'
        ordering = ('-fecha', 'hora')