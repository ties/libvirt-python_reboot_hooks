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

    if not dom.autostart():
        log.debug("{} should not be auto started, skipping.".format(vm_name))
        continue

    if major != 1 and (major, minor) != (3, 2):
        dom.create()
        resumed.add(dom)
        log.info("Restoring domain {}".format(vm_name))
    elif (major, minor) == (3, 2):
        resumed.add(dom)
    else:
        log.info("domain {} is already running.".format(vm_name))

# Sleep 60 seconds, to make sure resume finished.
time.sleep(60)

# TODO: Does this trigger a guest-agent resume signal?
for dom in resumed:
    log.info("resume {}".format(dom.name()))
    try:
        dom.resume()
    except:
        log.exception('Error when resuming {}'.format(dom.name()))

    try:
        dom.pMWakeup()
    except:
        log.exception("error in pMWakeup")
