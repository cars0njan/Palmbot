# Palmbot
_This is a_ .md  file_

## System commands
### /ping
`/ping`
> check if bot is online | bot latency

return:
{latency} ms. Bot is online.

errors:
- no retrun: bot is offline

### /feedback
`/feedback {type:choice} {content:str} {Optional: attachment:file}`

**Unecryped, do not send personal info**
> suggest new functions | report bugs | other feedback

params:
- `type` Type of feedback : Choice{"Report bug", "Suggest functions", "Others"}
- `content` The main body of your feedback : Str
- `file` Any files you want to attach to support your feedback : file

return:
Your response has been sent. Thank you.

errors:
- discord.not a valid choice: choice for `type` not in list
- discord.this field is required: required field is not filled
- long content: string input for `content` exceed 2000 characters
- large file: file input for `file` exceed 10MB
- unknown error: cannot log your response. Please try later or use `/contact` function

### /contact
`/contact`

> contact developer(s)

return: 

To contact the developer, please email `sc.carson.jan@gmail.com`

*To suggest new functions or report bugs, please use the* `feedback` *command instead*

### /docs
`/docs`

> see docunmentation

return:

There are two ways to see docunmentation.

Method 1: download `.md` file attached and read with a Markdown editor.

Method 2: go to palmbot.cars0njan.repl.co for a plain-text version.

{file}

## Utilities
### /ap_cal
`/cal {Optional: tmr:Bool = False}`

> Is AP-Calculus today/tomorrow day-1 or day-2?

params:
- `tmr` Check for tomorrow : Bool (default to be False)

return: 
{month}. {date} - Day {day_num}

errors:
- no result : cannot find any result from the website
- too many results : mistakenly find more than one result from the website

