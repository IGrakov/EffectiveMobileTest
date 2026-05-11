# Permissions Management App

## Local deployment (Ubuntu)

1. Build docker image:\
``Make build``

2. To launch service:\
``Make up``

3. To shut down service:\
``Make down``

4. To run tests:\
``Make test``

Other useful commands are specified in Makefile


## Permissions schema

Permissions schema has two tiers:
1. Role permissions
For those standard Django groups are used + superuser status. The following groups (roles) are defined:
- admin
- supervisor
- manager
- default_user

Roles have the following ranks:
- superuser - 100 (highest possible)
- admin - 80
- supervisor - 50
- manager - 30
- default_user - 0

User can be assigned only a single role. If another role is assigned, the previous one is cleared.

A user is registered with default role of default_user. Higher rank roles can be assigned later only by admins.
Admin role or superuser role can be assigned only by superuser.

Users can be managed by themselves. Only admins can manage other users.
An admin user can be managed only by superuser or by himself.
Only superuser can retrieve or list superusers. Other operations with superusers cannot be performed via API.

Users are soft deleted, i.e. are not deleted from DB, but their status is_active becomes False.
A deleted user cannot log in or perform any actions.
Only superuser can perform actions with deleted users.

Only admin users can assign permissions to other users. Only superuser can assign permissions to admins and superusers.

2. Specific permissions related to products, which can be assigned to users
These are assigned in the table `user_userproductpermission`

The following permissions are defined:
- VIEW_PRODUCT
- SEE_QUANTITY

View product permission is specified via region permission to user, i.e. a user will be able to view products only in his region.

See quantity permission allows user to see wherehouse quantity only for products in his region.
If there no see quantity permission, user will be None instead of quantity. Users with role rank lower than manager cannot see quantity even with respective permission.

Permission to any user can be granted, revoked and updated only by superuser or admin.

