# System commands
## /ping
`/ping`
> check if bot is online | bot latency

return: {latency} ms. Bot is online.

errors:
- no retrun: bot is offline

## /feedback
`/feedback {type:choice} {content:str} {Optional: attachment:file}`

**Unecryped, do not send personal info**
> suggest new functions | report bugs | other feedback

perms:
- `type` Type of feedback : Choice{"Report bug", "Suggest functions", "Others"}
- `content` The main body of your feedback : Str
- `file` Any files you want to attach to support your feedback : file

return: Your response has been sent. Thank you.

errors:
- discord.not a valid choice: choice for `type` not in list
- discord.this field is required: required field is not filled
- long content: string input for `content` exceed 2000 characters
- large file: file input for `file` exceed 10MB
- unknown error: cannot log your response. Please try later or use `/contact` function


## /contact
`/contact`

> contact developer(s)

return: 

To contact the developer, please email `sc.carson.jan@gmail.com`

*To suggest new functions or report bugs, please use the* `feedback` *command instead*


