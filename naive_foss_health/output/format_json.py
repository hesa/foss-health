import json

from naive_foss_health.output.format import OutputFormatter

class OutputFormatterJson(OutputFormatter):

    def __init__(self):
        pass

    def format(self, report):
        return json.dumps(report, indent=4)

    def format_error(self, message):
        return json.dumps({ "error": { "message": message} }, indent=4)

