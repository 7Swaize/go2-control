## Receiving `PublishSubscribeOpenError(UnableToOpenDynamicServiceInformation)` Error

There are stale resources that need to be cleaned up. Usually this is done automatically via Icoryx2 internal.
However, if cleanup didn't happen automatically, we must remove stale resources.

We provided a script to do that for you.

Linux:

```bash
bash ./go2-control/scripts/unix/clear_iceoryx_caches.sh
``` 

Windows:

Execute the `go2-control/scripts/windows/clear_iceoryx_caches.bat` script. You may need to run it as administrator.


## Can I create multiple `Go2Controller` instances? 

Maybe. Currently, no guarantees are made about using multiple `Go2Controller` instances within the same process.
While it may work in some configurations, it has not been thoroughly tested, and you may encounter issues with IPC via `Iceoryx2`.
Furthermore, no guarantees are made about using `Go2Controller` instances across **multiple processes** (for the same reasons).

For now, it is recommended to have only one instance of the `Go2Controller` alive across your whole system.
Support for multiple instances across processes is being considered, but it is not currently a priority.
If there is sufficient demand or a stronger use case, it can become a higher-priority feature in the future.