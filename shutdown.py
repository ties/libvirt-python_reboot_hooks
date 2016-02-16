#!/usr/bin/env python
import libvirt
import logging
import logging.handlers

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')
logging.getLogger().addHandler(handler)

conn = libvirt.open(None)

#  For all machines:
for dom in conn.listAllDomains():
    major, minor = dom.state()
    vm_name = dom.name()

    if major == 1:
        log.info("{} is running".format(vm_name))

        try:
            dom.managedSave(0)
        except:
            log.exception("managedsave failure for {}".format(vm_name))
