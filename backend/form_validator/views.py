import phonenumbers

from dateutil import parser

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FormTemplate

# Константы для типов полей
DATE_FIELD = "date"
PHONE_FIELD = "phone"
EMAIL_FIELD = "email"
TEXT_FIELD = "text"

# Константы для названий шаблонов
TEMPLATE_FIELD_MAP = {
    "DateForm": "date",
    "PhoneForm": "phone",
    "EmailForm": "email",
    "TextForm": "text",
}


@api_view(["POST"])
def get_form(request):
    # Получаем данные из запроса
    form_data = request.data

    # Валидация полей формы
    validated_fields, status = validate_fields(form_data)

    # Обработка невалидных полей
    if status == "invalid":
        sorted_field = sort_fields(validated_fields)
        return Response(sorted_field)

    # Поиск соответствующего шаблона для валидных полей
    template_name = find_matching_template(validated_fields)

    # Подготовка данных для ответа
    response_data = {"name": template_name}

    # Добавление информации о полях, если это один из стандартных шаблонов
    if template_name in TEMPLATE_FIELD_MAP.keys():
        response_data["field_name_1"] = get_one_field_type(template_name)
    else:
        # Добавление информации о типах полей
        for i, field_info in enumerate(validated_fields.values()):
            response_data[f"field_name_{i + 1}"] = field_info["type"]

    # Возвращаем ответ
    return Response(response_data)


def sort_fields(validated_fields):
    # Сортировка полей по порядку
    order = {DATE_FIELD: 0, PHONE_FIELD: 1, EMAIL_FIELD: 2, TEXT_FIELD: 3}
    sorted_data = sorted(validated_fields.items(), key=lambda x: order[x[1]])

    return dict(sorted_data)


def get_one_field_type(template_name):
    return TEMPLATE_FIELD_MAP.get(template_name, "text")


def validate_fields(form_data):
    # Валидация полей формы
    validated_fields = {}
    invalid_fields = {}
    validation_field_names = [DATE_FIELD, PHONE_FIELD, EMAIL_FIELD, TEXT_FIELD]

    for field_name, value in form_data.items():
        field_type = get_field_type(value)

        # Учитываем только поля, поддерживаемые моделью
        if field_type == field_name and field_name in validation_field_names:
            validated_fields[field_name] = {"value": value, "type": field_type}
        else:
            invalid_fields[field_name] = field_type

    # Возвращаем валидные или невалидные поля
    return (
        (validated_fields, "valid")
        if validated_fields
        else (invalid_fields, "invalid")
    )


def get_field_type(value):
    # Определение типа поля на основе данных
    if is_date(value):
        return DATE_FIELD
    elif is_phone(value):
        return PHONE_FIELD
    elif is_email(value):
        return EMAIL_FIELD
    else:
        return TEXT_FIELD


def is_date(value):
    # Проверка дат на соотвествие форматам (DD.MM.YYYY или YYYY.MM.DD)
    try:
        parser.parse(value)
        return True
    except ValueError:
        return False


def is_phone(value):
    # Проверка, является ли значение номером телефона
    # в формате +7 xxx xxx xx xx
    try:
        phone_number = phonenumbers.parse(value, None)
        return phonenumbers.is_valid_number(phone_number)
    except phonenumbers.NumberParseException:
        return False


def is_email(value):
    # Проверка, является ли значение электронной почтой
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False


def find_matching_template(validated_fields):
    templates = FormTemplate.objects.all()
    one_field = []

    # Поиск соответствующего шаблона
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

        # Если количество совпадающих полей равно истинному
        # количеству и общему количеству валидных полей,
        # возвращаем название шаблона
        if match_count == true_fields_count == len(validated_fields):
            return template.name

        # Если только одно совпадающее поле, добавляем шаблон в список
        if match_count == 1:
            one_field.append(template.name)

    # Возвращаем первый из шаблонов из списка, если он существует
    return one_field[0] if one_field else None
