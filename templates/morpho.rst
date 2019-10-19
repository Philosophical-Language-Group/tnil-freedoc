{%- from "rst_utils.rst" import section, toc_values, toc_groups -%}
{{ section(name, 2, full) }}
There are {{ values|length }} {{ name|title }}s
{%- if groups %} divided into {{ groups|length }} groups
{%- endif -%}:
{%- if groups -%}
{{ toc_groups(groups) }}
{%- else -%}
{{ toc_values(values) }}
{%- endif -%}
{% for value in values %}
{% if value['abbr'] %}.. _{{ value['abbr'] }}:{% endif %}
{{ section(value['name'], 3, value['full']) }}
{% if value['abbr'] %}{{ "Abbreviation: " + value['abbr'] }}{% endif %}
{% endfor %}
