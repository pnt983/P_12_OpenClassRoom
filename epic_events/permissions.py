from rest_framework.permissions import BasePermission


class HasSignupPermission(BasePermission):

    def has_permission(self, request, view):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if view.action in ['create', 'list', 'retrieve']:
            if is_team_management or request.user.is_superuser:
                return True

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if view.action in ['update', 'destroy']:
            if is_team_management or request.user.is_superuser:
                return True

        return False


class HasCustomerPermission(BasePermission):

    def has_permission(self, request, view):
        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()
        is_team_management = request.user.groups.filter(name="Management").exists()
        if view.action in ['list', 'retrieve']:
            if is_saler or is_support or is_team_management or request.user.is_superuser:
                return True

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.sales_contact == request.user:
                return True

        return False


class HasContractPermission(BasePermission):

    def has_permission(self, request, view):
        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()
        is_team_management = request.user.groups.filter(name="Management").exists()
        if view.action in ['list', 'retrieve']:
            if is_saler or is_support or is_team_management or request.user.is_superuser:
                return True

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.sales_contact == request.user:
                return True

        return False


class HasEventPermission(BasePermission):

    def has_permission(self, request, view):
        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()
        is_team_management = request.user.groups.filter(name="Management").exists()
        if view.action in ['list', 'retrieve']:
            if is_saler or is_support or is_team_management or request.user.is_superuser:
                return True

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.support_contact == request.user or obj.client.sales_contact == request.user:
                return True

        return False

