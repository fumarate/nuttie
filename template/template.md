# {{ title }}

{% for msg in msg_list %}
{% if msg.status %}✅{% else %}❗{% endif %}{{msg.username}}{{msg.message}}
{% endfor %}
![](https://s3.bmp.ovh/imgs/2022/03/30/5da1fb3b32061ee7.jpg)