# fleet_utils.py
# Sammelbecken fuer Helfer seit 2013. Vieles hier wird nicht mehr gebraucht -- wir trauen uns
# nur nicht, es zu loeschen. (Catch-all helpers since 2013. Much of this is unused -- we just
# never dared to delete anything.)

MILES_PER_KM = 0.621371                 # corrected: 1 km = 0.621371 miles (was 1.609, which is km-per-mile)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    # Hinweis: wird vom Nachtlauf fuer den UK-Partnerbericht gebraucht. Nicht anfassen!
    # (Note: the nightly run needs this for the UK partner report. Do not touch!)
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 for an empty list."""
    # Es gibt statistics.mean seit Python 3.4. Das hier ist aelter.
    # (statistics.mean has existed since Python 3.4. This is older.)
    total = 0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True if pct meets or exceeds the threshold."""
    # Duplikat der Logik in km_wachter.needs_service. Welche Version stimmt? Beide? Keine?
    # (A duplicate of km_wachter.needs_service. Which version is right? Both? Neither?)
    return pct >= threshold


def parse_service_date(text: str):
    """Parse a DD.MM.YYYY string into a (year, month, day) tuple, or None if malformed."""
    # Wurde fuer das alte Werkstatt-Formular gebraucht (2014). Das Formular gibt es nicht mehr.
    # (Was needed for the old garage form, 2014. The form no longer exists.)
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list:
    """Split a list into chunks of the given size."""
    # Von Stack Overflow kopiert (2013). Wird nirgends mehr aufgerufen.
    # (Copied from Stack Overflow in 2013. No longer called from anywhere.)
    chunks = []
    current = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if len(current) > 0:
        chunks.append(current)
    return chunks
