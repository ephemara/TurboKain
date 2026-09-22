# Locale

Markscript locale and internationalization - query and set the system locale,
language, encoding, region, and character set. Dispatches through the IVT to
Kain's `std::locale` bridge.

---

## get

Get the current locale identifier string.

> run "echo %LANG% 2>nul || chcp"

```markscript
# Query the current locale
call("locale_get")
# Result: locale string like "en_US.UTF-8" or "en-US"
```

---

## set

Set the runtime locale for this process.

> run "chcp 65001"

```markscript
# Set locale for this process
push("en_GB.UTF-8")
call("locale_set")
# Result: 1 on success, 0 if the locale is unsupported
```

---

## list

List all available locales installed on the system.

> run "wmic os get locale"

```markscript
# List all installed locales
call("locale_list")
# Result: newline-delimited locale identifier list
```

---

## encoding

Get the current character encoding (code page).

> run "chcp"

```markscript
# Query the current character encoding
call("locale_encoding")
# Result: encoding name like "UTF-8", "CP1252", "Shift-JIS"
```

---

## language

Get the current language code (ISO 639-1).

> run "echo %LANG% 2>nul || wmic os get OSLanguage"

```markscript
# Query the current language
call("locale_language")
# Result: two-letter code like "en", "de", "ja", "fr"
```

---

## country

Get the current country/region code (ISO 3166-1 alpha-2).

> run "echo %COUNTRY% 2>nul"

```markscript
# Query the current region
call("locale_country")
# Result: two-letter code like "US", "DE", "JP", "FR"
```

---

## format_date

Get the date format pattern used by the current locale.

```markscript
# Query date format for current locale
call("locale_format_date")
# Result: pattern string like "YYYY-MM-DD" or "MM/DD/YYYY"
```

---

## format_time

Get the time format pattern used by the current locale.

```markscript
# Query time format for current locale
call("locale_format_time")
# Result: pattern string like "HH:MM:SS" or "hh:MM:SS TT"
```
