class User(models.Model):
    username    = models.CharField(max_length=255, unique=True, db_index=True)
    email       = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    avatar      = models.FileField(upload_to=user_directory_path, default="")
