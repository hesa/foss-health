import json
import logging

class RepoAnalyzer:

    def __init__(self, report, thresholds=None):
        logging.debug(f'report data: {json.dumps(report, indent=4)}')
        self.report = report
        
        self.thresholds = thresholds

    def _check_value(self, key):
        logging.debug(f'compare:')
        logging.debug(f'       : key    {key}')
        logging.debug(f'       : report {self.report}')
        logging.debug(f'       : expr   {self.report[key]} >= {self.thresholds[key]}')
        return {
            "check": key,
            'status': {
                "actual":  self.report[key],
                "threshold":  self.thresholds[key],
                "status": int(self.report[key]) >= int(self.thresholds[key])
            }
        }
    
    def check(self):
        statuses = {}
        status = True
        for check in self.thresholds.keys():
            result = self._check_value(check)
            status = status and result['status']['status']
            statuses[check] = result
        
        return {
            'repository': self.report['repository'],
            'statuses': statuses,
            'status': status
        }
