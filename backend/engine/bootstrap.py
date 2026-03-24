from backend.engine.card_loader import load_all_cards

BOOTSTRAP = load_all_cards()

CARDS = BOOTSTRAP.cards
CARD_ERRORS = BOOTSTRAP.errors
