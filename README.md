# "Suspend VM's ICE" scripts
One of my machines runs multiple KVM vm's.

When the host needs to reboot i suspend the vm's first using this quick and
dirty script.

After the reboot there is some time skew in the vm's (they continue at the time
 of the suspend). You either need to use one of these solutions:
  * Send a message using qemu-guest-agent. I did not find host support for
      this, and the libvirt python api does not allow it
  * reboot the vm's. They will pickup the correct time...
  * manually stop ntp (service stop ntp) and let ntpd fix the time with a large
       step (ntpd -gq)
  * setup ntp to skew the clock faster

The preferred clocksource for KVM/qemu is kvm-clock. Unfortunately this clock
source does not allow for a policy to be setup where the guest clock ticks are
merged or the clock catches up.

[Red Hat](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Virtualization_Administration_Guide/sect-Virtualization-Tips_and_tricks-Libvirt_Managed_Timers.html)
provides a lot of background on these clocksources.
  
Since I don't reboot often I have not tried this yet.
