# SETUP: VIRTUAL ENVIRONMENT
## for environment variables
from dotenv import load_dotenv
import os

## for chatbot functionalities
import telebot
from string import Template
import emoji
from gtts import gTTS

## for data analysis
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# SETUP: TELEGRAM BOT API TOKEN
load_dotenv()
TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)


# -------------------- CHECKPOINT 1 --------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # TO DO: chat_id, full_name, message_text
    chat_id = message.from_user.id

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = f'{first_name} {last_name}' if last_name is not None else first_name
    
    # TO DO: subtitute text with variable
    with open('template_text/welcome.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        temp = Template(content)
        welcome = temp.substitute(FULL_NAME = full_name)

    bot.send_message(
        chat_id,
        welcome,
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['about'])
def send_about(message):
    # TO DO: chat_id
    chat_id = message.from_user.id

    # TO DO: subtitute text with static values
    with open('template_text/about.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        temp = Template(content)
        about = temp.substitute(
            STUDENT_NAME = "Rizki Aldiansyah",
            BATCH_ACADEMY = "Vulcan",
            GITHUB_REPO_LINK = "https://github.com/rizkialldiansyah"
        )

    bot.send_message(
        chat_id,
        about,
        parse_mode='Markdown'
    )


# -------------------- CHECKPOINT 2 --------------------
# TO DO: read data and convert data type
df = pd.read_csv("./data_input/facebook_ads_v2.csv", parse_dates=["reporting_date"])

# TO DO: get unique values of campaign_id
df['campaign_id'] = df['campaign_id'].astype('str')
unique_campaign = df['campaign_id'].unique()

# TO DO: change the data type of ad_id, age, and gender
df['ad_id'] = df['ad_id'].astype('str')
category_dtype = ['age', 'gender']

for i in category_dtype:
    df[i] = df[i].astype('category')

@bot.message_handler(commands=['summary'])
def ask_id_summary(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    chat_id = message.from_user.id

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in unique_campaign:
        markup.add(i)
    sent = bot.send_message(chat_id, 'Choose campaign to be summarized:', reply_markup=markup)

    bot.register_next_step_handler(sent, send_summary)

def send_summary(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    chat_id = message.from_user.id
    selected_campaign_id = message.text

    if selected_campaign_id in unique_campaign:
        # TO DO: find the range date
        df_campaign = df.loc[df['campaign_id'] == selected_campaign_id]
        
        start_date = df_campaign['reporting_date'].min().strftime(format="%d %b %y")
        end_date = df_campaign['reporting_date'].max().strftime(format="%d %b %y")
        
        # TO DO: perform calculation
        total_spent = int(df_campaign['spent'].sum())
        total_conversion = int(df_campaign['total_conversion'].sum())
        cpc = round(total_spent/total_conversion, 1)

        # TO DO: subtitute text with variables
        with open('template_text/summary.txt', mode='r', encoding='utf-8') as f:
            content = f.read()
            temp = Template(content)
            summary = temp.substitute(
                CAMPAIGN_ID = selected_campaign_id,
                START_DATE = start_date,
                END_DATE = end_date,
                TOTAL_SPENT = total_spent,
                TOTAL_CONVERSION = total_conversion,
                CPC = cpc
            )

        bot.send_message(chat_id, summary)
    else:
        bot.send_message(chat_id, 'Campaign ID not found. Please try again!')
        ask_id_summary(message)


# -------------------- CHECKPOINT 3 --------------------
@bot.message_handler(commands=['plot'])
def ask_id_plot(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    chat_id = message.from_user.id

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in unique_campaign:
        markup.add(i)
    sent = bot.send_message(chat_id, 'Choose campaign to be visualized:', reply_markup=markup)

    bot.register_next_step_handler(sent, send_plot)

def send_plot(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    chat_id = message.from_user.id
    selected_campaign_id = message.text

    if selected_campaign_id in unique_campaign:
        # TO DO: prepare data for visualization
        df_campaign = df.loc[df['campaign_id'] == selected_campaign_id]
        df_plot = df_campaign.groupby('age').agg({'spent': 'sum', 'approved_conversion': 'sum'})
        df_plot['cpc'] = df_plot['spent'] / df_plot['approved_conversion']
        
        # TO DO: visualization

        # prepare 3 subplots vertically
        fig, axes = plt.subplots(3, sharex=True, dpi=300)

        # create frameless plot
        for ax in axes:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

        # first subplot: total spent per age group
        axes[0].bar(df_plot.index, df_plot['spent'], color='#AE2024')
        axes[0].set_ylabel("Total Spent", fontsize=8)

        # second subplot: total approved conversion per age group
        axes[1].bar(df_plot.index, df_plot['approved_conversion'], color='#000000')
        axes[1].set_ylabel("Total Approved Conversion", fontsize=8)

        # third subplot: average CPC per age group
        axes[2].bar(df_plot.index, df_plot['cpc'], color='#AE2024')
        axes[2].set_ylabel("Average CPC", fontsize=8)

        # set the label and title for plots
        plt.xlabel(f"Age Group")
        axes[0].set_title(
            f'''Average CPC, Total Spent, and Total Approved Conversion
            across Age Group for Campaign ID: {selected_campaign_id}''')
        plt.tight_layout()

        # create output folder
        if not os.path.exists('output'):
            os.makedirs('output')

        # save plot
        plt.savefig('output/plot.png', bbox_inches='tight')

        # send plot
        bot.send_chat_action(chat_id, 'upload_photo')
        with open('output/plot.png', 'rb') as img:
            bot.send_photo(chat_id, img)

        # extract minimum and maximum values of index
        min_spent_age = df_plot['spent'].idxmin()
        max_spent_age = df_plot['spent'].idxmax()
        min_approved_age = df_plot['approved_conversion'].idxmin()
        max_approved_age = df_plot['approved_conversion'].idxmax()
        min_cpc_age = df_plot['cpc'].idxmin()
        max_cpc_age = df_plot['cpc'].idxmax()

        # VOICE MESSAGE
        plot_info = list(zip(
            ['Spent', 'Approved Conversion', 'CPC'],
            [max_spent_age, max_approved_age, max_cpc_age],
            [min_spent_age, min_approved_age, min_cpc_age]))

        plot_text = f'This is your requested plot for Campaign ID {selected_campaign_id}.\n'
        for col, maxi, mini in plot_info:
            text = f"Age group with the highest {col} is {maxi}, while the lowest is {mini}.\n"
            plot_text += text

        # save voice message
        speech = gTTS(text = plot_text)
        speech.save('output/plot_info.ogg')

        # send voice message
        with open('output/plot_info.ogg', 'rb') as f:
            bot.send_voice(chat_id, f)
    else:
        bot.send_message(chat_id, 'Campaign ID not found. Please try again!')
        ask_id_plot(message)

# --------------------- IMPROVE --------------------------
df_ws = pd.read_csv("./data_input/dataset_kalibrr.csv")
df_ws['Posted'] = pd.to_datetime(df_ws['Posted'])
df_ws['Deadline'] = pd.to_datetime(df_ws['Deadline'])

@bot.message_handler(commands=['webscraping'])
def ask_wfh(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    wfh = message.from_user.id

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Data WFH")
    markup.add("Data WFO")
    sent = bot.send_message(wfh, 'Choose to be plot:', reply_markup=markup)

    bot.register_next_step_handler(sent, send_plot_ws)

def send_plot_ws(message):
    # TO DO: chat_id (SAME AS CHECKPOINT 1)
    chat_id = message.from_user.id
    selected_w = message.text
    if selected_w == "Data WFO":
        selected_w = "No"
    else: 
        selected_w = "Yes"
    if selected_w in ["Yes", "No"]:
        # TO DO: find the range date
        wf = lambda x: "WFH" if x == "Yes" else "WFO"
        df_wf = df_ws.loc[df_ws['WFH'] == selected_w]

        today = datetime.today()

        one_week_ago = today - timedelta(days=7)
        new_jobs_df = df_wf[df_wf['Posted'] >= one_week_ago]

        new_jobs = new_jobs_df['Title'].count()

        # Cities
        top_cities = new_jobs_df['Kota'].value_counts().head(3)
        top_cities.plot(kind='bar', color=['#AE2024', '#000000', '#FFC20E'], figsize=(8,6))
        plt.title(f'Top 3 Cities with the Most Newly Opened {wf(selected_w)} Jobs in the Past Week', fontsize=14, fontweight='bold')
        plt.xlabel('Kota', fontsize=12)
        plt.ylabel('Jumlah Job', fontsize=12)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.tight_layout()

        # create output folder
        if not os.path.exists('output'):
            os.makedirs('output')

        # save plot
        plt.savefig('output/plot_ws_1.png', bbox_inches='tight')

        # send plot
        bot.send_chat_action(chat_id, 'upload_photo')
        with open('output/plot_ws_1.png', 'rb') as img:
            bot.send_photo(chat_id, img)

        # Companies
        company = new_jobs_df.groupby('Company').size().reset_index(name='Job Count')

        company = company.sort_values('Job Count', ascending=False)
        top_company = company.iloc[0]
        print(f'{top_company[0]} Sebanyak : {top_company[1]}')

        fig, ax = plt.subplots(figsize=(8,6))
        ax.bar(company['Company'][:3], company['Job Count'][:3], color=['#AE2024', '#000000', '#FFC20E'])
        ax.set_title(f'Top 3 Companies with Most Newly Opened {wf(selected_w)} Jobs in the Past Week')
        ax.set_xlabel('Company')
        ax.set_ylabel('Job Count')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        # create output folder
        if not os.path.exists('output'):
            os.makedirs('output')

        # save plot
        plt.savefig('output/plot_ws_2.png', bbox_inches='tight')

        # send plot
        bot.send_chat_action(chat_id, 'upload_photo')
        with open('output/plot_ws_2.png', 'rb') as img:
            bot.send_photo(chat_id, img)

        plot_text = f'In the past week, there were a total of {new_jobs} new job openings {wf(selected_w)} positions. The city with the highest number of job openings is {top_cities.index[0]}, with {top_cities[0]} openings. The company that posted the most job openings is {top_company[0]}, with a total of {top_company[1]} openings.'

        speech = gTTS(text = plot_text)
        speech.save('output/plot_info_ws.ogg')
        
        with open('output/plot_info_ws.ogg', 'rb') as f:
            bot.send_voice(chat_id, f)
    else:
        bot.send_message(chat_id, 'Error')
        ask_id_summary(message)

# -------------------- CHECKPOINT 4 --------------------
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # TO DO: emoji
    with open('template_text/default.txt', mode='r', encoding='utf-8') as f:
        temp = Template(f.read())
        default = temp.substitute(EMOJI = emoji.emojize(':pensive_face:'))
        
    bot.reply_to(message, default)


if __name__ == "__main__":
    bot.polling()