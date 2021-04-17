# Monopoly
Aplikacja webowa umożliwiająca grę w monopoly 2-4 osób w czasie rzeczywistym realizowana w ramach kursu z pythona na 6 semestrze studiów.
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
- Adres: http://localhost:8080

Konfiguracyjne zmienne w pliku `settings_local.py`

### Baza danych

- Postgresql: latest
- port: 5432
