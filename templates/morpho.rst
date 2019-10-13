{% macro rst_section_heading(text, underline) -%}
{{ text|title }}
{{ underline * text|length}}
{%- endmacro %}
{{ rst_section_heading(name, '=') }}

{{ full }}

There are {{ values|length }} {{ name|title }}s:

{% for value in values %}
- {{ value['name'] }}_: {{ value['brief'] }}
{% endfor %}

{% for value in values %}
{{ rst_section_heading(value['name'], '-')}}

{{ value['full'] }}
{% endfor %}
