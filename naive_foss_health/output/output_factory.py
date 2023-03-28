from naive_foss_health.output.format import OutputFormatter
from naive_foss_health.output.format_json import OutputFormatterJson
from naive_foss_health.output.format_yaml import OutputFormatterYaml
from naive_foss_health.output.format_markdown import OutputFormatterMarkdown

FORMAT_JSON = "json"
FORMAT_YAML = "yaml"
FORMAT_MARKDOWN = "markdown"

SUPPORTED_FORMATS = [ FORMAT_JSON, FORMAT_YAML , FORMAT_MARKDOWN ]

class OutputFormatterFactory:

    @staticmethod
    def formatter(format):
        if format.lower() == FORMAT_JSON:
            return OutputFormatterJson()
        elif format.lower() == FORMAT_YAML:
            return OutputFormatterYaml()
        elif format.lower() == FORMAT_MARKDOWN:
            return OutputFormatterMarkdown()

    @staticmethod
    def formats():
        return SUPPORTED_FORMATS
    
