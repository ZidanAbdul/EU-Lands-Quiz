# Länder-Quiz EU 1.0 Program 🌍

Ein interaktives Lernspiel, das Kindern und Erwachsenen hilft, die Länder Europas und deren Hauptstädte kennenzulernen. Ideal für Kinder ab 6 Jahren! 

Ein interaktives Quiz-Programm über europäische Länder und ihre Flaggen.


## Überblick
**Länder-Quiz EU 1.0** ist ein Quizspiel mit Flaggen und Hauptstädten von 40 europäischen Ländern. Ziel ist es, auf spielerische Weise geografisches Wissen zu fördern.

## Zielgruppe
- Kinder ab **6 Jahren** 
- Lehrkräfte und Eltern
- Alle, die Europa entdecken wollen 

## Voraussetzungen
- Windows-Betriebssystem
- Kein Internet erforderlich 
- Bildschirmauflösung: mind. 1024x768

## Installation 
1. Entpacke den Ordner `Länder_Quiz_Program`.
2. Doppelklicke auf `main.exe`, um das Spiel zu starten.
3. Kein Setup notwendig!


## Spielinhalt
- Insgesamt **80 Fragen** (je 40 Flaggen- & Hauptstadträtsel)
- Jede Frage zeigt entweder:
  - Eine Flagge → Wähle den Ländernamen.
  - Eine Flagge mit Ländernamen → Wähle die Hauptstadt.
- Nach jeder Antwort wird das Ergebnis angezeigt.
- Am Ende: Auswertung + Option zum Neustart.



## Anforderungen

- Python 3.x
- Tkinter (in Python enthalten)
- Pillow (PIL) für die Bildverarbeitung

## Installation

1. Stellen Sie sicher, dass Python 3.x installiert ist
2. Installieren Sie die erforderlichen Pakete:
   ```
   pip install Pillow
   ```

## Projektstruktur

- `main.py` - Hauptprogrammdatei
- `questions_with_ids.json` - Fragendatenbank
- `flage/` - Ordner mit Flaggenbildern und Hintergrundbild

## Verwendung

1. Starten Sie das Programm:
   ```
   python main.py
   ```
2. Klicken Sie auf "Quiz starten"
3. Beantworten Sie die Fragen durch Auswahl der richtigen Option
4. Sie können das Quiz jederzeit über den "Quiz beenden" Button beenden
5. Am Ende sehen Sie Ihre Ergebnisse mit der Option zum Neustart

## Ergebnisanzeige

Nach Abschluss des Quiz oder nach dem Klicken auf "Quiz beenden" sehen Sie:
- Anzahl der beantworteten Fragen
- Anzahl der richtigen und falschen Antworten
- Erfolgsquote in Prozent
- Motivierende Nachricht basierend auf Ihrer Leistung

## Autoren
- **The World Projektteam** – GFN Akademie Stuttgart, Abschlussprojekt 2025