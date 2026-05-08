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