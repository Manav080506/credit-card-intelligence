from backend.schemas.card_schema import (
    REQUIRED_CARD_FIELDS,
    REQUIRED_FEES_FIELDS,
    REQUIRED_EARN_RULE_FIELDS,
    OPTIONAL_CARD_FIELDS
)

class CardValidationError(Exception):
    pass


def _check_fields(obj: dict, schema: dict, context: str):
    for key, expected_type in schema.items():
        if key not in obj:
            raise CardValidationError(f"{context}: missing field '{key}'")

        if not isinstance(obj[key], expected_type):
            raise CardValidationError(
                f"{context}: field '{key}' must be of type {expected_type}"
            )


def validate_card(card: dict, filename: str):
    _check_fields(card, REQUIRED_CARD_FIELDS, filename)

    _check_fields(card["fees"], REQUIRED_FEES_FIELDS, f"{filename}.fees")

    if not card["earn_rules"]:
        raise CardValidationError(f"{filename}: earn_rules cannot be empty")

    for i, rule in enumerate(card["earn_rules"]):
        _check_fields(
            rule,
            REQUIRED_EARN_RULE_FIELDS,
            f"{filename}.earn_rules[{i}]"
        )
