"""Modelos de descritivo fornecidos pela área usuária; # indica informação a preencher."""

MODELOS_DESCRITIVO: tuple[tuple[str, str], ...] = (
    ("Chapa metálica", "Chapa metálica medindo # cm de diâmetro estampada: #."),
    ("Pino metálico", "Pino metálico medindo # cm de altura."),
    ("Tronco de pirâmide", "Tronco de pirâmide de concreto com base maior medindo # cm e base menor "
     "medindo # cm; altura do topo em relação à base de # cm; chapa metálica medindo # cm de diâmetro "
     "estampada: #; plataforma de proteção adicional medindo # m x # m."),
    ("Pilar cilíndrico com centragem/pino", "Pilar cilíndrico de concreto com diâmetro de # cm; altura "
     "do topo em relação à base de # cm; possui no topo um dispositivo de centragem forçada / pino "
     "metálico com # cm de altura; possui uma chapa metálica a # cm do topo medindo # cm de diâmetro estampada: #."),
    ("Pilar cilíndrico com chapa no topo", "Pilar cilíndrico de concreto com diâmetro de # cm; altura "
     "do topo em relação à base de # cm; possui no topo uma chapa metálica medindo # cm de diâmetro "
     "estampada: #; possui uma chapa metálica a # cm do topo medindo # cm de diâmetro estampada: #."),
    ("Pilar prismático com centragem/pino", "Pilar prismático de concreto; altura do topo em relação "
     "à base de # cm; possui no topo um dispositivo de centragem forçada / pino metálico com # cm de "
     "altura; possui uma chapa metálica a # cm do topo medindo # cm de diâmetro estampada: #."),
    ("Pilar prismático com chapa no topo", "Pilar prismático de concreto; altura do topo em relação "
     "à base de # cm; possui no topo uma chapa metálica medindo # cm de diâmetro estampada: #; possui "
     "uma chapa metálica a # cm do topo medindo # cm de diâmetro estampada: #."),
)
