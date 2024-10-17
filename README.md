# Zastosowanie dużych modeli językowych do tworzenia inteligentnych agentów w grach komputerowych
Kod źródłowy do pracy magisterskiej na kierunku Informatyka (specjalność: Sztuczna Inteligencja) na Wydziale Informatyki i Telekomunikacji Politechniki Poznańskiej.

## Instrukcja uruchomienia
Potrzebna wersja Pythona: 3.11

Praca wykorzystuję menadzer pakietów `poetry`, który można zainstalować korzystając z instrukcji na stronie [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

Aby zainstalować wszystkie zależności przy pomocy narzędzia `poetry`, należy wykonać poniższe polecenie:
```bash
poetry install
```
Z racji użycia dużych modeli językowych konieczne jest podaine klucza API do OpenAI. Klucz można uzyskać na stronie [https://beta.openai.com/signup/](https://beta.openai.com/signup/). Po uzyskaniu klucza, należy go przypisać do zmiennej środowiskowej `OPENAI_API_KEY`.

Aby uruchomić wersje demonstracyjną, należy wykonać poniższe polecenie:
```bash
cd src
poetry run python demo.py
```