from rest_framework.decorators import api_view
from rest_framework.response import Response

import re
import datetime
from .models import FormTemplate


@api_view(["POST"])
def get_form(request):
    form_data = request.data

    validated_fields, status = validate_fields(form_data)

    if status == "invalid":
        sorted_field = sorted_by(validated_fields)
        return Response(sorted_field)

    template_name = find_matching_template(validated_fields)

    response_data = {"name": template_name}

    if template_name == "DateForm":
        response_data["field_name_1"] = "date"
    elif template_name == "EmailForm":
        response_data["field_name_1"] = "email"
    elif template_name == "TextForm":
        response_data["field_name_1"] = "text"

    for i, field_info in enumerate(validated_fields.values()):
        if template_name not in ["DateForm", "EmailForm", "TextForm"]:
            response_data[f"field_name_{i + 1}"] = field_info["type"]

    return Response(response_data)


def sorted_by(validated_fields):
    order = {"date": 0, "phone": 1, "email": 2, "text": 3}
    sorted_data = sorted(validated_fields.items(), key=lambda x: order[x[1]])

    return dict(sorted_data)


def validate_fields(form_data):
    validated_fields = {}
    invalid_fields = {}
    validation_field_names = ["date", "phone", "email", "text"]

    for field_name, value in form_data.items():
        field_type = get_field_type(value)

        # Учитываем только поля, которые поддерживаются моделью
        if field_type == field_name and field_name in validation_field_names:
            validated_fields[field_name] = {"value": value, "type": field_type}
        else:
            invalid_fields[field_name] = field_type

    if validated_fields:
        return validated_fields, "valid"

    return invalid_fields, "invalid"


def get_field_type(value):
    # Функция для определения типа поля на основе входных данных
    if is_date(value):
        return "date"
    elif is_phone(value):
        return "phone"
    elif is_email(value):
        return "email"
    else:
        return "text"


def is_date(value):
    # Проверка, является ли значение датой в формате DD.MM.YYYY или YYYY.MM.DD
    try:
        if "." in value:
            # Пытаемся разобрать в формате DD.MM.YYYY
            datetime.datetime.strptime(value, "%d.%m.%Y")
        else:
            # Пытаемся разобрать в формате YYYY-MM-DD
            datetime.datetime.strptime(value, "%Y.%m.%d")
        return True
    except ValueError:
        return False


def is_phone(value):
    # Проверка, является ли значение телефонным номером в формате +7xxxxxxxxxx
    phone_pattern = re.compile(r"^\+7\d{3}\d{3}\d{2}\d{2}$")
    return bool(phone_pattern.match(value))


def is_email(value):
    # Проверка, является ли значение корректным email
    email_pattern = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    return bool(email_pattern.match(value))


def find_matching_template(validated_fields):
    templates = FormTemplate.objects.all()
    one_field = []

    for template in templates:
        true_fields_count = sum(
            getattr(template, field)
            for field in template.__dict__
            if isinstance(getattr(template, field), bool)
        )

        match_count = 0
        for field_info in validated_fields.values():
            if getattr(template, field_info["type"]) == 1:
                match_count += 1

        if match_count == true_fields_count == len(validated_fields):
            return template.name

        if match_count == 1:
            one_field.append(template.name)

    return one_field[0]
