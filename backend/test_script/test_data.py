test_data = [
    # Валидные примеры
    {
        "comment": "Valid example for DateForm",
        "test_data": {"date": "11.12.2020", "text": "test_text"},
    },
    {
        "comment": "Valid example for PhoneForm",
        "test_data": {"phone": "+79123456789", "text": "test_text"},
    },
    {
        "comment": "Valid example for EmailForm",
        "test_data": {"email": "test@example.com", "text": "test_text"},
    },
    {
        "comment": "Valid example for TextForm",
        "test_data": {"text": "test_text"},
    },
    {
        "comment": "Valid example for ContactForm",
        "test_data": {
            "email": "test@example.com",
            "phone": "+79123456789",
            "text": "test_text",
        },
    },
    {
        "comment": "Valid example for CustomForm",
        "test_data": {
            "email": "test@example.com",
            "phone": "+79123456789",
            "date": "11.12.2020",
            "text": "test_text",
        },
    },
    # Невалидные примеры
    {
        "comment": "Invalid example with missing key",
        "test_data": {"telephone": "+79123456789"},
    },
    {
        "comment": "Invalid example with missing key",
        "test_data": {"date_time": "1111.12.03"},
    },
    {
        "comment": "Invalid example with missing key",
        "test_data": {"e_mail": "test@test.ru"},
    },
    {
        "comment": "Invalid example for DateForm",
        "test_data": {"date": "invalid_date", "text": "test_text"},
    },
    {
        "comment": "Invalid example for PhoneForm",
        "test_data": {"phone": "+791234567890", "text": "test_text"},
    },
    {
        "comment": "Invalid example for EmailForm",
        "test_data": {"email": "invalid_email", "text": "test_text"},
    },
    {"comment": "Invalid example for TextForm", "test_data": {"text": 123}},
]
