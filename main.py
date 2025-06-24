from reserva_bot import ejecutar_reserva
import os

if __name__ == "__main__":
    ejecutar_reserva(os.getenv("EMAIL_GYM"), os.getenv("PASS_GYM"))
    ejecutar_reserva(os.getenv("EMAIL_GYM2"), os.getenv("PASS_GYM2"))
    ejecutar_reserva(os.getenv("EMAIL_GYM3"), os.getenv("PASS_GYM3"))
