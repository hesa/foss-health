import json

from naive_foss_health.output import OutputFormatter

class OutputFormatterJson(OutputFormatter):

    def __init__(self):
        pass

    def format(self, report):
        return json.dumps(analysis, indent=4)


