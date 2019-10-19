{% macro section_heading(text, level) -%}
{%- with underline = "#*=-^\"" -%}
{%- if level < 2 -%}
{{ underline[level] * text|length }}
{% endif -%}
{{ text|title }}
{{ underline[level] * text|length }}
{%- endwith -%}
{%- endmacro -%}
{% macro bullet(text, level=0) -%}
{{ " " * level + "- " + text}}
{% endmacro %}
{% macro toc_values(values, level=0) %}
{%- for value in values -%}
{{ bullet(value['name'] + "_: *" + value['brief'] + "*", level) }}
{%- endfor -%}
{%- endmacro -%}
{% macro toc_groups(groups, level=0) %}
{% for group in groups -%}
{{ bullet(group['name'] + "_: *" + group['brief'] + "*", level) }}{{ toc_values(group['members'], level + 1) }}
{%- endfor -%}
{%- endmacro %}
{% macro section(title, level, text) -%}
{{ section_heading(title, level) }}
{{ text }}
{%- endmacro -%}
