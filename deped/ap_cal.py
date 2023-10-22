async def ap_cal(
    interaction:discord.Interaction #,
    #search_next : Literal['Day 1', 'Day 2'] = None
):
    current_month = fx.datetime_van().strftime('%b')
    current_day = int(fx.datetime_van().strftime('%d'))

    r = requests.get('https://whmkwan.wixsite.com/math/ap-calculus')
    text = BS(r.text, features='html.parser').prettify()
    soup = BS(text, 'html.parser')

    p_spans = soup.find_all('p')
    h6_spans = soup.find_all('h6')
    spans = p_spans + list(set(h6_spans) - set(p_spans))

    span_text =[]
    for i in spans:
        i = i.text.strip()
        if (' - Day 1' in i) or (' - Day 2' in i):
            span_text.append(i.lower())

    current_str = f'{current_month}. {current_day} -'.lower()
    def search_today(span_text):
        for i in span_text:
            if i.startswith(current_str):
                return i
        return 'No-Class'

    #if search_next == None:
    today_str = search_today(span_text)
    await interaction.response.send_message(f'AP-Calculus\nToday: **{today_str.title()}**', ephemeral=True)
    fx.stats()
    return

    # month_mapping = {
    #     'jan.': 1, 'feb.': 2, 'mar.': 3, 'apr.': 4, 'may': 5, 'jun.': 6,
    #     'jul.': 7, 'aug.': 8, 'sept.': 9, 'oct.': 10, 'nov.': 11, 'dec.': 12
    # }

    # def sort_key(span_text):
    #     month, day_description = span_text.split(' - ')
    #     month, day = month.split(' ')
    #     return (int(month_mapping[month]), int(day.split('.')[0]), day_description)

    # span_text = sorted(span_text, key=sort_key)

    # def with_prefix(list):
    #     for plus in range(0,5):
    #         for index, i in enumerate(list):
    #             if i.startswith(f'{current_month}. {current_day+plus} -'.lower()):
    #                 return index +1
    #     return None

    # if with_prefix(span_text) == None:
    #     await interaction.response.send_message('error - no result', ephemeral=True)
    #     return
    # for i in range(with_prefix(span_text),len(span_text)):
    #     if search_next.lower() in span_text[i]:
    #         today_str = search_today(span_text) or 'no-class'
    #         next_str = span_text[i]
    #         await interaction.response.send_message(f'AP-Calculus\n\nToday: **{today_str.title()}**\nNext: **{next_str.title()}**', ephemeral=True)
    #         fx.stats()
    #         return
    # await interaction.response.send_message('error - no result', ephemeral=True)
    # return

tree.add_command(ap_cal)