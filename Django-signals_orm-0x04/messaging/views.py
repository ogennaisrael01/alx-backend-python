from django.contrib.auth.models import User
def delete_user(user_id):
    """
    Delete user by id
    """
    user = User.objects.get(id=user_id)
    user.delete()