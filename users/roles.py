class BaseRole:
    """
    Base role class. By default, denies all permissions.
    Subclasses should override methods to grant specific permissions.
    """
    def __init__(self, user):
        self.user = user

    def can_view_customers(self): return False
    def can_view_all_customers(self): return False
    def can_add_edit_customer(self, customer=None): return False
    def can_add_edit_any_customer(self): return False
    def can_view_orders(self): return False
    def can_view_all_orders(self): return False
    def can_create_order(self): return False
    def can_edit_cancel_order(self, order): return False
    def can_edit_cancel_any_order(self): return False
    def can_update_order_status(self, order=None): return False
    def can_assign_orders(self): return False
    def can_manage_products(self): return False
    def can_manage_users(self): return False
    def can_assign_agents(self): return False
    def can_configure_settings(self): return False
    def can_export_reports(self): return False

class AgentRole(BaseRole):
    """
    Role for agents. Grants permissions only for their own customers and orders.
    """
    def can_view_customers(self): return True
    def can_view_all_customers(self): return False
    def can_add_edit_customer(self, customer=None):
        # Only if customer is in agent's regions
        return customer is None or customer.region in self.user.regions.all()
    def can_create_order(self): return True
    def can_view_orders(self): return True
    def can_edit_cancel_order(self, order):
        # Agent can edit/cancel only their own orders in 'Pending' status
        return order.agent_id == self.user.id and order.status.name == 'Pending'

class StaffRole(BaseRole):
    """
    Role for staff. Grants permissions for all customers and orders, and product management.
    """
    def can_view_customers(self): return True
    def can_view_all_customers(self): return True
    def can_add_edit_customer(self, customer=None): return True
    def can_add_edit_any_customer(self): return True
    def can_view_orders(self): return True
    def can_view_all_orders(self): return True
    def can_create_order(self): return True
    def can_edit_cancel_order(self, order): return True
    def can_edit_cancel_any_order(self): return True
    def can_update_order_status(self, order=None): return True
    def can_assign_orders(self): return True
    def can_manage_products(self): return True
    def can_export_reports(self): return True

class AdminRole(StaffRole):
    """
    Role for admin. Grants all permissions, including user and agent management and configuration.
    """
    def can_manage_users(self): return True
    def can_assign_agents(self): return True
    def can_configure_settings(self): return True

def get_user_role(user):
    """
    Returns the appropriate role instance for the given user.
    """
    if not hasattr(user, 'role'):
        return BaseRole(user)
    if user.role == 'ADMIN':
        return AdminRole(user)
    elif user.role == 'STAFF':
        return StaffRole(user)
    elif user.role == 'AGENT':
        return AgentRole(user)
    return BaseRole(user)