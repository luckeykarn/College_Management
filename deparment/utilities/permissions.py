#------permission are classified into three types------->
#first-level:-Admin,Superadmin,Superuser (this is  user model class which can be considered as ObjectA)
#second-level:-object 'B' is assigned to user(i.e in object B , ObjectA is assigned), where user called as ObjectA
#third-level:-object 'C' is assigned to object object B(i.e object B is assigned in object C)

#model ObjectB->user field
#model ObjectC->objectB field(objectB id)


#as example, we can consider as , user,company,job where user is ObjectA,company is ObjectB,job is ObjectC

from rest_framework.permissions import BasePermission

SUPER_ADMIN = 1
ADMIN = 2


def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def SuperAdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.is_superuser)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [ADMIN,SUPER_ADMIN])

def isOwner(request):
    if str(request.user.id) == str(request.data.get('user')):
        return True
    
    elif len(request.data)==0 and len(request.POST)==0:
        return True

    return False


# def ObjectBOwner(request):
#     company = ObjectB.objects.filter(id = request.data.get('objectb'),user = request.user.id)
#     if company.exists():
#         return True
#     return False

class deparmentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list"]:
            return True
        elif view.action in ['retrieve']:
            return isOwner(request)
        elif view.action in ['create','update']:
           print("user prirnting",request.user.is_authenticated)
           if not request.user.is_authenticated:
               return False
           if request.user.role in ['Admin','Hr']:
               return True
           else:
               return False
        elif view.action == "partial_update":
            if request.user.role in ["Admin" , "Hr"]:
                return True
            else:
                return False
        elif view.action == 'destroy':
            if request.user.role == "Admin":
                return True
            else:
                return False

