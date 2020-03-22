# Monopoly

### Instalacja

Do odpalenia projektu trzeba pobrać dockera.
[Instrukcja na stronie](https://docs.docker.com/install/)

## Zarządzanie

### Komendy

#### Uruchomienie

`$ cd project_path/Monopoly`

`$ docker-compose up`

#### Zatrzymanie

`$ docker-compose stop`

#### Usunięcie kontenerów

`$ docker-compose down`


### Dane techniczne

#### Projekt

- Wersja pythona: 3.8.2
- Adres: http://localhost:8000

Konfiguracyjne rzeczy przychowujemy w pliku `settings_local.py`,
którego nie dodajemy do gita.

### Baza danych

- Postgresql: latest
- port: 5432
