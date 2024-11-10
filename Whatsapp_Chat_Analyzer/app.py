import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
#uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

   # fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group _notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        #stats area
        st.title('Top Statistics')
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
        with col4:
            st.header('Links Shared')
            st.title(num_links)
            #monthly_timeline
            st.title('Monthly Timeline')
            timeline=helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline['time'],timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            #daily_timeline
            st.title('Daily Timeline')
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            #activity
            st.title('Activity Map')
            col1,col2=st.columns(2)
            with col1:
                st.header('Most_busy_day')
                busy_day=helper.weak_activity_map(selected_user,df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header('Most_busy_month')
                busy_month = helper.monthly_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            st.title('weekly_activity_map')
            activity_heatmap=helper.activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax=sns.heatmap(activity_heatmap)
            st.pyplot(fig)

            #finding the busiest user in the group
            if selected_user=='Overall':
                st.title('Most Busy Users')
                x,new_df=helper.most_busy_user(df)
                fig,ax=plt.subplots()

                col1,col2=st.columns(2)
                with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.header('Percentage')
                    st.dataframe(new_df)
            #wordcloud
            st.title('WorDCloud')
            df_wc=helper.create_wordcloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
            most_common_df=helper.most_common_words(selected_user,df)
            st.dataframe(most_common_df)
            fig,ax=plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1],color='red')
            st.title('Most Common Words')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            #emoji Analysis
            emoji_df=helper.emoji_helper(selected_user,df)
            st.title('Emoji')
            col1,col2=st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax=plt.subplots()
                ax.pie(emoji_df[1],labels=emoji_df[0],autopct='%.2f')
                st.pyplot(fig)


