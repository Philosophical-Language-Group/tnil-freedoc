{%- from "rst_utils.rst" import section, toc_values, toc_groups -%}
{% macro enumerate_values(values, level=3) %}
{% for value in values %}
{% if value['abbr'] %}.. _{{ value['abbr'] }}:{% endif %}
{{ section(value['name'], level, value['full']) }}
{% if value['abbr'] %}{{ "Abbreviation: " + value['abbr'] }}{% endif %}
{% endfor %}
{% endmacro %}
{{ section(name, 2, full) }}
There are {{ values|length }} {{ name|title }}s
{%- if groups %} divided into {{ groups|length }} groups
{%- endif -%}:
{%- if groups %}
{{ toc_groups(groups) }}
{% else %}

{{ toc_values(values) }}
{% endif %}
{% if groups %}
{% for group in groups %}
{{ section(group['name'], 3, group['full']) }}

{{ enumerate_values(group['members'], 4) }}
{% endfor %}
{% else %}
{{ enumerate_values(values) }}
{% endif %}
