# Template

MarkScript template rendering -- fill variables, loops, conditionals, includes.
Wraps `sed`, `awk`, and shell tools via the IVT for text templating.

---

## render

Replace `{{ variable }}` placeholders with values.

> run "sed 's/{{name}}/World/g' template.md > output.md"

```markscript
let template = "greeting.tmpl"
let output = "greeting.md"
let name = "World"
push("sed 's/{{name}}/" + name + "/g' " + template + " > " + output)
call("run")
# "Hello, {{name}}" -> "Hello, World"
```

---

## multiple_vars

Render multiple variables in one template.

> run "sed -e 's/{{title}}/Report/g' -e 's/{{year}}/2026/g' template.txt"

```markscript
let file = "report.tmpl"
let title = "Q2 Report"
let year = 2026
push("sed -e 's/{{title}}/" + title + "/g' -e 's/{{year}}/" + year + "/g' " + file)
call("run")
# all variables substituted
```

---

## variable_default

Provide default values for variables not in template.

> run "grep -q '{{author}}' template.txt && sed -i 's/{{author}}/Unknown/g' template.txt"

```markscript
let var = "author"
let default = "Unknown"
let file = "letter.tmpl"
push("grep -q '{{" + var + "}}' " + file + " && sed -i 's/{{" + var + "}}/" + default + "/g' " + file)
call("run")
# {{author}} replaced with "Unknown" if present
```

---

## loop_rows

Repeat a template row for each item in a data file.

> run "while IFS= read -r line; do sed \"s/{{item}}/$line/g\" row.tmpl; done < items.txt"

```markscript
let template = "row.tmpl"
let data = "items.txt"
push("while IFS= read -r item; do sed 's/{{item}}/'\"$item\"'/g' " + template + "; done < " + data)
call("run")
# row template rendered for each item
```

---

## loop_table

Generate HTML table rows from CSV data.

> run "awk -F',' '{print \"<tr><td>\" $1 \"</td><td>\" $2 \"</td></tr>\"}' data.csv"

```markscript
let file = "data.csv"
let sep = ","
push("awk -F'" + sep + "' '{print \"<tr><td>\" $1 \"</td><td>\" $2 \"</td></tr>\"}' " + file)
call("run")
# CSV data to table rows
```

---

## condition_if

Conditionally include content based on a setting.

> run "if [ \"$FLAG\" = \"true\" ]; then sed -n '/<!-- BEGIN -->/,/<!-- END -->/p' template.md; fi"

```markscript
let flag = "true"
let file = "page.tmpl"
push("if [ \"" + flag + "\" = \"true\" ]; then sed -n '/<!-- BEGIN_SHOW -->/,/<!-- END_SHOW -->/p' " + file + "; else sed '/<!-- BEGIN_SHOW -->/,/<!-- END_SHOW -->/d' " + file + "; fi")
call("run")
# only includes section if flag is true
```

---

## include

Include one file into another at a marker.

> run "sed '/{{include:header}}/{r header.md' -e 'd}' base.md"

```markscript
let marker = "{{include:header}}"
let include_file = "header.md"
let base = "page.md"
push("sed '/" + marker + "/{r " + include_file + "' -e 'd}' " + base)
call("run")
# inserts header.md content at marker
```

---

## include_multi

Include multiple partials into a master template.

> run "sed -e '/{{include:header}}/{r header.md' -e 'd}' -e '/{{include:footer}}/{r footer.md' -e 'd}' base.md"

```markscript
let base = "base.md"
push("sed -e '/{{include:header}}/{r header.md' -e 'd}' -e '/{{include:footer}}/{r footer.md' -e 'd}' -e '/{{include:nav}}/{r nav.md' -e 'd}' " + base)
call("run")
# multiple file inclusions
```

---

## escape_html

Escape HTML special characters in text.

> run "sed 's/&/\\&amp;/g; s/</\\&lt;/g; s/>/\\&gt;/g; s/\"/\\&quot;/g' input.txt"

```markscript
let file = "raw.txt"
push("sed 's/&/\\\\&amp;/g; s/</\\\\&lt;/g; s/>/\\\\&gt;/g; s/\"/\\\\&quot;/g' " + file)
call("run")
# HTML-safe output
```

---

## date_insert

Insert the current date into a template.

> run "sed \"s/{{date}}/$(date +%Y-%m-%d)/g\" template.md"

```markscript
let file = "letter.tmpl"
push("sed \"s/{{date}}/$(date +%Y-%m-%d)/g\" " + file)
call("run")
# {{date}} replaced with 2026-06-10
```

---

## batch_render

Apply a template to multiple data rows from a JSON file.

> run "jq -r '.[] | \"\\(.name), \\(.role)\"' people.json | while IFS=',' read -r name role; do sed -e \"s/{{name}}/$name/g\" -e \"s/{{role}}/$role/g\" card.tmpl > \"cards/$name.md\"; done"

```markscript
let tmpl = "card.tmpl"
let data = "people.json"
let out_dir = "cards/"
push("mkdir -p " + out_dir + " && jq -r '.[] | \"\\(.name)| \\(.role)\"' " + data + " | while IFS='|' read -r name role; do sed -e \"s/{{name}}/$name/g\" -e \"s/{{role}}/$role/g\" " + tmpl + " > \"" + out_dir + "$name.md\"; done")
call("run")
# renders a card per person from JSON data
```

---

## upper_filter

Apply uppercase transformation to variable values.

> run "sed 's/{{name}}/NAME/g' template.txt"

```markscript
let file = "template.txt"
let name = "John"
push("sed \"s/{{name}}/$(echo " + name + " | tr 'a-z' 'A-Z')/g\" " + file)
call("run")
# "John" rendered as "JOHN"
```
