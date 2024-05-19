test
=========

Test `test` module and `test` action plugin.

Example Playbook
----------------

Here is an example playbook on how to use this role.

---

- hosts: all
  tasks:
    - name: Verify os info
      ansible.builtin.include_role:
        name: test

Author Information
------------------

TechLabSatoru
