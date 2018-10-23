#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals

import platform as pf

from . import core


class PlatformCollector(object):
    """Collector for python platform information"""

    def __init__(self, namespace='', registry=core.REGISTRY, platform=None):
        self._namespace = namespace
        self._prefix = namespace + '_python_' if namespace else 'python_'
        self._platform = pf if platform is None else platform
        info = self._info()
        system = self._platform.system()
        if system == "Java":
            info.update(self._java())
        self._metrics = [
            self._add_metric(self._prefix + "info", "Python platform information", info)
        ]
        if registry:
            registry.register(self)

    def collect(self):
        return self._metrics

    @staticmethod
    def _add_metric(name, documentation, data):
        labels = data.keys()
        values = [data[k] for k in labels]
        g = core.GaugeMetricFamily(name, documentation, labels=labels)
        g.add_metric(values, 1)
        return g

    def _info(self):
        major, minor, patchlevel = self._platform.python_version_tuple()
        return {
            "version": self._platform.python_version(),
            "implementation": self._platform.python_implementation(),
            "major": major,
            "minor": minor,
            "patchlevel": patchlevel
        }

    def _java(self):
        java_version, _, vminfo, osinfo = self._platform.java_ver()
        vm_name, vm_release, vm_vendor = vminfo
        return {
            "jvm_version": java_version,
            "jvm_release": vm_release,
            "jvm_vendor": vm_vendor,
            "jvm_name": vm_name
        }


PLATFORM_COLLECTOR = PlatformCollector()
"""PlatformCollector in default Registry REGISTRY"""
