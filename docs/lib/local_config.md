
::: lib.local_config


---
# All Local Settings

All this local settings are in a .txt file in the folder %USERPROFILE%\TemplateRecognitionAPI.
They are **case sensitive** and if changed directly from that file, there must no be spaces between name, = and value (for example: name=value and not name = value)

- template_folder: the folder from where to search for all template to use in template matching
- saving_folder: the folder where to save the matched templates
- MATCHING_THRESHOLD: a global value for template matching. tm return positive matching if confidence is over this value
- is_colored: If use colored template and frame during template matching