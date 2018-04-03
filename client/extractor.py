#!/usr/bin/env python3

import re
import os

import magic

class Extractor():
    def __init__(self):
        # This list is referencing https://github.com/zricethezav/gitleaks/blob/4b21bbef2e40ad345491e449e098a91d6074d5ce/main.go
        self.regexes = [
            ("PKCS8", re.compile("-----BEGIN PRIVATE KEY-----")),
            ("RSA",   re.compile("-----BEGIN RSA PRIVATE KEY-----")),
            ("SSH",   re.compile("-----BEGIN OPENSSH PRIVATE KEY-----")),
            ("Facebook", re.compile("(?i)facebook.*['|\"][0-9a-f]{32}['|\"]")),
            ("Twitter", re.compile("(?i)twitter.*['|\"][0-9a-zA-Z]{35,44}['|\"]")),
            ("Github", re.compile("(?i)github.*[['|\"]0-9a-zA-Z]{35,40}['|\"]")),
            ("AWS",   re.compile("AKIA[0-9A-Z]{16}")),
            ("Reddit",re.compile("(?i)reddit.*['|\"][0-9a-zA-Z]{14}['|\"]")),
            ("Heroku",re.compile("(?i)heroku.*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}"))
        ]

        self.magi = magic.Magic(mime=True)

    def _is_in_blacklist(self, file_name):
        blacklist = ['node_modules', 'test']
        for black in blacklist:
            if black in file_name:
                return True
        return False

    def get_sensitive_files(self, directory):
        all_files_found = []
        old_root = ''
        for root, _, files in os.walk(directory):
            if self._is_in_blacklist(root):
                continue
            for file in files:
                file_name = os.path.join(root, file)
                print(file_name)
                try:
                    if self.magi.from_file(file_name) != 'text/plain':
                        continue
                    with open(file_name, 'r') as f:
                        file_contents = f.read()
                        for r in self.regexes:
                            result = re.findall(r[1], file_contents)
                            if len(result) != 0:
                                all_files_found.append(file_name)
                except KeyboardInterrupt:
                    raise SystemExit
                except:
                    continue
        return all_files_found
