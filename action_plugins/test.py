from ansible.plugins.action import ActionBase
import re



class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)

        module_args = self._task.args.copy()
        result = self._execute_module(
            module_name = 'test',
            module_args = module_args,
            task_vars = task_vars,
            tmp = tmp,
        )

        # Get parameters.
        os_name = self._task.args.get('os_name', '')
        os_version = self._task.args.get('os_version', '')

        # If the user exec with check mode.
        if self._play_context.check_mode:
            return {
                'changed': False,
                'message': 'It is correct.'
            }

        # Verify the os information.
        message = self.verify_os_info(os_name, os_version)

        # Get actual os information on Control Node.
        expected_os_name, expected_os_version = self.get_os_info()

        if 'correct' in message:
            result.update({
                'changed': False,
                'message': message,
                'expected_os_name_on_control_node': expected_os_name,
                'expected_os_version_on_control_node': expected_os_version,
            })
        else:
            result.update({
                'failed': True,
                'changed': False,
                'message': message,
                'expected_os_name_on_control_node': expected_os_name,
                'expected_os_version_on_control_node': expected_os_version,
            })

        return result



    def get_os_info(self):
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



    def verify_os_info(self, os_name, os_version):
        '''Compare the os information which is got from the user and '/etc/os-release'.
        '''

        expected_os_name, expected_os_version = self.get_os_info()

        if os_name == expected_os_name:
            if os_version == '':
                message = 'It is correct.'
            elif os_version == expected_os_version:
                message = 'It is correct.'
            else:
                message = 'It is wrong.'
        else:
            message = 'It is wrong.'

        return message
