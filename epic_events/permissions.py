from rest_framework.permissions import BasePermission


class HasSignupPermission(BasePermission):
    """
    Only team management or superuser can create, list, retrieve, update and destroy an user.
    """
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
    """
    Team management and superuser can do everything
    - list, retrieve : for team sale and team support
    - create, update : for team sale
    """

    message = "Vous n'avez pas les droits requis pour effectuer cette opération sur les clients."

    def has_permission(self, request, view):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()
        if view.action in ['list', 'retrieve']:
            if is_saler or is_support:
                return True

        if view.action in ['create', 'update']:
            return is_saler

        return False

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.sales_contact == request.user:
                return True

        return False


class HasContractPermission(BasePermission):
    """
        Team management and superuser can do everything
        - list, retrieve : for team sale and team support
        - create : for team sale
        - update : for sale if is sales_contact
    """

    message = "Vous n'avez pas les droits requis pour effectuer cette opération sur les contrats."

    def has_permission(self, request, view):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()

        if view.action in ['list', 'retrieve']:
            if is_saler or is_support:
                return True

        if view.action in ['create', 'update']:
            return is_saler

        return False

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.sales_contact == request.user:
                return True

        return False


class HasEventPermission(BasePermission):
    """
            Team management and superuser can do everything
            - list, retrieve : for team sale and team support
            - create : for team sale
            - update : for sale if is sales_contact or for support if is support_contact
            """

    message = "Vous n'avez pas les droits requis pour effectuer cette opération sur les événements."

    def has_permission(self, request, view):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        is_saler = request.user.groups.filter(name="Sale").exists()
        is_support = request.user.groups.filter(name="Support").exists()

        if view.action in ['list', 'retrieve']:
            if is_saler or is_support:
                return True

        if view.action in ['create']:
            return is_saler

        if view.action in ['update']:
            if is_saler or is_support:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        is_team_management = request.user.groups.filter(name="Management").exists()

        if request.user.is_superuser or is_team_management:
            return True

        if view.action in ['update']:
            if obj.support_contact == request.user or obj.client.sales_contact == request.user:
                return True

        return False