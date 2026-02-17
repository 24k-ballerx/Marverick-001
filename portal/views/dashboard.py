from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Redirect to role-based dashboard."""
    user = request.user
    if user.role == 'admin':
        return redirect('portal:admin_dashboard')
    if user.role == 'teacher':
        return redirect('portal:teacher_dashboard')
    if user.role == 'student':
        return redirect('portal:student_dashboard')
    return redirect('portal:admin_dashboard')
