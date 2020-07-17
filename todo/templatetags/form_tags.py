from django import template

register = template.Library()

@register.filter
def field_type(field):
	return field.field.widget.__class__.__name__

@register.filter
def input_class(field):
	css_class = ""
	if field.form.is_bound:
		if field_type(field) != "PasswordInput":
			if field.errors:
				css_class = "is-invalid"
			else:
				css_class = "is-valid"

	return f"form-control {css_class}"