#!/bin/bash

python3 backend/tools/card_template.py axis_flip Axis_Flip Axis mid cashback > backend/data/cards/axis/axis_flip.json
python3 backend/tools/card_template.py axis_ace Axis_Ace Axis premium cashback > backend/data/cards/axis/axis_ace.json
python3 backend/tools/card_template.py icici_amazon Amazon_ICICI ICICI mid cashback > backend/data/cards/icici/icici_amazon.json
python3 backend/tools/card_template.py icici_coral ICICI_Coral ICICI entry points > backend/data/cards/icici/icici_coral.json
python3 backend/tools/card_template.py hdfc_moneyback HDFC_MoneyBack HDFC entry cashback > backend/data/cards/hdfc/hdfc_moneyback.json
