# qbt_queue_controller

This python scheduled container helps you to manage your qbt queue. It's implementation remains quite basic:

1. If there is enough space, downloads are resumed
2. If space is low, downloads are paused, and a ping is sent to healthchecks.io
