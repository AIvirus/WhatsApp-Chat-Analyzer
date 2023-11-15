# from urlextract import URLExtract
# from wordcloud import WordCloud
# import pandas as pd
# from collections import Counter
# import os
# import emoji


# extract = URLExtract()

# def fetch_stats(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     # fetch number of messages
#     num_messages = df.shape[0]
#     # fetch number of words
#     words = []
#     for message in df['message']:
#         words.extend(message.split())
    
#     # fetch number of media messages
#     num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
#     # fetch number of links shared
#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))

#     return num_messages,len(words),num_media_messages,len(links)

#     '''if selected_user == 'Overall':
#         # fetch number of messages
#         num_messages = df.shape[0]
#         # fetch number of words
#         words = []
#         for message in df['message']:
#             words.extend(message.split())
#         return num_messages,len(words)
#     else:
#         new_df = df[df['user'] == selected_user]
#         num_messages = new_df.shape[0]
#         words = []
#         for message in new_df['message']:
#             words.extend(message.split())
        
#         return num_messages,len(words)'''

# def most_busy_users(df):
#     x = df['user'].value_counts().head()
#     df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'index':'name','user':'percent'})

#     return x,df


# def create_wordcloud(selected_user,df):
    
#     # f = open('C:\\Users\\abc\\Desktop\\application\\WhatsApp-Chat-Analysis\\stop_hinglish.txt', 'r')

#     #import os
#     file_path = os.path.join(os.getcwd(), 'stop_hinglish.txt')
#     f = open(file_path, 'r')

#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     def remove_stop_words(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)    
    
#     wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     temp['message'] = temp['message'].apply(remove_stop_words)
#     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
#     return df_wc


# def most_common_words(selected_user,df):
#     #f = open('stop_hinglish.txt','r')
#     # f = open('C:\\Users\\abc\\Desktop\\application\\WhatsApp-Chat-Analysis\\stop_hinglish.txt', 'r')

#     #import os
#     file_path = os.path.join(os.getcwd(), 'stop_hinglish.txt')
#     f = open(file_path, 'r')

#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

    
#     words = []

#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
    
#     most_common_df = pd.DataFrame(Counter(words).most_common(20))
#     return most_common_df

# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#     return emoji_df

# def monthly_timeline(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
#     timeline['time'] = time
#     return timeline

# def daily_timeline(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     daily_timeline = df.groupby('only_date').count()['message'].reset_index()

#     return daily_timeline

# def week_activity_map(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     return df['day_name'].value_counts()

# def month_activity_map(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     return df['month'].value_counts()

# def activity_heatmap(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

#     return user_heatmap


from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import os
import emoji
import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2} (?:AM|PM|am|pm)? - '

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message-date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # fetch number of messages
    num_messages = df.shape[0]
    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

    '''if selected_user == 'Overall':
        # fetch number of messages
        num_messages = df.shape[0]
        # fetch number of words
        words = []
        for message in df['message']:
            words.extend(message.split())
        return num_messages,len(words)
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        
        return num_messages,len(words)'''

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'index':'name','user':'percent'})

    return x,df


def create_wordcloud(selected_user,df):
    
    # f = open('C:\\Users\\abc\\Desktop\\application\\WhatsApp-Chat-Analysis\\stop_hinglish.txt', 'r')

    # import os
    file_path = os.path.join(os.getcwd(), 'stop_hinglish.txt')
    f = open(file_path, 'r')

    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)    
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    #f = open('stop_hinglish.txt','r')
    f = open('C:\\Users\\abc\\Desktop\\application\\WhatsApp-Chat-Analysis\\stop_hinglish.txt', 'r')

    #import os
    # file_path = os.path.join(os.getcwd(), 'stop_hinglish.txt')
    # f = open(file_path, 'r')

    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap

