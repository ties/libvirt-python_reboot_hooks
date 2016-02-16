#!/usr/bin/env python
import libvirt
import time
import logging
import logging.handlers

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')
logging.getLogger().addHandler(handler)

conn = libvirt.open(None)

# Machines that have been resumed
resumed = set()

for dom in conn.listAllDomains():
    major, minor = dom.state()
    vm_name = dom.name()

    if major != 1:
        if dom.autostart():
            dom.create()
            resumed.add(dom)
            log.info("Restoring domain {}".format(vm_name))
        else:
            log.debug("{} should not be auto started, skipping.".format(vm_name))
    else:
        log.info("domain {} is already running.".format(vm_name))

# Sleep 60 seconds, to make sure resume finished.
time.sleep(60)

# TODO: Does this trigger a guest-agent resume signal?
for dom in resumed:
    log.info("resume {}".format(dom.name()))
    dom.resume()    
