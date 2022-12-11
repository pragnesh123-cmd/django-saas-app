class RoleType:
    ADMIN = 1
    STAFF = 2

    CHOICES = ((ADMIN, "admin"),(STAFF, "staff"))


class SocialAccountType:
    NORMAL = 0
    GOOGLE = 1
    FACEBOOK = 2

    CHOICES = (
        (NORMAL, "normal"),
        (GOOGLE, "google"),
        (FACEBOOK, "facebook"),
    )
