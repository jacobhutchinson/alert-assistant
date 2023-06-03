# Prompts for smart_monitoring

PROMPT_TEMPLATE = """

"""

QUERY1 = """The Salesforce Data Extensions pipeline ran into the following error:

```
ERROR - __main__ - salesforce_data_extensions_run.extension_preprocessing - 
Extension Activation_PL_GotRate_AWS was not found at location 
s3://upstart/env/production/partner/salesforce/extensions/
Activation_PL_GotRate_AWS/Activation_PL_GotRate_AWS_20230524.csv
```

Can you summarize the issue and suggest resolutions?"""

QUERY2 = """How do I get started making queries to the data lake, and who do I need to contact to get access?"""

REFINE_TEMPLATE = """

"""
