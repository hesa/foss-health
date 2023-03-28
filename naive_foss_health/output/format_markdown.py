from naive_foss_health.output.format import OutputFormatter

class OutputFormatterMarkdown(OutputFormatter):

    def __init__(self):
        pass

    def _format_status(self, val):
        if val:
            return "OK"
        return "Not OK"
    
    def _format_items(self, report):
        data = []
        data.append("## Variables")
        data.append("| Variable | Value | Threshold | Status |")
        data.append("|----------|-------|---------|----------|")
        for key,value in report.get("statuses").items():
            
            #print("key: " + str(key))
            #print("value: " + str(value))
            item = value.get("status")
            #print("item: " + str(item))
    
            data.append(f'| {key} | {item.get("actual")} | {item.get("threshold")} | {self._format_status(item.get("status"))} | ')
        return "\n".join(data)
    
    def format(self, report):
        
        items = self._format_items(report)

        return items
