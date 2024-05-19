from ansible.module_utils.basic import AnsibleModule
import re



def get_os_info():
    '''Get os information from '/etc/os-release'
    '''

    os_release_path = '/etc/os-release'

    name_pattern = re.compile(r'^NAME=["\']?([^"\']+)["\']?$')
    version_pattern = re.compile(r'^VERSION=["\']?([^"\']+)["\']?$')

    with open(os_release_path) as file:
        for line in file:
            line = line.strip()

            os_name_match = name_pattern.match(line)
            os_version_match = version_pattern.match(line)

            if os_name_match:
                os_name = os_name_match.group(1)
            elif os_version_match:
                os_version = os_version_match.group(1)

    return os_name, os_version



def verify_os_info(os_name, os_version):
    '''Compare the os information which is got from the user and '/etc/os-release'.
    '''

    actual_os_name, actual_os_version = get_os_info()

    if os_name == actual_os_name:
        if os_version == '':
            message = 'It is correct.'
        elif os_version == actual_os_version:
            message = 'It is correct.'
        else:
            message = 'It is wrong.'
    else:
        message = 'It is wrong.'

    return message



def main():
    module = AnsibleModule(
        argument_spec=dict(
            os_name=dict(type='str', required=True),
            os_version=dict(type='str', required=False, default=''),
        ),
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(
            changed=False,
            message='It is correct.',
        )

    message = verify_os_info(module.params['os_name'], module.params['os_version'])

    actual_os_name, actual_os_version = get_os_info()

    if module.check_mode or 'correct' in message:
        module.exit_json(
            changed=False,
            message=message,
            actual_os_name_on_managed_node=actual_os_name,
            actual_os_version_on_managed_node=actual_os_version,
        )
    else:
        module.fail_json(
            msg=message,
            changed=False,
            expected_os_name=module.params['os_name'],
            expected_os_version=module.params['os_version'],
            actual_os_name_on_managed_node=actual_os_name,
            actual_os_version_on_managed_node=actual_os_version,
        )

if __name__ == '__main__':
    main()
