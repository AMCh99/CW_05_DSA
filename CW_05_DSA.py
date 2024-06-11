import random
import hashlib

# test złożoności do testu Millera-Rabina
def miller_rabin_complexity(a, d, n, r):
    if pow(a, d, n) == 1:
        return False
    for j in range(r):
        if pow(a, 2**j * d, n) == n-1:
            return False
    return True

# Test Millera-Rabina do sprawdzania pierwszości liczby
def miller_rabin(n, k=64):
    if n != int(n):
        return False
    n = int(n)
    if n == 0 or n == 1:
        return False
    if n == 2 or n == 3:
        return True
    r = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        r += 1
    assert(2**r * d == n - 1)
    d = int(d)
    r = int(r)
    for i in range(k):
        a = random.randint(2, n - 2)
        if miller_rabin_complexity(a, d, n, r):
            return False
    return True

# Generowanie liczby pierwszej o określonej liczbie bitów - liczba q
def gen_prime_bits(bits=160):
    x = 0
    if bits < 1:
        return False
    while not miller_rabin(x, 64):
        x = random.randrange(2 ** (bits - 1), 2 ** bits) # Losuj liczbę x z zakresu odpowiedniego dla podanej liczby bitów
    return x

# Generowanie liczby pierwszej p o długości L bitów i dzielniku q o długości 160 bitów
def gen_prime_L_bit(L=1024):
    p = 1
    if L > 1024 or L < 512 or L % 64 != 0:
        return False
    while not (miller_rabin(p) and p.bit_length() == L):
        # Losowanie wartości x tak, aby liczba p miała dokładnie L bitów po przemnożeniu przez q i dodaniu 1
        x = random.randrange(2 ** (L - 160 - 1), 2 ** (L - 160))
        q = gen_prime_bits(160)
        p = x * q + 1  # Obliczanie p jako x*q + 1
    return p, q

# Generowanie parametrów DSA
def gen_param(L=1024):
    p, q = gen_prime_L_bit(L)
    h = random.randint(2, p - 2) # Losowanie wartości h z zakresu od 2 do p-2
    g = pow(h, int((p - 1) // q), p) # Obliczanie g jako h^((p-1)/q) mod p
    while g == 1:
        h = random.randint(2, p - 2)
        g = pow(h, int((p - 1) // q), p)
    return p, q, g

# Generowanie kluczy DSA
def gen_key(p, q, g):
    x = random.randint(1, q-1)  # Klucz prywatny
    y = pow(g, x, p)  # Klucz publiczny
    return x, y

# Funkcja do hashowania całego pliku za pomocą SHA-256
def sha256sum(file_path):
    file_hash = hashlib.sha256()  # Utwórz obiekt haszujący
    with open(file_path, 'rb') as f:
        fb = f.read(BLOCK_SIZE)  # Odczytaj blok z pliku
        while len(fb) > 0:
            file_hash.update(fb)  # Zaktualizuj obiekt haszujący
            fb = f.read(BLOCK_SIZE)  # Odczytaj kolejny blok
    return int(file_hash.hexdigest(), 16)

BLOCK_SIZE = 65536

# Funkcja podpisująca wiadomość
def sign(p, q, g, x, file_path):
    H_m = sha256sum(file_path)

    k = random.randint(1, q-1)  # Losowanie losowej liczby k z zakresu od 1 do q-1
    r = pow(g, k, p) % q  # Obliczanie r jako (g^k mod p) mod q
    if r == 0:
        return sign(p, q, g, x, file_path)
    
    k_inv = pow(k, -1, q)  # Odwrotność modulo q
    s = (k_inv * (H_m + x * r)) % q  # Obliczanie s jako (k^-1 * (H(m) + x * r)) mod q
    if s == 0:
        return sign(p, q, g, x, file_path)
    
    return r, s

# Funkcja weryfikująca podpis
def verify(p, q, g, y, file_path, signature):
    H_m = sha256sum(file_path)

    r, s = signature
    if not (0 < r < q and 0 < s < q):
        return False
    
    w = pow(s, -1, q)  # Obliczanie odwrotności s modulo q
    u1 = (H_m * w) % q  # Obliczanie u1 jako (H(m) * w) mod q
    u2 = (r * w) % q  # Obliczanie u2 jako (r * w) mod q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q  # Obliczanie v jako ((g^u1 * y^u2) mod p) mod q
    
    return v == r


def podpisz_plik(file_location):
    L = 1024
    p, q, g = gen_param(L)  # Generowanie parametrów
    x, y = gen_key(p, q, g)  # Generowanie kluczy
    file_path = file_location  # Ścieżka do pliku do podpisania
    signature = sign(p, q, g, x, file_path)  # Podpisanie pliku
    is_valid = verify(p, q, g, y, file_path, signature)  # Weryfikacja podpisu
    
    return L, p,q,g,x,y,file_path,signature,is_valid


def zweryfikuj_plik(file_location, key, signature, p, q, g):
    L = 1024
    # p, q, g = gen_param(L)  # Generowanie parametrów
    # x, y = gen_key(p, q, g)  # Generowanie kluczy
    file_path = file_location  # Ścieżka do pliku do podpisania
    # signature = sign(p, q, g, x, file_path)  # Podpisanie pliku
    is_valid = verify(p, q, g, key, file_path, signature)  # Weryfikacja podpisu
    
    return L,p,q,g,key,file_path,signature,is_valid


if __name__ == "__main__":
    # Przykład użycia:
    L = 1024
    p, q, g = gen_param(L)  # Generowanie parametrów
    x, y = gen_key(p, q, g)  # Generowanie kluczy
    file_path = "example.txt"  # Ścieżka do pliku do podpisania
    signature = sign(p, q, g, x, file_path)  # Podpisanie pliku
    is_valid = verify(p, q, g, y, file_path, signature)  # Weryfikacja podpisu

    # Wyświetlanie wyników
    print("Parametry:")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"g = {g}")
    print("\nKlucze:")
    print(f"x = {x} (private key)")
    print(f"y = {y} (public key)")
    print("\nWiadomość:")
    print(f"file_path = {file_path}")
    print("\nPodpis:")
    print(f"signature = {signature}")
    print(f"\nPodpis prawidłowy: {is_valid}")
