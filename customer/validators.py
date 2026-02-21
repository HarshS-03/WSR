import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomComplexityValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("Password must include at least one uppercase letter."),
                code="password_no_upper",
            )
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("Password must include at least one lowercase letter."),
                code="password_no_lower",
            )
        if not re.search(r"\d", password):
            raise ValidationError(
                _("Password must include at least one digit."), code="password_no_digit"
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _(
                    "Password must include at least one special character (e.g., @, #, $, etc)."
                ),
                code="password_no_special",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters and include one uppercase letter, "
            "one lowercase letter, one number, and one special character."
        )
