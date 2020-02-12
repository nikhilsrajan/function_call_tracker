# function_call_tracker
Set of codes to track function calls in a project

This was something that I made to understand how a software in a company I am working at worked. To know in what order functions are being called - a visual after-the-fact debugger of sorts. This was on the company's GitLab, and now I have shifted it to my GitHub.

My last update on it was on 31 Dec 2019.

There are plans to make improvements in it as currently it is tuned to the company's codebase.

## Known Issues:
- Concurrency while printing message into the log file.
- Robustness of function decalaration identifier.
- Readability of ```lineadder``` function.