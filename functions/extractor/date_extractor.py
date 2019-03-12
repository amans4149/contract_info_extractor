import calendar
import re
from collections import OrderedDict
from datetime import datetime

import datefinder
from functions.commons import preprocess


def dates_from_substring(list_of_word_contexts):
    month_list = calendar.month_name
    is_a_date = []
    all_dates = []
    candidate_dates = list(
        datefinder.find_dates(list_of_word_contexts))  # if we use strict=True, our precision is higher,
    # recall is lower
    if not candidate_dates:  # if no candidate date, then say this list of words is not a date
        is_a_date.append(0)
        all_dates.append(0)
    else:
        for candid in candidate_dates:
            # search for month_name / number in numbers_in_context of that sentence
            match_year = re.search('\\s\d{4}\\s', list_of_word_contexts)
            if match_year:
                match_month = re.search('\s+' + month_list[candid.month], list_of_word_contexts)
                if not match_month:
                    match_month = re.search('\s+\d{2}\s+', list_of_word_contexts)
                    if not match_month:  # suppose we get only a 4 digit number as year, we still dont want to go ahead and would
                        # check if we get the month matching within the context
                        is_a_date.append(0)
                        all_dates.append(candid)
                    else:
                        is_a_date.append(1)
                        all_dates.append(candid)
                else:
                    is_a_date.append(1)
                    all_dates.append(candid)
            else:  ##lots of regex :D
                match_full = re.search('\s+(\d{2})(/|-)(\d{2})(/|-|)\d{4}\s+', list_of_word_contexts)
                if not match_full:
                    match_full = re.search('\s+(\d{2})(/|-)(\d{2})(/|-|)\d{2}\s+', list_of_word_contexts)
                    is_a_date.append(0)
                    all_dates.append(0)
                else:
                    is_a_date.append(1)
                    all_dates.append(candid)

    return all_dates, is_a_date


def get_dates_formatted(numbers_in_context, CONTEXT_SIZE=5):
    is_a_date = []
    all_dates = []
    ## DONT PANIC. This variable numbers_in_context is a list of tokens around a token identified as CD. So, we have a huge series of
    #   w-2,w-1,w,w+1,w+2. To pick every w, I iterate through a window of context size and consider every w-2:w+2
    # tokens. The +1 is because of pythons dumbness in not including b if range(a,b) is considered. So to include b, we
    # must use range(a,b+1)
    for m in range(0, int(len(numbers_in_context) / CONTEXT_SIZE) + 1):  # for all candidate_dates

        if m == int(len(numbers_in_context) / CONTEXT_SIZE) + 1:
            context_list = numbers_in_context[m * CONTEXT_SIZE:-1]
        else:
            context_list = numbers_in_context[m * CONTEXT_SIZE:m * CONTEXT_SIZE + CONTEXT_SIZE]

        only_words = []
        for w in range(0, len(context_list)):
            only_words.append(context_list[w][0])

        list_of_word_contexts = " ".join(str(x) for x in only_words)
        few_dates, few_is_a_date = dates_from_substring(list_of_word_contexts)
        all_dates.extend(few_dates)
        is_a_date.extend(few_is_a_date)

    return all_dates, is_a_date


def dates_for_format(list_of_word_contexts):
    candidate_dates = list(datefinder.find_dates(list_of_word_contexts, strict=True))
    if not candidate_dates:
        return '00-00-0000'
    else:
        for candid in candidate_dates:
            return candid.strftime('%d-%m-%Y')


def get_dates(raw_input):
    sentences = preprocess.preprocess(raw_input)
    # numbers_in_context = [preprocess.get_all_numerals(sent) for sent in sentences]
    all_dates = []
    for sent in sentences:
        numbers_in_context = preprocess.get_all_numerals(sent)
        candidate_dates, is_a_date = get_dates_formatted(numbers_in_context)
        for d in range(0, len(is_a_date)):
            if is_a_date[d] == 1:
                new_date = datetime.strptime(str(candidate_dates[d]), "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
                all_dates.append(new_date)
    return list(OrderedDict.fromkeys(all_dates))
