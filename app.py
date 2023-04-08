import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.title("WhatsApp Chat Analyzer")
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    chats = preprocessor.preprocess(data)

    # fetch unique users
    user_list = chats['sender'].unique().tolist()
    # user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Chat Records")

        if selected_user == "Overall":
            st.dataframe(chats)
        else:
            chats = chats[chats["sender"] == selected_user]
            st.dataframe(chats)
        total_messages, total_words, media_shared, total_links = helper.fetch_stats(selected_user, chats)
        # total_words = helper.fetch_stats(selected_user, chats)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Media Shared")
            st.title(media_shared)
        with col4:
            st.header("Links Shared")
            st.title(total_links)

        if selected_user == "Overall":
            most_active, active_user_df = helper.most_active_users(chats)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Active Users")
                ax.barh(most_active.index, most_active.values, color="maroon")
                for s in ['top', 'bottom', 'right']:
                    ax.spines[s].set_visible(False)
                st.pyplot(fig)

            with col2:
                st.header("Message Percent")
                st.dataframe(active_user_df)

        # draw wordcloud
        st.title("WordCloud")
        chats_wc = helper.create_wordCloud(selected_user, chats)
        fig, ax = plt.subplots()
        ax.imshow(chats_wc)
        st.pyplot(fig)

        # most common words
        st.title("Frequent Words")
        common_words_df = helper.most_common_words(selected_user, chats)

        fig, ax = plt.subplots()
        ax.barh(common_words_df["word"], common_words_df["frequency"])
        for s in ['top', 'bottom', 'right']:
            ax.spines[s].set_visible(False)
        st.pyplot(fig)


        #emoji analysis

        emoji_df = helper.emoji_count(selected_user, chats)

        col1, col2 = st.columns(2)

        with col1:
            st.title("Emoji Analysis")
            st.dataframe(emoji_df)

        with col2:
            st.title("Pie-Chart")
            fig, ax = plt.subplots()
            # ax.pie(emoji_df[0], labels=emoji_df[1])
            colors = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7", "#2E5B88"]
            ax.pie(emoji_df["frequency"].head(), labels=emoji_df["emoji"].head(), autopct='%1.1f%%', colors=colors, textprops={'fontsize': 10}, wedgeprops={"linewidth": 1, "edgecolor": "white"})
            # plt.pie()
            st.pyplot(fig)


        #Monthly-Timeline
        st.title("Monthly Timeline")
        monthly_timeline_df = helper.monthly_timeline(selected_user, chats)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline_df["Month-Year"], monthly_timeline_df["message"], marker='o', color="maroon")
        plt.setp(ax.get_xticklabels(), rotation=45)
        ax.spines[['right', 'top']].set_visible(False)
        ax.set(xlabel="Month_Year",
               ylabel="Message Count");
        st.pyplot(fig)

        #Daily-Timeline
        st.title("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(selected_user, chats)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_df["only_date"], daily_timeline_df["message"])
        plt.setp(ax.get_xticklabels(), rotation=45)
        ax.spines[['right', 'top']].set_visible(False)
        ax.set(xlabel="Months",
               ylabel="Message Count");
        st.pyplot(fig)

# streamlit run app.py