import yaml

from naive_foss_health.output.format import OutputFormatter

class OutputFormatterYaml(OutputFormatter):

    def __init__(self):
        pass

    def format(self, report):
        return yaml.safe_dump(report)

    def format_error(self, message):
        return yaml.safe_dump({ "error": { "message": message} }, indent=4)

