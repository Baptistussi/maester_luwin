import random

names = [
    "Joaquim",
    "João",
    "Antônio",
    "José",
    "Pedro",
    "Sebastião",
    "Miguel",
    "Antenor",
    "Jeremias",
    "Gertrude",
    "Rosa",
    "Amália",
    "Maria",
    "Amanda",
    "Serafina",
    "Madalenha",
    "Paula",
]

surnames = [
    "Ferreira",
    "Teixeira",
    "Siqueira",
    "Marinho",
    "Safra",
    "Matarazzo",
    "Lopes",
    "Figueira",
]


def fake_full_name():
    return f"{random.choice(names)} {random.choice(surnames)}"


def fake_amount():
    return random.randint(1000, 1000000)  # R$ 10,00 ~ R$ 10.000,00


def generate_cpf():
    # Generate first 9 digits
    cpf = [random.randint(0, 9) for _ in range(9)]

    # Calculate first check digit
    sum_ = sum((10 - i) * cpf[i] for i in range(9))
    d1 = (sum_ * 10 % 11) % 10
    cpf.append(d1)

    # Calculate second check digit
    sum_ = sum((11 - i) * cpf[i] for i in range(10))
    d2 = (sum_ * 10 % 11) % 10
    cpf.append(d2)

    # Convert to string format XXX.XXX.XXX-YY
    cpf_str = "".join(map(str, cpf))
    return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
