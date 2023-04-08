import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, chats):
    if selected_user != "Overall":
        chats = chats[chats["sender"] == selected_user]

    overall_msgs = chats.shape[0]

    words = []
    for word in chats['message']:
        words.extend(word.split(" "))
    total_words = len(words)

    try:
        media_shared = chats["message"].value_counts()["<Media omitted>"]
    except Exception as e:
        media_shared = 0
    links = []
    for messages in chats["message"]:
        links.extend(extractor.find_urls(messages))
    total_links = len(links)

    return overall_msgs, total_words, media_shared, total_links


def most_active_users(chats):
    active_users = chats["sender"].value_counts().head()
    active_user_df = round((chats["sender"].value_counts() / chats.shape[0]) * 100, 2).reset_index().rename(
        columns=({"index": "sender", "sender": "percentage"}))

    return active_users, active_user_df


def create_wordCloud(selected_uer, chats):
    file = open("Hindi-English Stopwords.txt", "r")
    stop_words = file.read()

    if selected_uer != "Overall":
        chats = chats[chats["sender"] == selected_uer]

    messages = chats["message"][chats["message"] != "<Media omitted>"][chats["message"] != "This message was deleted"]
    filter = []
    for message in messages:
        for word in message.split():
            if word.lower() not in stop_words:
                filter.append(word)
    filtered_text = " ".join(filter)
    wc = WordCloud(background_color="white", colormap="plasma")
    chats_wc = wc.generate(filtered_text)
    return chats_wc


def most_common_words(selected_user, chats):
    file = open("Hindi-English Stopwords.txt", "r")
    stop_words = file.read()

    if selected_user != "Overall":
        chats = chats[chats["sender"] == selected_user]

    messages = chats["message"][chats["message"] != "<Media omitted>"][chats["message"] != "This message was deleted"]

    common_words = []

    for message in messages:
        for word in message.split():
            if word.lower() not in stop_words:
                common_words.append(word)

    common_words_df = pd.DataFrame(Counter(common_words).most_common(20))
    common_words_df.columns = ["word", "frequency"]
    return common_words_df


def emoji_count(selected_user, chats):
    if selected_user != "Overall":
        chats = chats[chats["sender"] == selected_user]

    emojis = []
    emojis.extend(symbol for symbol in chats["message"] if symbol in emoji.EMOJI_DATA)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    emoji_df.columns = ["emoji", "frequency"]

    return emoji_df


def monthly_timeline(selected_user, chats):
    if selected_user != "Overall":
        chats = chats[chats["sender"] == selected_user]

    chats["month_name"] = chats["date"].dt.month_name()

    monthly_timeline_df = chats.groupby(["year", "month", "month_name"]).count()["message"].reset_index()

    month_year = []
    for i in range(len(monthly_timeline_df)):
        month_year.append(monthly_timeline_df["month_name"][i] + " - " + str(monthly_timeline_df["year"][i]))

    monthly_timeline_df["Month-Year"] = month_year

    return monthly_timeline_df


def daily_timeline(selected_user, chats):
    if selected_user != "Overall":
        chats = chats[chats["sender"] == selected_user]

    chats["only_date"] = chats["date"].dt.date
    daily_timeline_df = chats.groupby(["only_date"]).count()["message"].reset_index()

    return daily_timeline_df