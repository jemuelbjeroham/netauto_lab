#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json
import re

def extract_user_logins(logs):
    lines = logs.split("\n")
    log_info_list = []
    for line in lines:
        user_match = re.search(r'\[user: (\w+)\]', line)
        status_match = re.search(r'LOGIN_(SUCCESS|FAILED)', line)
        ip_match = re.search(r'\[Source: ([\d\.]+)\]', line)
        local_port_match = re.search(r'\[localport: (\d+)\]', line)
        time_match = re.search(r'at ([^\n]+)$', line)
        if user_match and status_match and ip_match and local_port_match and time_match:
            log_info = {
                "user": user_match.group(1),
                "status": status_match.group(1),
                "ip": ip_match.group(1),
                "local_port": local_port_match.group(1),
                "time": time_match.group(1)
            }
            log_info_list.append(log_info)
    return log_info_list

def main():
    module = AnsibleModule(
        argument_spec=dict(
            logs=dict(type='str', required=True)
        )
    )

    logs = module.params['logs']
    try:
        user_logins = extract_user_logins(logs)
        module.exit_json(changed=False, logs=user_logins)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()