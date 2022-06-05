# Simple Polling App Django

A simple polling app that can quickly create, share and vote polls without any login.

**How this works?**
1. Whenever a new poll is created, a unique poll ID is generated. This poll ID is used to identify the poll for sharing/voting and viewing results.
2. While voting the poll from voting/respond url, a unique response ID cookie is generated to create a user session. This is to identify a user responding to poll and prevent duplicate polling.
3. Other than response ID, no information is stored about a user. This makes a poll voting complete anonymous.
4. All polls created are valid for 5 days, after that the poll is disabled. This is achieved by poll_cleaner script running in background. The data for all polls is retained.
5. All requests and data changes in database are logged in log files.

