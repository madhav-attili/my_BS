#!/usr/bin/env python

import json
import logging
import os
import requests
import sys
import unittest

class PfizerHtaccessTestCase(unittest.TestCase):
    """
    Tests Pfizer's .htaccess rules.
    """

    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.tests_dir = os.path.join(base_dir, 'tests')
        apache_dir = os.path.join(base_dir, 'apache_rules')
        docroot = os.path.join(base_dir, 'docroot')

        if not os.path.exists(docroot):
            os.mkdir(docroot)

        self._create_index(docroot)
        self._generate_htaccess(apache_dir, docroot)

    def test_public(self):
        """
        Tests .htaccess rules on public URLs
        """
        file_name = 'tests.json'
        self.tests = self._load_tests(self.tests_dir, file_name)
        for test in self.tests['tests']:
            self._check_rule(test)

    def test_pfizer(self):
        """
        Tests .htaccess rules for pfizer IPs on public URLs
        """
        file_name = 'tests_pfizer_ips.json'
        self.tests = self._load_tests(self.tests_dir, file_name)
        for test in self.tests['tests']:
            headers = {"AH-Client-IP": '155.94.70.193'}
            self._check_rule(test, headers)

    def test_vendor(self):
        """
        Tests .htaccess rules for pfizer vendor IPs on public URLs
        """
        file_name = 'tests_vendor_ips.json'
        self.tests = self._load_tests(self.tests_dir, file_name)
        for test in self.tests['tests']:
            headers = {"AH-Client-IP": '82.140.10.138'}
            self._check_rule(test, headers)

    def _check_rule(self, test, headers=None):
        """
        Validate each test case with rule present in .htaccess

        :param test: each test case present in respective json file
        :type test: dict
        :param headers: custom apache headers needs to be send with each request
        :type headers: str
        :rtype: None
        """

        response = requests.get(self._generate_full_url(test['path']), allow_redirects=False, headers=headers)
        logging.debug("Checked '%s'. Response: %s. Excepted: %s", test['path'], response.status_code, test['status'])
        self.assertEqual(response.status_code, test['status'], 'Incorrect status code')
        if response.status_code in [301, 302]:
            url = self._generate_full_url(test['destination'])
            self.assertEqual(response.headers['Location'], url, 'Incorrect destination')

    def _create_index(self, docroot):
        """
        Creates an index.php file.

        :param docroot: The server docroot that the file will be placed in.
        :type docroot: str.
        :rtype: None.
        """
        fp = open(os.path.join(docroot, 'index.php'), 'w')
        # I know I could skip the PHP tag and just output OK, but I want to do it this way.
        fp.write('<?php echo "OK"; ?>')
        fp.close()

    def _generate_full_url(self, path):
        """
        Generates a full url from a full path.

        :param path: The path to be used.
        :type path: str.
        :return: The generated URL.
        :rtype: str.
        """
        return "".join(['http://localhost', path])


    def _generate_htaccess(self, source_path, docroot):
        """
        Generates an Apache .htaccess file for testing.

        :param source_path: The path that contains the source rules.
        :type source_path: str.
        :param docroot: The target docroot for the generated file.
        :type docroot: str.
        :rtype: None.
        """
        htaccess_parts = ['SetEnvIfNoCase ^AH-Client-IP$ "(.+)" AH_Client_IP=$1']

        gr_fp = open(os.path.join(source_path, 'apache_custom_global-common-1.1.conf'))
        htaccess_parts.append(gr_fp.read())
        gr_fp.close()

        ipw_fp = open(os.path.join(source_path, 'login_allowed_ips.conf'))
        htaccess_parts.append(ipw_fp.read())
        ipw_fp.close()

        response = requests.get('http://cgit.drupalcode.org/drupal/plain/.htaccess', params={'h': '7.x'})
        htaccess_parts.append(response.text.encode('ascii', 'ignore'))

        htaccess = open(os.path.join(docroot, '.htaccess'), 'w')
        htaccess.write("\n".join(htaccess_parts))
        htaccess.close()

    def _load_tests(self, base_path, file_name):
        """
        Fetches the tests from disk.

        :param base_path: The base path for the tests.
        :type base_path: str.
        :param file_name: Name of file contains tests.
        :type file_name: str.
        :return: The tests to be run.
        :rtype: list.
        """
        tests_fp = open(os.path.join(base_path, file_name))
        tests = json.load(tests_fp)
        return tests

    def tearDown(self):
        """
        Cleanup all variables
        """
        del self.tests_dir
        del self.tests

if __name__ == '__main__':
    # Debug HTTP requests.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.addHandler(logging.StreamHandler(sys.stdout))
    requests_log.propagate = True

    unittest.main()
