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

**Unecryped, do not send personal sensitive info**
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
`/cal {Optional: search next:Choice}`

> AP-Calculus day for today | your next AP-Cal class

params:
- `tmr` Search next : Choice{Day-1, Day-2 =, *null}

return: 
TODAY : {Day_text}
NEXT {Day_text} : {month}. {date}

errors:
- no result : cannot find any result from the website

bug:
- search function may jam when searching (on last few days of a month & there is no class today)

### /map
`/map`

> Show school map

return: {map_image}

### /bell
`/bell`

> Show school bell schedule

return: {bell_image}

### /to_qr
`/to_qr {url:str}, {private:bool = True}`

> make a QR code with a url

params:
- `private` = Return private response. Default to be True

Return:
{url}
By: {user.name}
{QR_code}

error:
- invalid url: this str cannot be tranformed into a QR code via python lib qrcode

## Server
### /invite
`/invite {lifespan:int =48}, {private:bool = True}, {temp:bool = False}`

> generate an invite QR code & url

params:
- `lifespan` = Hours before the code expires. Default to be 48
- `private` = Return private response. Default to be True
- `temp` = Give temporary role. Default to be False

Return:
{url}
{QR_code}

errors:
- no invite permission: caller is not permitted to create invite in this channel

## Clubs
### /volunteer_hours
`/volunteer_hours`

> show a link to log volunteer hours

return:
(link)

error:
`NullValue - There is no link set for you server`

### /volunteer_hours_set
`/volunteer_hours_set`

Perms: `Guild_onwer` OR with role `Admin_Palmbot`
Memory: One slot per Guild
Security: Encrypted

> set a link to show by `/volunteer_hours` in this server

Params:
`url`:str

return:
`successfully added` or `successfully updated`